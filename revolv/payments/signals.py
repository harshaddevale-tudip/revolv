from django.db.models import signals, Sum
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

from revolv.base.models import RevolvUserProfile
from revolv.base.utils import is_user_reinvestment_period
from django.contrib.auth.models import Group
from revolv.project.models import Project
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType, RepaymentFragment, UserReinvestment)
from revolv.payments.utils import (NotEnoughFundingException, NotInUserReinvestmentPeriodException,
                                   ProjectNotCompleteException, NotInAdminReinvestmentPeriodException,
                                   ProjectNotEligibleException)



@receiver(signals.post_save, sender=AdminRepayment)
def post_save_admin_repayment(**kwargs):
    """
    When an AdminRepayment is saved, a RepaymentFragment is generated for all
    donors to a project, each weighed by that donor's proportion of the
    contribution to the project.
    """
    if not kwargs.get('created'):
        return
    instance = kwargs.get('instance')
    for donor in instance.project.donors.all():
        amount = instance.project.proportion_donated(donor) * instance.amount
        repayment = RepaymentFragment(user=donor,
                                      project=instance.project,
                                      admin_repayment=instance,
                                      amount=amount
                                      )
        # user's reinvest_pool will be incremented on save
        repayment.save()

@receiver(m2m_changed, sender=Project.ambassadors.through)
def post_save_user_groups(**kwargs):
    """
    When an project is saved, Check the project ambassador and add user to the
    ambassador group.
    """

    if not kwargs.get('instance'):
        return
    instance = kwargs.get('instance')
    ambassadors=[]
    projects = Project.objects.all()
    for project in projects:
        for ambassador in project.ambassadors.all():
            user = User.objects.get(id=ambassador.user_id)
            ambassadors.append(user)

    group=Group.objects.get(name='ambassadors')
    for user in group.user_set.all():
        if user.username != 'administrator':
            group.user_set.remove(user)

    group=Group.objects.get(name='ambassadors')
    for ambassador in ambassadors:
        group.user_set.add(ambassador)


@receiver(signals.post_save, sender=RepaymentFragment)
def post_save_repayment_fragment(**kwargs):
    """
    When a RepaymentFragment is saved, we increment the reinvest_pool in the
    related user.
    """
    if not kwargs.get('created'):
        return
    instance = kwargs.get('instance')
    instance.user.reinvest_pool += float(instance.amount)
    instance.user.save()


@receiver(signals.pre_delete, sender=RepaymentFragment)
def pre_delete_repayment_fragment(**kwargs):
    """
    Before a RepaymentFragment is deleted, we decrement the reinvest_pool in the
    related user.
    """
    instance = kwargs.get('instance')
    instance.user.reinvest_pool -= float(instance.amount)
    instance.user.save()


@receiver(signals.post_save, sender=Payment)
def post_save_payment(**kwargs):
    """
    If the payment is organic, we add this payment's user as a donor to the
    related project. If the payment is a reinvestment, we decrement the
    reinvest_pool in the related user.
    """
    if not kwargs.get('instance'):
        return
    instance = kwargs.get('instance')
    # if instance.is_organic:
    if instance.project:
        instance.project.donors.add(instance.user)
        for donor in instance.project.donors.all():
            payment_count = Payment.objects.filter(user=donor).count()
            if payment_count == 0:
                instance.project.donors.remove(donor)

    if instance.payment_type == PaymentType.objects.get_reinvestment_fragment():
        instance.user.reinvest_pool -= float(instance.amount)
        instance.user.reinvest_pool = float(format(round(instance.user.reinvest_pool, 2)))
        instance.user.save()


@receiver(signals.pre_delete, sender=Payment)
def pre_delete_payment(**kwargs):
    """
    Before a Payment is deleted, if it is a reinvestment, we increment the
    reinvest_pool in the related user.
    """
    instance = kwargs.get('instance')
    # if instance.is_organic:
    donation_count = instance.project.payment_set.filter(
                user=instance.user).count()
    if donation_count == 1:
        instance.project.donors.remove(instance.user)
    if instance.payment_type == PaymentType.objects.get_reinvestment_fragment():
        instance.user.reinvest_pool += float(instance.amount)
        instance.project.monthly_reinvestment_cap += float(instance.amount)
        instance.user.save()


@receiver(signals.post_delete, sender=Payment)
def post_delete_payment(**kwargs):
    """
    We need to cleanup here. If this related to UserReinvestment then just delete it.
    For AdminReinvestment we need some checking
    """
    instance = kwargs.get('instance')
    if not instance.user_reinvestment:
        return
    else:
        instance.user_reinvestment.delete()
    if instance.admin_reinvestment:
        admin_reinvestment = instance.admin_reinvestment
        admin_reinvestment.amount -= float(instance.amount)
        if admin_reinvestment.payment_set.all().count() == 0:
            admin_reinvestment.delete()


@receiver(signals.post_save, sender=UserReinvestment)
def post_save_user_reinvestment(**kwargs):
    """
    When an AdminReinvestment is saved, we pool as many donors as we need to
    fund the reinvestment, prioritizing users that have a preference for the
    Category of the project begin invested into. We only consider users that
    have a non-zero pool of investable money.

    """
    if not kwargs.get('created'):
        return
    instance = kwargs.get('instance')
    reinvestment = Payment(user=instance.user,
                           project=instance.project,
                           entrant=instance.user,
                           payment_type=PaymentType.objects.get_reinvestment_fragment(),
                           user_reinvestment=instance,
                           amount=instance.amount
                           )
    if instance.project.amount_donated >= instance.project.funding_goal:
        instance.project.project_status = instance.project.COMPLETED
        instance.project.save()
        # user's reinvest_pool will be decremented on this Payment's save
    reinvestment.save()
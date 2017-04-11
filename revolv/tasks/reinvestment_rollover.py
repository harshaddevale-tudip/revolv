from django.conf import settings

from revolv.project.models import Project
from revolv.payments.models import ProjectMontlyRepaymentConfig, AdminReinvestment, PaymentType, Payment
from revolv.base.models import RevolvUserProfile
from django.db.models import Sum

from celery.task import task

import sys
import time
import logging

logger = logging.getLogger("revolv")


@task
def distribute_reinvestment_fund():
    """
    This task is for Automatic reinvestment

    This is how this script do:
    1. Get all project that is eligible for reinvestment:
        (project with monthly_reinvestment_cap >0 and not fully funded)
    2. For each project determine how we'll reinvest
    3. Add AdminReinvestment object with above value
    4. Reinvestment every user's reinvestment amount in project funding proportion.
    """

    time.sleep(60)
    ADMIN_PAYMENT_USERNAME = settings.ADMIN_PAYMENT_USERNAME

    try:
        admin = RevolvUserProfile.objects.get(user__username=ADMIN_PAYMENT_USERNAME)
    except RevolvUserProfile.DoesNotExist:
        logger.error("Can't find admin user: {0}. System exiting!".format(ADMIN_PAYMENT_USERNAME))
        sys.exit()

    reinvest_amount_left = RevolvUserProfile.objects.all().aggregate(total=Sum('reinvest_pool'))['total']
    total_funding_goal = Project.objects.get_active().aggregate(total=Sum('funding_goal'))['total']
    pending_reinvestors = []

    users = RevolvUserProfile.objects.filter(reinvest_pool__gt=0.0)
    for user in users:
        reinvest_pool=user.reinvest_pool
        pending_reinvestors.append((user, reinvest_pool))
    for project in Project.objects.get_active():
        reinvest_amount_praportion = float(project.funding_goal)/float(total_funding_goal)
        reinvest_amount=float(reinvest_amount_praportion)*float(reinvest_amount_left)
        reinvest_amount=float("{0:.2f}".format(reinvest_amount))

        adminReinvestment=AdminReinvestment.objects.create(
            amount=reinvest_amount,
            admin=admin,
            project=project
        )

        for (user, reinvest_pool) in pending_reinvestors:
            reinvest_amount_left=user.reinvest_pool
            amount = reinvest_pool * float("{0:.2f}".format(reinvest_amount_praportion))
            logger.info('Trying to reinvest %s in %s project!',format(round(amount,2)),project.title)
            reinvestment = Payment(user=user,
                                   project=project,
                                   entrant=admin,
                                   payment_type=PaymentType.objects.get_reinvestment_fragment(),
                                   admin_reinvestment=adminReinvestment,
                                   amount=format(round(amount,2))
                                   )

            if project.amount_donated >= project.funding_goal:
                project.project_status = project.COMPLETED
                project.save()
            reinvestment.save()

    for user in users:
        if user.reinvest_pool <= 0.01:
            user.reinvest_pool = 0
            user.save()
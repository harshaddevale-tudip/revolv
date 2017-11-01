from django.db.models import Sum
from revolv.payments.models import Payment, UserReinvestment
from revolv.project.models import Project


def humanize_int(n):
    # NOTE: GPL licensed snipped c/o
    # https://github.com/localwiki/localwiki-backend-server/blob/master/localwiki/users/views.py#L47
    mag = 0
    if n < 1000:
        return str(n)
    while n>= 1000:
        mag += 1
        n /= 1000.0
    return '%.1f%s' % (n, ['', 'k', 'M', 'B', 'T', 'P'][mag])


def humanize_integers(d):
    for k in d:
        d[k] = humanize_int(int(d[k]))

def get_solar_csv_url(csv_id, mode):
    """Gets request url to export csv for project with that id.
    Mode represents daily, monthly or annual values based on whether
    it is 1, 2, or 3 respectively."""

    url = "http://home.solarlog-web.net/sds/modul/SolarLogWeb/Statistik.php?logid=0&c="
    url += csv_id + "&mode=" + str(mode) + "&offset=0&flag=32&ex=csv"
    return url

def aggregate_stats(user_profile):
    """Aggregates statistics about a Re-volv user's impact and returns a dictionary with 
    these values. These values are later presented on the user's dashboard.
    """
    stat_dict = {}
    stat_dict['project_count'] = Project.objects.donated_projects(user_profile).count()
    stat_dict['repayments'] = Payment.objects.repayment_fragments(user=user_profile).aggregate(Sum('amount'))['amount__sum'] or 0
    admin_reinvestment = Payment.objects.filter(user=user_profile).filter(admin_reinvestment__isnull=False).aggregate(Sum('amount'))['amount__sum'] or 0
    user_reinvestment = UserReinvestment.objects.filter(user=user_profile).aggregate(Sum('amount'))['amount__sum'] or 0
    stat_dict['reinvestment'] = admin_reinvestment + user_reinvestment
    stat_dict['trees'] = user_profile.user_impact_of_acr_of_tree_save()
    stat_dict['kwh'] = user_profile.user_impact_for_watts()
    stat_dict['carbon_dioxide'] = user_profile.user_impact_for_carbon_dioxide()

    return stat_dict


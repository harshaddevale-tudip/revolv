from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE,
        'stripe_api_key': settings.STRIPE_SECRET_KEY
    }
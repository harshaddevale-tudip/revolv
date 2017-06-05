from django.contrib import admin

from .models import RevolvUserProfile

admin.site.register(RevolvUserProfile)

class RevolvUserProfileadmin(admin.ModelAdmin):

    search_fields = ('user__username','user__first_name','user__email','user__last_name',)

admin.site.unregister(RevolvUserProfile)
admin.site.register(RevolvUserProfile, RevolvUserProfileadmin)
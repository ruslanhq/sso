from django.contrib import admin

from authentication.models import User, Groups, EcomInformation

admin.site.register(User)
admin.site.register(Groups)
admin.site.register(EcomInformation)

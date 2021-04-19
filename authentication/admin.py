from django.contrib import admin

from authentication.models import User, Groups

admin.site.register(User)
admin.site.register(Groups)

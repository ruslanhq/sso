from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls', namespace='authentication')),
]

if settings.DEBUG:
    urlpatterns += [
        path('docs', include_docs_urls(title='SSO Doc'))
    ]

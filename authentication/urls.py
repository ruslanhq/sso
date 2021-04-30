from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import UserViewSet, CustomTokenObtainPairView

app_name = 'authentication'

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]

urlpatterns += router.urls

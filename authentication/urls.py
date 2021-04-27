from rest_framework.routers import DefaultRouter

from authentication.views import UserViewSet

app_name = 'authentication'

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')


urlpatterns = router.urls

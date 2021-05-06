from rest_framework.routers import DefaultRouter

from private_api.views import UserViewSet

app_name = 'private_api'

router = DefaultRouter()
router.register('get_user', UserViewSet, basename='get_user')

urlpatterns = router.urls

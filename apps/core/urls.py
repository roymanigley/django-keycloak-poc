from apps.core import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'dummy', views.DummyViewSet)

urlpatterns = router.urls


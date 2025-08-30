from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'agents', views.AgentUserViewSet)
router.register(r'cameras', views.CameraViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'reports', views.RapportViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'accounts', views.CompteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]

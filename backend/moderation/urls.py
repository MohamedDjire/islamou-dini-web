from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, BanViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'bans', BanViewSet, basename='ban')

urlpatterns = [
    path('', include(router.urls)),
]

"""
URL configuration for communities app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'communities', views.CommunityViewSet, basename='community')
router.register(r'lives', views.LiveViewSet, basename='live')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'channels/<int:channel_id>/threads/',
        views.ChannelThreadViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='channel-threads'
    ),
    path(
        'channels/<int:channel_id>/threads/<int:pk>/',
        views.ChannelThreadViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='thread-detail'
    ),
    path(
        'channels/<int:channel_id>/threads/<int:pk>/reply/',
        views.ChannelThreadViewSet.as_view({'post': 'reply'}),
        name='thread-reply'
    ),
]

"""
URL configuration for social app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'reels', views.ReelViewSet, basename='reel')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('trending/hashtags/', views.TrendingHashtagsView.as_view(), name='trending-hashtags'),
    path('bookmarks/', views.BookmarkedContentView.as_view(), name='bookmarks'),
]

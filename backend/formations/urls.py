"""
URL configuration for formations app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'formations', views.FormationViewSet, basename='formation')
router.register(r'enrollments', views.EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmarks'),
    path(
        'formations/<slug:formation_slug>/modules/',
        views.ModuleViewSet.as_view({'get': 'list'}),
        name='formation-modules'
    ),
    path(
        'formations/<slug:formation_slug>/modules/<int:pk>/',
        views.ModuleViewSet.as_view({'get': 'retrieve'}),
        name='module-detail'
    ),
    path(
        'formations/<slug:formation_slug>/modules/<int:pk>/progress/',
        views.ModuleViewSet.as_view({'post': 'progress'}),
        name='module-progress'
    ),
]

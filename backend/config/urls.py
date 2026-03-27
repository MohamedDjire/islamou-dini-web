"""
URL configuration for islamou-dini backend.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('users/', include('users.urls')),
    path('formations/', include('formations.urls')),
    path('social/', include('social.urls')),
    path('communities/', include('communities.urls')),
    path('messaging/', include('messaging.urls')),
    path('moderation/', include('moderation.urls')),
    
    # Health check
    path('health/', include('config.health_urls')),
]

"""
Health check endpoint
"""

from django.urls import path
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'service': 'islamou-dini-django-backend'
    })


urlpatterns = [
    path('', health_check, name='health_check'),
]

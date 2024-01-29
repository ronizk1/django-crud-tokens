"""
apppppppppppppp
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

from base import views
from base import views

urlpatterns = [
    path('', views.index),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('private', views.private),
    path('register/', views.register),
    path('products', views.products),
    path('products/<int:id>',views.products),
    path('refresh', TokenRefreshView.as_view(), name='token_resresh'),
    
]

# Add URL patterns for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
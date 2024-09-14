"""
URL configuration for barbershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from scheduling import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scheduling.urls')),  # Include your app's URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's built-in auth views
    path('register/', views.register, name='register'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('barber_dashboard/', views.barber_dashboard, name='barber_dashboard'),
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),
    path('profile/', views.profile, name='profile'),  # Add this for the profile page
]

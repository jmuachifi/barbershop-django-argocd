from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('barber_dashboard/', views.barber_dashboard, name='barber_dashboard'),
    path('appointment/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointment/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('appointment/mark_completed/<int:appointment_id>/', views.mark_as_completed, name='mark_as_completed'),
]

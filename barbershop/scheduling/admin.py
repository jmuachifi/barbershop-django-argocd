from django.contrib import admin
from .models import User, Appointment, Barber

# Custom admin for the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')  # Display these fields in the admin list view
    search_fields = ('username', 'email')  # Search by these fields
    list_filter = ('role',)  # Filter users by their role

# Custom admin for the Barber model
@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience')  # Display the barber's user and experience
    search_fields = ('user__username',)  # Search barbers by username
    list_filter = ('experience',)  # Filter by experience

# Custom admin for the Appointment model
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('barber', 'customer', 'date_time')  # Show appointments with barber, customer, and date
    search_fields = ('barber__user__username', 'customer__username')  # Search by barber and customer username
    list_filter = ('date_time',)  # Filter by appointment date

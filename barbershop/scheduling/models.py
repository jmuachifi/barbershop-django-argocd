from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('barber', 'Barber'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    # Add related_name to avoid conflict with built-in Django User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Barber Model (for additional fields, if needed)
class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.IntegerField(null=True, blank=True)  # Example field

    def __str__(self):
        return self.user.username

# Appointment Model
class Appointment(models.Model):
    barber = models.ForeignKey(
        User, 
        limit_choices_to={'role': 'barber'}, 
        on_delete=models.CASCADE, 
        related_name='barber_appointments'
    )
    customer = models.ForeignKey(
        User, 
        limit_choices_to={'role': 'customer'}, 
        on_delete=models.CASCADE, 
        related_name='customer_appointments'
    )
    date_time = models.DateTimeField()
    completed = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"Appointment with {self.barber.username} and {self.customer.username} on {self.date_time}"

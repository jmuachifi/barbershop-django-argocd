from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, Barber, Appointment
from .forms import UserRegisterForm, AppointmentForm
from django.contrib import messages


# Home View
def home(request):
    return render(request, "scheduling/home.html")


# Register View
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "scheduling/register.html", {"form": form})


# Dashboard Views
@login_required
def customer_dashboard(request):
    # Fetch all appointments where the customer is the logged-in user
    appointments = Appointment.objects.filter(customer=request.user)

    # Fetch all barbers (for booking a new appointment)
    barbers = User.objects.filter(role='barber')

    # Appointment form for booking a new appointment
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = request.user
            appointment.barber = User.objects.get(id=request.POST['barber_id'])
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('customer_dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'scheduling/customer_dashboard.html', {
        'appointments': appointments,
        'barbers': barbers,
        'form': form
    })


@login_required
def barber_dashboard(request):
    appointments = Appointment.objects.filter(barber=request.user)
    return render(
        request, "scheduling/barber_dashboard.html", {"appointments": appointments}
    )


@login_required
def profile(request):
    return render(request, "scheduling/profile.html")


@login_required
def redirect_after_login(request):
    if request.user.role == "customer":
        return redirect("customer_dashboard")
    elif request.user.role == "barber":
        return redirect("barber_dashboard")
    else:
        return redirect("home")  # Or some other default page


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('customer_dashboard')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'scheduling/edit_appointment.html', {'form': form, 'appointment': appointment})

def cancel_appointment(request, appointment_id):
    # Check if the logged-in user is either the customer or the barber for the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure that the current user is either the customer or the barber
    if appointment.customer != request.user and appointment.barber != request.user:
        messages.error(request, "You don't have permission to cancel this appointment.")
        return redirect('home')

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment canceled successfully!')
        # Redirect based on the user role
        if request.user == appointment.customer:
            return redirect('customer_dashboard')
        elif request.user == appointment.barber:
            return redirect('barber_dashboard')

    return render(request, 'scheduling/cancel_appointment.html', {'appointment': appointment})

def mark_as_completed(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, barber=request.user)
    
    if request.method == 'POST':
        appointment.completed = True
        appointment.save()
        messages.success(request, 'Appointment marked as completed!')
        return redirect('barber_dashboard')

    return render(request, 'scheduling/mark_as_completed.html', {'appointment': appointment})



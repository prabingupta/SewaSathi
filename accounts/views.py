from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import RegisterForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to SewaSaathi, {user.username}! Your account has been created.")

            if user.role == User.Role.PROVIDER:
                messages.info(request, "Just one more step — tell us about your services.")
                return redirect('provider_complete_profile')

            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return reverse_lazy('home')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

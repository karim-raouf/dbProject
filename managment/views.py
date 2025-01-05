from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login as auth_login 
from .models import *
# Create your views here.

def login(request):
    context = {'error': False}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                auth_login(request, user)
                return redirect('dashboard')
            else:
                # messages.error(request, "Invalid username or password!")
                context['error'] = True
                print('Error flag:', context['error'])
                
        except Exception as e:       
            print(f'An error occurred: {e}')
            context['error'] = True
            print('Error flag:', context['error'])
    
    return render(request, "login.html", context)


def logout(request):
    auth_logout(request)  # Logs out the user
    # messages.success(request, "You have been logged out successfully.")
    return redirect("login")

def dashboard(request):
    context={}
    return render(request, 'dashboard.html' , context)

def inventory(request):
    context={}
    return render(request, 'inventory.html' , context)

def orders(request):
    context={}
    return render(request, 'orders.html' , context)

def reports(request):
    context={}
    return render(request, 'reports.html' , context)

def suppliers(request):
    context={}
    return render(request, 'suppliers.html' , context)

def settings(request):
    context={}
    return render(request, 'settings.html' , context)

def product(request):
    context={}
    return render(request, 'product.html' , context)

def alerts(request):
    context={}
    return render(request, 'alerts.html' , context)
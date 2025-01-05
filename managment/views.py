from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login as auth_login 
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.

def login(request):
    context = {'error': False}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("1")
        try:
            user = User.objects.get(username=username)
            print("2")
            if user.check_password(password):
                print("3")
                auth_login(request, user)
                print("4")
                return redirect('dashboard')
            else:
                # messages.error(request, "Invalid username or password!")
                print("5")
                context['error'] = True
                print('Error flag:', context['error'])
                
        except Exception as e:     
            print("6")  
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
    products = Product.objects.all()
    inventory = Inventory.objects.all()
    context={"inventory" : inventory , "products": products}
    return render(request, 'inventory.html' , context)

def orders(request):
    orders = Order.objects.all()
    context={"orders" : orders}
    return render(request, 'orders.html' , context)

def reports(request):
    context={}
    return render(request, 'reports.html' , context)

def suppliers(request):
    suppliers = Supplier.objects.all()
    products = Product.objects.all() 
    context={"suppliers" : suppliers , "products" : products}
    return render(request, 'suppliers.html' , context)

def add_supplier(request):
    
    context={}
    return render(request, 'add_supplier.html' , context)

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")

        try:
            # Create a new User instance
            user = User(
                username=username,
                phone_number=phone,
                email=email,
                role=role,
                password=make_password(password),  # Hash the password
            )
            user.save()
            messages.success(request, "User added successfully!")
            return redirect('add-user')  # Redirect to a success page or refresh the form
        except Exception as e:
            messages.error(request, f"Error adding user: {e}")
    context={}
    return render(request, 'add_user.html' , context)

def settings(request):
    if request.method == "POST":
        # Iterate through posted data to update inventory
        for key, value in request.POST.items():
            if key.startswith("lowstock_"):  # Look for keys matching the pattern
                try:
                    inventory_id = key.split("_")[1]  # Extract the inventory ID
                    inventory_instance = Inventory.objects.get(id=inventory_id)
                    inventory_instance.low_stock_alert = int(value)  # Update lowstock
                    inventory_instance.save()
                except (Inventory.DoesNotExist, ValueError):
                    messages.error(request, f"Error updating inventory ID: {inventory_id}")

        messages.success(request, "Low stock thresholds updated successfully!")
        return redirect("settings")  # Replace with the name of your view
    
    # Fetch inventory and render the page for GET requests
    inventory = Inventory.objects.all()
    return render(request, "settings.html", {"inventory": inventory})

def product(request):
    context={}
    return render(request, 'product.html' , context)

def alerts(request):
    inventory = Inventory.objects.all()
    context={"inventory" : inventory}
    return render(request, 'alerts.html' , context)
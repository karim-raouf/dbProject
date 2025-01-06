from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, login as auth_login 
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import *
from django.utils import timezone
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
                if user.role == "Admin":
                    return redirect('dashboard')
                else:
                    return redirect('orders')
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
    new_orders = Order.objects.filter(status="Pending").count()
    all_orders = Order.objects.count()
    num_suppliers = Supplier.objects.count()
    num_products = Product.objects.count()
    context={"new_orders" : new_orders , "all_orders" : all_orders , "num_suppliers" : num_suppliers, "num_products" : num_products}
    return render(request, 'dashboard.html' , context)

def inventory(request):
    products = Product.objects.all().prefetch_related('inventory')
    context = {
        'products': products,
    }
    return render(request, 'inventory.html' , context)

def orders(request):
    if request.user.role == "Admin":
        orders = Order.objects.all()
    else:
        supplier = request.user.supplier_profile
        orders = Order.objects.filter(supplier=supplier)
    context={"orders" : orders}
    return render(request, 'orders.html' , context)

def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Ensure the user is a supplier and the order status is "Pending"
    if request.user.role == "Supplier" and order.status == "Pending":
        order.status = "Shipped"
        order.save()

    return redirect('orders')

def receive_order(request, order_id):
    # Retrieve the order or return a 404 if not found
    order = get_object_or_404(Order, id=order_id)
    
    # Check if the user is an Admin and the order status is "Shipped"
    if request.user.role == "Admin" and order.status == "Shipped":
        try:
            # Retrieve the associated product and inventory
            product = order.product
            inventory = Inventory.objects.get(product=product)
            
            # Update inventory stock level
            inventory.stock_level += order.quantity
            inventory.save()
            
            # Update the order status and received date
            order.status = "Received"
            order.received_date = timezone.now()
            order.save()
            
            # Add a success message
            messages.success(request, f"Order #{order.id} marked as received, and inventory updated.")
        except Inventory.DoesNotExist:
            # Handle cases where inventory for the product doesn't exist
            messages.error(request, f"Inventory not found for product: {product.name}.")
    else:
        # Add an error message if conditions are not met
        messages.error(request, "You are not authorized to receive this order or the order status is not 'Shipped'.")
    
    # Redirect back to the orders page
    return redirect('orders')

def reports(request):
    context={}
    return render(request, 'reports.html' , context)

def suppliers(request):
    suppliers = Supplier.objects.all()
    products = Product.objects.all() 
    context={"suppliers" : suppliers , "products" : products}
    return render(request, 'suppliers.html' , context)

def add_supplier(request):
    if request.method == 'POST':
        form = supplierForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the form data and create a new Supplier instance
            form.save()
            
            # Redirect to a success page or supplier list page after saving
            return redirect('suppliers')  # Modify this to your actual redirect URL
            
        else:
            # If the form is not valid, return the form with error messages
            return render(request, 'add_supplier.html', {'form': form})
    
    # If the request is GET, show the empty form
    else:
        form = supplierForm()
    context={"form" : form}
    return render(request, 'add_supplier.html' , context)

def add_order(request):
    if request.method == 'POST':
        form = orderForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the form data and create a new Supplier instance
            form.save()
            # Redirect to a success page or supplier list page after saving
            return redirect('orders')  # Modify this to your actual redirect URL
            
        else:
            return render(request, 'add_order.html', {'form': form})
    
    # If the request is GET, show the empty form
    else:
        form = orderForm()
    context={"form" : form}
    return render(request, 'add_order.html' , context)

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


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Save the product instance
            product = form.save()

            # Now create an Inventory instance related to the product
            # You can set default values for other fields in Inventory
            inventory = Inventory.objects.create(
                product=product,   # Assign the newly created product
                stock_level=0,      # Default stock level, can be customized
                low_stock_alert=0  # Default low stock alert value
            )

            # Redirect to the inventory page or wherever you want
            return redirect('inventory')
    else:
        form = ProductForm()  # Create a new empty form when GET request is made
    
    return render(request, 'add_product.html', {'form': form})

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
from django import forms
from .models import *
from managment.models import *
from django.forms import widgets
from django.contrib.auth.hashers import make_password
import re


class supplierForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(supplier_profile__isnull=True , role="Supplier"),
        widget=forms.Select(attrs={'class': 'user-select'}),
        required=True  # Make this required if needed
    )
    
    start_date = forms.DateField(
        widget=widgets.TextInput(attrs={'placeholder': 'Enter Start Date...', 'id': 'start-date', 'type': 'date'}),
        required=True  # Set required to True
    )
    
    # Change end_date to DateField for proper date handling and make it required
    end_date = forms.DateField(
        widget=widgets.TextInput(attrs={'placeholder': 'Enter End Date...', 'id': 'end-date', 'type': 'date'}),
        required=True  # Set required to True
    )
    
    class Meta:
        model = Supplier
        fields = ['user','start_date' , 'end_date']
        
        
        
class ProductForm(forms.ModelForm):
    # Include a ModelChoiceField for Supplier
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(products__isnull=True),
        widget=forms.Select(attrs={'class': 'supplier-select'}),
        required=True,
        label="Supplier"
    )
    
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
        required=True,
        label="Product Name"
    )
    
    sku = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SKU'}),
        required=True,
        label="SKU"
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter product description'}),
        required=True,
        label="Description"
    )
    
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price'}),
        required=True,
        label="Price"
    )
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'price', 'supplier']
        
        

class orderForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'user-select'}),
        required=True  # Make this required if needed
    )
    
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.Select(attrs={'class': 'user-select'}),
        required=True  # Make this required if needed
    )
    
    # Change end_date to DateField for proper date handling and make it required
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Quantity...', 'id': 'quantity', 'type': 'number'}),
        required=True
    )
    
    class Meta:
        model = Order
        fields = ['product','supplier' , 'quantity']
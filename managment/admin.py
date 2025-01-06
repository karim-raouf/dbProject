from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Order)


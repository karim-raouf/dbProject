from .models import *

def global_variables(request):
    num = 0
    inventory = Inventory.objects.all()
    for item in inventory:
        if item.stock_level <= item.low_stock_alert:
            num += 1
            
    return{"num" : num}





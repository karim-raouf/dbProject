from django.urls import path
from . import views

urlpatterns = [
    path('', views.login , name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard , name="dashboard"),
    path('inventory/', views.inventory , name="inventory"),
    path('reports/', views.reports , name="reports"),
    path('orders/', views.orders , name="orders"),
    path('suppliers/', views.suppliers , name="suppliers"),
    path('settings/', views.settings , name="settings"),
    path('product/', views.product , name="product"),
    path('alerts/', views.alerts , name="alerts"),
    path('add-supplier/', views.add_supplier , name="add-supplier"),
    path('add-user/', views.add_user , name="add-user"),
    path('add-product/', views.add_product , name="add-product"),
    path('add-order/', views.add_order , name="add-order"),
    path('order/accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('order/receive/<int:order_id>/', views.receive_order, name='receive_order'),
]
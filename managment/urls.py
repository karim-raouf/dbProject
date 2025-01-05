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
]
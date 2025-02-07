from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    path("", views.all_orders, name="all_orders"),
    path("create/", views.create_order, name="create_order"),
    path("close/", views.close_order, name="close_order"),
    path('orders/add/', views.add_order, name='add_order'),
    path('orders/edit/<int:pk>/', views.edit_order, name='edit_order'),
]

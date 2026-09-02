from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    path("", views.OrderListView.as_view(), name="all_orders"),
    path("create/", views.OrderCreateView.as_view(), name="create_order"),
    path("<int:pk>/close/", views.OrderCloseView.as_view(), name="close_order"),
]

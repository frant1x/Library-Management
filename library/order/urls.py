from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    path("", views.OrderListView.as_view(), name="order_list"),
    path("<int:book_id>/create/", views.OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>/close/", views.OrderCloseView.as_view(), name="order_close"),
]

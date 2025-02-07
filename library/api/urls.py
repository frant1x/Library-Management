from django.urls import path, include
from . import views
from rest_framework_nested import routers

user_router = routers.SimpleRouter()
user_router.register("user", views.UserView, basename="users_view")

user_order_router = routers.NestedSimpleRouter(user_router, "user", lookup="user")
user_order_router.register("order", views.UserOrderView, basename="user-order")

author_router = routers.DefaultRouter()
author_router.register("author", views.AuthorView, basename="author_view")

book_router = routers.DefaultRouter()
book_router.register("book", views.BookView, basename="book_view")

order_router = routers.DefaultRouter()
order_router.register("order", views.OrderView, basename="order_view")


app_name = "api"
urlpatterns = [
    path("v1/", include(user_router.urls)),
    path("v1/", include(user_order_router.urls)),
    path("v1/", include(author_router.urls)),
    path("v1/", include(book_router.urls)),
    path("v1/", include(order_router.urls)),
]

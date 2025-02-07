# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from order.models import Order
from .forms import *


def home(request):
    return render(request, "authentication/home.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse("authentication:login"))
    form = RegistrationForm()
    return render(request, "authentication/register.html", {"form": form})


def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("authentication:home"))
    form = LoginForm()
    return render(request, "authentication/log_in.html", {"form": form})


def log_out(request):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    logout(request)
    return redirect(reverse("authentication:home"))


def show_users(request):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    users = CustomUser.get_all()
    context = {"users": users}
    return render(request, "authentication/users.html", context=context)


def show_user(request, user_id):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    if request.user.is_superuser or request.user.id == user_id:
        user = CustomUser.get_by_id(user_id)
        if request.method == "POST":
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect(reverse("authentication:show_users"))
        form = UserForm(instance=user)
        context = {"form": form}
        return render(request, "authentication/user.html", context=context)
    else:
        return redirect(reverse("authentication:show_users"))


def show_user_books(request, user_id):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    if request.user.is_superuser or request.user.id == user_id:
        user = CustomUser.get_by_id(user_id)
        books = user.books.all()
        context = {"books": books, "user_name": user.first_name, "filter": False}
        return render(request, "book/books.html", context=context)
    else:
        return redirect(reverse("book:all_books"))


def show_user_orders(request, user_id):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    if request.user.is_superuser or request.user.id == user_id:
        user = CustomUser.get_by_id(user_id)
        orders = Order.objects.filter(user=user)
        context = {"orders": orders}
        return render(request, "order/orders.html", context=context)
    else:
        return redirect(reverse("authentication:home"))

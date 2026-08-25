from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import User

# from order.models import Order
from .forms import RegistrationForm, LoginForm, UserForm


def register(request):
    """View for user registration."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("authentication:login")
    else:
        form = RegistrationForm()

    return render(request, "authentication/register.html", {"form": form})


def log_in(request):
    """View for user login."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, "authentication/log_in.html", {"form": form})


@login_required
def log_out(request):
    logout(request)
    return redirect("home")


@login_required
def show_users(request):
    users = User.objects.all().order_by("id")
    context = {"users": users}
    return render(request, "authentication/users.html", context=context)


@login_required
def show_user(request, user_id):
    if request.user.is_superuser or request.user.id == user_id:
        user = get_object_or_404(User, user_id)

        if request.method == "POST":
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()

                if request.user.is_staff:
                    return redirect("authentication:show_users")
                return redirect(reverse("authentication:show_user", user_id=user.id))
        else:
            form = UserForm(instance=user)

        context = {"form": form}
        return render(request, "authentication/user.html", context=context)
    else:
        raise PermissionDenied


# def show_user_books(request, user_id):
#     if not request.user.is_active:
#         return redirect(reverse("authentication:login"))
#     if request.user.is_superuser or request.user.id == user_id:
#         user = User.get_by_id(user_id)
#         books = user.books.all()
#         context = {"books": books, "user_name": user.first_name, "filter": False}
#         return render(request, "book/books.html", context=context)
#     else:
#         return redirect(reverse("book:all_books"))


# def show_user_orders(request, user_id):
#     if not request.user.is_active:
#         return redirect(reverse("authentication:login"))
#     if request.user.is_superuser or request.user.id == user_id:
#         user = User.get_by_id(user_id)
#         orders = Order.objects.filter(user=user)
#         context = {"orders": orders}
#         return render(request, "order/orders.html", context=context)
#     else:
#         return redirect(reverse("authentication:home"))

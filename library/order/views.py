# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Order, Book, CustomUser
from .forms import OrderForm


def all_orders(request):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    if request.user.is_superuser:
        orders = Order.get_all()
        context = {"orders": orders}
        return render(request, "order/orders.html", context=context)
    else:
        return redirect(
            reverse("authentication:user_orders", kwargs={"user_id": request.user.id})
        )


def create_order(request):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))

    if request.method == "POST":
        book = Book.objects.filter(name=request.POST.get("title"))[0]
        user = CustomUser.get_by_email(request.POST.get("user_email"))
        plated_end_at = timezone.now() + timedelta(days=14)
        Order.create(user, book, plated_end_at)
        user.books.add(book)
        return redirect(reverse("order:all_orders"))


def close_order(request):
    if request.user.is_superuser:
        order_id = request.GET.get("order_id")
        order = Order.get_by_id(order_id)
        order.end_at = timezone.now()
        order.save()
        user = order.user
        user.books.remove(order.book)
        return redirect(reverse("order:all_orders"))
    

def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_order')
    else:
        form = OrderForm()
    return render(request, 'order/add_order.html', {'form': form})


def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('edit_order')
    else:
        form = OrderForm(instance=order)
    return render(request, 'order/edit_order.html', {'form': form})

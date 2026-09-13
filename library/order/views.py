from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from library.mixins import StaffRequiredMixin
from .models import Order
from book.models import Book
from authentication.models import User


class OrderListView(LoginRequiredMixin, ListView):
    """View to list all orders for staff and limits regular readers to their own orders."""

    model = Order
    template_name = "order/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = Order.objects.select_related("book__author", "user")

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        book_query = self.request.GET.get("book")
        if book_query:
            queryset = queryset.filter(book__title__icontains=book_query.strip())

        user_id = self.request.GET.get("user")
        if user_id and self.request.user.is_staff:
            user_id = user_id.strip()
            if user_id.isdigit():
                queryset = queryset.filter(user_id=int(user_id))
            else:
                queryset = queryset.none()

        status = self.request.GET.get("status")
        today = timezone.localdate()
        if status == "active":
            queryset = queryset.filter(end_at__isnull=True)
        elif status == "overdue":
            queryset = queryset.filter(end_at__isnull=True, planned_end_at__lt=today)
        elif status == "returned":
            queryset = queryset.filter(end_at__isnull=False)

        sort_mapping = {
            "created_desc": "-created_at",
            "created_asc": "created_at",
            "due_asc": "planned_end_at",
            "due_desc": "-planned_end_at",
            "returned_desc": "-end_at",
        }
        sort_by = self.request.GET.get("sort", "created_desc")
        return queryset.order_by(sort_mapping.get(sort_by, "-created_at"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_staff:
            context["users"] = User.objects.all()

        return context


class OrderCreateView(LoginRequiredMixin, View):
    """Handles order placement for logged-in users."""

    def post(self, request, book_id):

        book = get_object_or_404(Book, pk=book_id)

        if book.count <= 0:
            return redirect("book:book_detail", pk=book.id)

        Order.objects.create(user=request.user, book=book)
        book.count -= 1
        book.save(update_fields=["count"])

        return redirect("book:book_detail", pk=book.id)


class OrderCloseView(StaffRequiredMixin, View):
    """Closes an active order."""

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if not order.is_closed:
            order.end_at = timezone.localdate()
            order.save(update_fields=["end_at"])

            book = Book.objects.get(pk=order.book_id)
            book.count += 1
            book.save(update_fields=["count"])

        return redirect("order:order_list")

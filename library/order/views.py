from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from library.mixins import StaffRequiredMixin
from .models import Order
from book.models import Book
from .forms import OrderFilterForm


class OrderListView(LoginRequiredMixin, ListView):
    """View to list all orders for staff and limits regular readers to their own orders."""

    model = Order
    template_name = "order/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = Order.objects.select_related("book__author", "user")

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        self.filter_form = OrderFilterForm(
            self.request.GET or None, is_staff=self.request.user.is_staff
        )

        if not self.filter_form.is_valid():
            return queryset.order_by("-created_at")

        data = self.filter_form.cleaned_data

        if book := data.get("book"):
            queryset = queryset.filter(book__title__icontains=book)

        if self.request.user.is_staff and (user := data.get("user")):
            queryset = queryset.filter(user=user)

        if status := data.get("status"):
            now = timezone.now()
            if status == "active":
                queryset = queryset.filter(end_at__isnull=True)
            elif status == "overdue":
                queryset = queryset.filter(end_at__isnull=True, planned_end_at__lt=now)
            elif status == "returned":
                queryset = queryset.filter(end_at__isnull=False)

        sort_mapping = {
            "created_desc": ["-created_at"],
            "created_asc": ["created_at"],
            "due_asc": [F("planned_end_at").asc(nulls_last=True)],
            "due_desc": [F("planned_end_at").desc(nulls_last=True)],
            "returned_desc": [F("end_at").desc(nulls_last=True), "-created_at"],
        }
        ordering = sort_mapping.get(data.get("sort"), ["-created_at"])
        return queryset.order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
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

        messages.success(request, f"You have successfully borrowed '{book.title}'.")

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

            messages.success(
                request, f"Order #{order.pk} for '{book.title}' was marked as returned."
            )
        else:
            messages.info(request, f"Order #{order.pk} is already closed.")

        return redirect("order:order_list")

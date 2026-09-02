# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from library.mixins import StaffRequiredMixin
from .models import Order
from .forms import OrderCreateForm


class OrderListView(ListView):
    """View to list all orders for superusers, redirecting regular users to their own orders."""

    model = Order
    template_name = "order/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = Order.objects.select_related("book", "user")

        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = OrderCreateForm
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Handles order placement for logged-in users."""

    model = Order
    form_class = OrderCreateForm
    success_url = reverse_lazy("order:all_orders")
    failure_url = reverse_lazy("orders:all_orders")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect(self.failure_url)


class OrderCloseView(StaffRequiredMixin, View):
    """Closes an active order by setting the end date."""

    success_url = reverse_lazy("order:all_orders")

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if not order.end_at:
            order.end_at = timezone.localdate()
            order.save(update_fields=["end_at"])

        return redirect(self.success_url)

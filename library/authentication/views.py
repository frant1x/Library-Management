from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from library.mixins import StaffRequiredMixin
from .models import User
from .forms import RegistrationForm, LoginForm, UserProfileForm, StaffUserForm


class RegisterView(CreateView):
    """View for user registration."""

    form_class = RegistrationForm
    template_name = "authentication/register.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return redirect(self.get_success_url())


class CustomLoginView(LoginView):
    """View for user login."""

    template_name = "authentication/log_in.html"
    form_class = LoginForm
    redirect_authenticated_user = True


class UserListView(StaffRequiredMixin, ListView):
    """List of registered users accessible only to library staff."""

    model = User
    template_name = "authentication/users.html"
    context_object_name = "users"
    ordering = ["last_name", "first_name"]


class ProfileOrdersMixin:
    """Injects the target user's orders and active tab into the profile context."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.get_object()

        context["orders"] = target_user.orders.select_related("book__author").order_by(
            "end_at", "-created_at"
        )
        context["active_tab"] = self.request.GET.get("tab", "info")
        return context


class UserProfileView(LoginRequiredMixin, ProfileOrdersMixin, UpdateView):
    """View and update current authenticated user's profile."""

    model = User
    form_class = UserProfileForm
    template_name = "authentication/profile.html"
    success_url = reverse_lazy("authentication:auth_user")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.instance)
        return response


class UserUpdateView(StaffRequiredMixin, ProfileOrdersMixin, UpdateView):
    """Staff-only view to manage any user by primary key."""

    model = User
    form_class = StaffUserForm
    template_name = "authentication/profile.html"
    success_url = reverse_lazy("authentication:show_user")

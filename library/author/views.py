from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView
from library.mixins import StaffRequiredMixin
from .forms import AuthorForm
from .models import Author


class AuthorListView(ListView):
    """Displays a list of authors with form to add new authors for staff users."""

    model = Author
    template_name = "author/authors.html"
    context_object_name = "authors"
    ordering = ["last_name", "first_name"]


class AuthorCreateView(StaffRequiredMixin, CreateView):
    """View to handle author creation for authorized staff members."""

    model = Author
    form_class = AuthorForm
    template_name = "author/author_form.html"
    success_url = reverse_lazy("author:author_list")


class AuthorUpdateView(StaffRequiredMixin, UpdateView):
    """View to handle author updates for authorized staff members."""

    model = Author
    form_class = AuthorForm
    template_name = "author/author_form.html"
    success_url = reverse_lazy("author:author_list")

from django.db.models import Count
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from library.mixins import StaffRequiredMixin
from .forms import AuthorForm
from .models import Author


class AuthorListView(ListView):
    """Displays a list of authors with form to add new authors for staff users."""

    model = Author
    template_name = "author/authors.html"
    context_object_name = "authors"

    def get_queryset(self):
        return Author.objects.annotate(books_count=Count("books")).order_by(
            "last_name", "first_name"
        )


class AuthorCreateView(StaffRequiredMixin, CreateView):
    """View to handle author creation for authorized staff members."""

    model = Author
    form_class = AuthorForm
    template_name = "author/author_form.html"
    success_url = reverse_lazy("author:author_list")

    def form_valid(self, form):
        messages.success(
            self.request, f"Author '{form.instance}' was created successfully."
        )
        return super().form_valid(form)


class AuthorUpdateView(StaffRequiredMixin, UpdateView):
    """View to handle author updates for authorized staff members."""

    model = Author
    form_class = AuthorForm
    template_name = "author/author_form.html"
    success_url = reverse_lazy("author:author_list")

    def form_valid(self, form):
        messages.success(
            self.request, f"Author '{form.instance}' was updated successfully."
        )
        return super().form_valid(form)

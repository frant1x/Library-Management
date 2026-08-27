from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from library.mixins import StaffRequiredMixin
from .forms import AuthorForm
from .models import Author


class AuthorListView(ListView):
    model = Author
    template_name = "author/authors.html"
    context_object_name = "authors"
    ordering = ["last_name", "first_name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context["form"] = AuthorForm()
        return context


class AuthorCreateView(StaffRequiredMixin, CreateView):
    form_class = AuthorForm
    success_url = reverse_lazy("author:all_authors")
    failure_url = reverse_lazy("authors:all_authors")

    def form_invalid(self, form):
        return redirect(self.failure_url)


class AuthorEditView(StaffRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "author/edit_author.html"
    success_url = reverse_lazy("author:all_authors")


class AuthorDeleteView(StaffRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("author:all_authors")

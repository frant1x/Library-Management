from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from library.mixins import StaffRequiredMixin
from .models import Book
from .forms import BookForm, BookFilterForm


class BookListView(ListView):
    """Displays a list of books with optional GET filtering and search."""

    model = Book
    template_name = "book/books.html"
    context_object_name = "books"

    def get_queryset(self):
        queryset = Book.objects.select_related("author").order_by("title")
        self.filter_form = BookFilterForm(self.request.GET)

        if not self.filter_form.is_valid():
            return queryset

        data = self.filter_form.cleaned_data

        if title := data.get("title"):
            queryset = queryset.filter(title__icontains=title)

        if author := data.get("author"):
            queryset = queryset.filter(author=author)

        if (count_min := data.get("count_min")) is not None:
            queryset = queryset.filter(count__gte=count_min)

        if (count_max := data.get("count_max")) is not None:
            queryset = queryset.filter(count__lte=count_max)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        return context


class BookCreateView(StaffRequiredMixin, CreateView):
    """View to handle book creation for authorized staff members."""

    model = Book
    form_class = BookForm
    template_name = "book/book_form.html"
    success_url = reverse_lazy("book:book_list")

    def form_valid(self, form):
        messages.success(
            self.request, f"Book '{form.instance.title}' was created successfully."
        )
        return super().form_valid(form)


class BookDetailView(DetailView):
    """Renders detailed information for a single book instance."""

    model = Book
    template_name = "book/book.html"
    context_object_name = "book"

    def get_queryset(self):
        return Book.objects.select_related("author")


class BookUpdateView(StaffRequiredMixin, UpdateView):
    """Handles book updates for authorized staff members."""

    model = Book
    form_class = BookForm
    template_name = "book/book_form.html"

    def get_success_url(self):
        return reverse_lazy("book:book_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(
            self.request, f"Book '{form.instance.title}' was updated successfully."
        )
        return super().form_valid(form)

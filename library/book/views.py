from django.urls import reverse_lazy
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
        """Build and filter the book queryset based on validated GET parameters."""
        queryset = Book.objects.select_related("author").order_by("title")
        self.filter_form = BookFilterForm(self.request.GET)

        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data

            if title := data.get("title"):
                queryset = queryset.filter(title__icontains=title)

            if author := data.get("author"):
                queryset = queryset.filter(author=author)

            if (count_min := data.get("count_min")) is not None:
                queryset = queryset.filter(count__gte=int(count_min))

            if (count_max := data.get("count_max")) is not None:
                queryset = queryset.filter(count__lte=count_max)

        return queryset

    def get_context_data(self, **kwargs):
        """Inject the bound filter form and active filter status into the template context."""
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        context["is_filtered"] = any(
            self.request.GET.get(param)
            for param in ["title", "author", "count_min", "count_max"]
        )
        return context


class BookCreateView(StaffRequiredMixin, CreateView):
    """View to handle book creation for authorized staff members."""

    model = Book
    form_class = BookForm
    template_name = "book/add_book.html"
    success_url = reverse_lazy("book:all_books")


class BookDetailView(DetailView):
    """Renders detailed information for a single book instance."""

    model = Book
    template_name = "book/book.html"
    context_object_name = "book"

    def get_queryset(self):
        """Pre-fetch author relation to avoid extra database hits."""
        return Book.objects.select_related("author")


class BookUpdateView(StaffRequiredMixin, UpdateView):
    """Handles book updates for authorized staff members."""

    model = Book
    form_class = BookForm
    template_name = "book/edit_book.html"
    success_url = reverse_lazy("book:all_books")

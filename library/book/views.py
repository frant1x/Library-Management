# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Book
from author.models import Author
from .forms import BookForm


def all_books(request):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    books = Book.get_all()
    context = {"books": books, "filter": False}
    return render(request, "book/books.html", context=context)


def specific_book(request, book_id):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    book = Book.get_by_id(book_id)
    context = {"book": book}
    return render(request, "book/book.html", context=context)


def filter_books(request):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))

    if request.method == "POST":
        filter_conditions = {}

        if request.POST.get("title") != "":
            title = request.POST.get("title")
            filter_conditions["name__icontains"] = title

        if request.POST.get("author") != "":
            author_name, author_surname = request.POST.get("author").split()
            author_conditions = {"name": author_name, "surname": author_surname}
            author = Author.objects.filter(**author_conditions)[0]
            filter_conditions["authors"] = author.id

        if request.POST.get("count_min") != "":
            count_min = request.POST.get("count_min")
            filter_conditions["count__gte"] = count_min

        if request.POST.get("count_max") != "":
            count_max = request.POST.get("count_max")
            filter_conditions["count__lte"] = count_max

        books = Book.objects.filter(**filter_conditions)
        context = {"books": books, "filter": True}
        return render(request, "book/books.html", context=context)


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_book')
    else:
        form = BookForm()
    return render(request, 'book/add_book.html', {'form': form})


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('edit_book')
    else:
        form = BookForm(instance=book)
    return render(request, 'book/edit_book.html', {'form': form})

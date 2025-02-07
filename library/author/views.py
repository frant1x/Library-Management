# Create your views here.
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import AuthorForm
from .models import Author


def all_authors(request):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    authors = Author.get_all()
    form = AuthorForm()
    context = {"authors": authors, "form": form}
    return render(request, "author/authors.html", context=context)


def create_author(request):
    if request.method == "POST":
        if request.user.is_superuser:
            form = AuthorForm(request.POST)
            if form.is_valid():
                form.save()
        return redirect(reverse("author:all_authors"))


def edit_author(request, author_id):
    if not request.user.is_active:
        return redirect(reverse("authentication:login"))
    author = Author.get_by_id(author_id)
    if request.method == "POST":
        if request.user.is_superuser:
            form = AuthorForm(request.POST, instance=author)
            if form.is_valid():
                form.save()
        return redirect(reverse("author:all_authors"))
    form = AuthorForm(instance=author)
    return render(request, "author/edit_author.html", {"form": form})


def delete_author(request, author_id):
    if request.user.is_superuser:
        Author.delete_by_id(author_id)
    return redirect(reverse("author:all_authors"))

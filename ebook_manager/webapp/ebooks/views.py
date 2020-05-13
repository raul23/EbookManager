from django.http import Http404, HttpResponse
from django.shortcuts import render

from .models import Book


def index(request):
    latest_book_list = Book.objects.order_by('-add_date')[:3]
    context = {'latest_book_list': latest_book_list}
    return render(request, 'ebooks/index.html', context)


def book_detail(request, book_id):
    if book_id.isalpha():
        raise Http404("Book does not exist")
    return HttpResponse("You're looking at book %s." % book_id)


def book_ratings(request, book_id):
    response = "You're looking at the ratings of %s."
    return HttpResponse(response % book_id)


def rate(request, book_id):
    return HttpResponse("You're rating the book %s." % book_id)

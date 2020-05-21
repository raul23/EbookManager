from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Book, Rating


def index(request):
    latest_book_list = Book.objects.order_by('-add_date')[:3]
    context = {'latest_book_list': latest_book_list}
    return render(request, 'ebooks/index.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'ebooks/book_detail.html', {'book': book})


def book_ratings(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'ebooks/book_ratings.html', {'book': book})


def rate(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    try:
        user_rating = float(request.POST['rating'])
        rating_obj = book.rating_set.get(source='P')
    except (KeyError, ValueError):
        # ValueError if no rating ('', empty string)
        # Redisplay the book rating form
        return render(request, 'ebooks/book_detail.html', {
            'book': book,
            'error_message': "You didn't rate the book.",
        })
    except Rating.DoesNotExist:
        Rating.objects.create(book=book,
                              source='P',
                              avg_rating=user_rating,
                              nb_ratings=1)
    else:
        total_ratings = rating_obj.avg_rating * rating_obj.nb_ratings
        new_avg_rating = (total_ratings + user_rating) / (rating_obj.nb_ratings + 1)
        rating_obj.avg_rating = new_avg_rating
        rating_obj.nb_ratings += 1
        rating_obj.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(
        reverse('ebooks:book_ratings', args=(book.book_id,)))

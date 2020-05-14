from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Book


def index(request):
    latest_book_list = Book.objects.order_by('-add_date')[:3]
    context = {'latest_book_list': latest_book_list}
    return render(request, 'ebooks/index.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'ebooks/book_detail.html', {'book': book})


def book_ratings(request, book_id):
    response = "You're looking at the ratings of %s."
    return HttpResponse(response % book_id)


def rate(request, book_id):
    import ipdb
    ipdb.set_trace()
    book = get_object_or_404(Book, pk=book_id)
    try:
        rating = request.POST['rating']
    except (KeyError, Book.DoesNotExist):
        # Redisplay the book rating form.
        """
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
        """
        pass
    else:
        # selected_choice.votes += 1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        pass

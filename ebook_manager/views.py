from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .apps import EbookManagerConfig
from .models import Author, Book, Rating
from .utils.file_processor import FileProcessor

app_name = EbookManagerConfig.name


class IndexView(generic.ListView):
    template_name = '{}/index.html'.format(app_name)
    # For ListView,
    # NOTE 1: autogenerated default template name is
    # <label name>/<model name>_list.html
    # NOTE 2: automatically generated context variable
    context_object_name = 'book_list'

    def get_queryset(self):
        # """Return the last three added books."""
        # return Book.objects.order_by('-add_date')[:3]
        return Book.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "{}/author_detail.html".format(app_name)
    slug_field = "name"
    # slug_url_kwarg = 'author_name'


class BookDetailView(generic.DetailView):
    model = Book
    # For DetailView,
    # NOTE 1: autogenerated default template name is
    # <label name>/<model name>_detail.html
    # NOTE 2: automatically generated context variable is book
    template_name = "{}/book_detail.html".format(app_name)


class BookRatingsView(generic.DetailView):
    model = Book
    template_name = '{}/book_ratings.html'.format(app_name)


def rate(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    try:
        user_rating = float(request.POST['rating'])
        rating_obj = book.rating_set.get(source='P')
    except (KeyError, ValueError):
        # ValueError if no rating ('', empty string)
        # Redisplay the book rating form
        return render(request, '{}/book_detail.html'.format(app_name), {
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
        reverse('{}:book_ratings'.format(app_name), args=(book.book_id,)))


def upload_files(request):
    import ipdb
    ipdb.set_trace()
    tmp_files = request.FILES.getlist('files')
    for tmpf in tmp_files:
        # Process file
        FileProcessor(tmpf, **EbookManagerConfig.file_processor_cfg).start_processing()

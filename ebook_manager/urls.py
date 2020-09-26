from django.http import Http404
from django.urls import path, re_path

from . import apps, views


def response_error_handler(request):
    raise Http404("Not found: {}".format(request.get_full_path_info()))


app_name = apps.EbookManagerConfig.name
label = apps.EbookManagerConfig.label
urlpatterns = [
    # ex: /ebook-manager/upload_files/
    path('{}/upload_files/'.format(label), views.upload_files, name='upload_files'),
    # ex: /ebook-manager/
    # the 'name' value as called by the {% url %} template tag
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^{}/$'.format(label), views.IndexView.as_view(), name='index'),
    path('{}/author/'.format(label), response_error_handler),
    path('{}/book/'.format(label), response_error_handler),
    # ex: /ebook-manager/123456790/
    # TODO: slug?
    path('{}/book/<slug:pk>/'.format(label), views.BookDetailView.as_view(),
         name='book_detail'),
    # ex: /ebook-manager/123456790/ratings/
    path('{}/book/<slug:pk>/ratings/'.format(label), views.BookRatingsView.as_view(),
         name='book_ratings'),
    # ex: /ebook-manager/123456790/rate/
    path('{}/book/<slug:book_id>/rate/'.format(label), views.rate, name='rate'),
    path('{}/author/<slug>/'.format(label), views.AuthorDetailView.as_view(),
         name='author-detail'),
]

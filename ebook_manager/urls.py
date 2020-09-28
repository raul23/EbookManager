from django.http import Http404
from django.urls import path, re_path

from . import apps, views


def response_error_handler(request, msg=None):
    if msg:
        raise Http404(msg)
    else:
        raise Http404("Not found: {}".format(request.get_full_path_info()))


app_name = apps.EbookManagerConfig.name
label = apps.EbookManagerConfig.label
urlpatterns = [
    # ex: /ebook-manager/
    # the 'name' value as called by the {% url %} template tag
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^{}/$'.format(label), views.IndexView.as_view(), name='index'),
    # ex: /ebook-manager/author/ -> 404 error
    path('{}/author/'.format(label), response_error_handler),
    # ex: /ebook-manager/author/john-doe/
    path('{}/author/<slug:slug_name>/'.format(label),
         views.AuthorDetailView.as_view(),
         name='author_detail'),
    # ex: /ebook-manager/book/ -> 404 error
    path('{}/book/'.format(label), response_error_handler),
    # ex: /ebook-manager/book/123456790/
    path('{}/book/<slug:pk>/'.format(label), views.BookDetailView.as_view(),
         name='book_detail'),
    # ex: /ebook-manager/book/123456790/ratings/
    path('{}/book/<slug:pk>/ratings/'.format(label),
         views.BookRatingsView.as_view(),
         name='book_ratings'),
    # ex: /ebook-manager/123456790/rate/
    path('{}/book/<slug:book_id>/rate/'.format(label), views.rate, name='rate'),
    # ex: /ebook-manager/upload_ebooks/
    path('{}/upload-ebooks/'.format(label), views.UploadEbooksView.as_view(),
         name='upload_ebooks'),
    # ex: /ebook-manager/upload_ebooks/uploading
    path('{}/upload-ebooks/uploading/'.format(label), views.upload_ebooks,
         name='upload_submit_form'),
]

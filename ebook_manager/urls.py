from django.urls import path, re_path

from . import apps, views


app_name = apps.EbookManagerConfig.name
label = apps.EbookManagerConfig.label
# app_name = label
urlpatterns = [
    # ex: /ebook-manager/add_files/
    path('{}/upload_files/'.format(label), views.upload_files, name='upload_files'),
    # ex: /ebook-manager/
    # the 'name' value as called by the {% url %} template tag
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^{}/$'.format(label), views.IndexView.as_view(), name='index'),
    # ex: /ebook-manager/123456790/
    # TODO: slug?
    path('{}/<slug:pk>/'.format(label),  # route
         views.BookDetailView.as_view(),    # view
         name='book_detail'),
    # ex: /ebook-manager/123456790/ratings/
    path('{}/<slug:pk>/ratings/'.format(label),  # route
         views.BookRatingsView.as_view(),           # view
         name='book_ratings'),
    # ex: /ebook-manager/123456790/rate/
    path('{}/<slug:book_id>/rate/'.format(label), views.rate, name='rate'),
]

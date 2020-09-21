from django.urls import path, re_path

from . import apps, views


app_name = apps.EbooksConfig.name
urlpatterns = [
    # ex: /ebooks/add_files/
    path('{}/upload_files/'.format(app_name), views.upload_files, name='upload_files'),
    # ex: /ebooks/
    # the 'name' value as called by the {% url %} template tag
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^{}/$'.format(app_name), views.IndexView.as_view(), name='index'),
    # ex: /ebooks/123456790/
    # TODO: slug?
    path('{}/<slug:pk>/'.format(app_name),  # route
         views.BookDetailView.as_view(),    # view
         name='book_detail'),
    # ex: /ebooks/123456790/ratings/
    path('{}/<slug:pk>/ratings/'.format(app_name),  # route
         views.BookRatingsView.as_view(),           # view
         name='book_ratings'),
    # ex: /ebooks/123456790/rate/
    path('{}/<slug:book_id>/rate/'.format(app_name), views.rate, name='rate'),
]

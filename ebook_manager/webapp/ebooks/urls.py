from django.urls import path

from . import apps, views


app_name = apps.EbooksConfig.name
urlpatterns = [
    # ex: /ebooks/
    # the 'name' value as called by the {% url %} template tag
    path('', views.IndexView.as_view(), name='index'),
    path('{}/'.format(app_name), views.IndexView.as_view(), name='index'),
    # ex: /ebooks/123456790/
    # TODO: slug?
    path('{}/<slug:pk>/'.format(app_name),
         views.BookDetailView.as_view(),
         name='book_detail'),
    # ex: /ebooks/123456790/ratings/
    path('{}/<slug:pk>/ratings/'.format(app_name),
         views.BookRatingsView.as_view(),
         name='book_ratings'),
    # ex: /ebooks/123456790/rate/
    path('{}/<slug:book_id>/rate/'.format(app_name), views.rate, name='rate'),
]

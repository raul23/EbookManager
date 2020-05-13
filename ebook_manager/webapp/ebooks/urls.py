from django.urls import path

from . import apps, views


app_name = apps.EbooksConfig.name
urlpatterns = [
    # ex: /ebooks/
    # the 'name' value as called by the {% url %} template tag
    path('', views.index, name='index'),
    path('{}/'.format(app_name), views.index, name='index'),
    # ex: /ebooks/123456790/
    path('{}/<slug:book_id>/'.format(app_name),
         views.book_detail,
         name='book_detail'),
    # ex: /ebooks/123456790/ratings/
    path('{}/<slug:book_id>/ratings/'.format(app_name),
         views.book_ratings,
         name='book_ratings'),
    # ex: /ebooks/123456790/rate/
    path('{}/<slug:book_id>/rate/'.format(app_name), views.rate, name='rate'),
]

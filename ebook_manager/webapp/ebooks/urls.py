from django.urls import path

from . import views


urlpatterns = [
    # ex: /ebooks/
    path('', views.index, name='index'),
    path('ebooks/', views.index, name='index'),
    # ex: /ebooks/123456790/
    path('<slug:book_id>/', views.book_detail, name='detail'),
    # ex: /ebooks/123456790/ratings/
    path('<slug:book_id>/ratings/', views.book_ratings, name='ratings'),
    # ex: /ebooks/123456790/rate/
    path('<slug:book_id>/rate/', views.rate, name='rate'),
]

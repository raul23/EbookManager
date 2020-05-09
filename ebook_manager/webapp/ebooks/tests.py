from django.test import TestCase


# Create your tests here.
def debug_code():
    from ebooks.models import Author, Book, Rating, Tag, Category
    from django.utils import timezone

    b = Book(title="The Road", pub_date=timezone.now())
    b.pages = 30
    b.save()

    # Create authors
    b.author_set.create(first_name="John", last_name="Doe")
    b.author_set.create(first_name="James", last_name="King")
    b.author_set.create(first_name="Francisco", last_name="Gomez")

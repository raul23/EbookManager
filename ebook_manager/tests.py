from django.db import models
from django.test import TestCase

from .models import Book


class BookModelTests(TestCase):
    def test_book_creation_with_required_values_only(self):
        """TODO

        Returns
        -------

        """
        required_fields = {'book_id': '039333810X',
                           'book_id_type': 'ISBN',
                           'title': "Test title",
                           'pages': 1}
        book = Book(**required_fields)
        msg_empty = "{} should be an empty string by default"
        msg_none = "{} should be None by default"
        for field in book._meta.fields:
            if field.name not in required_fields and field.has_default():
                field_value = getattr(book, field.name, None)
                if isinstance(field, models.fields.files.ImageField):
                    field_value = None
                if field.default == '':
                    self.assertIs(field_value, "", msg_empty.format(field.name))
                elif field.default is None:
                    self.assertIsNone(field_value, msg_none.format(field.name))
        # After the clean, new values for some non-required fields, e.g. asin
        book.full_clean()

    def test_book_id_as_asin(self):
        book = Book(book_id='B07ZG18BH3',
                    book_id_type='ASIN',
                    title='Effective Python: 90 Specific Ways to Write Better '
                          'Python (2nd Edition)')
        book.full_clean()
        self.assertEqual(book.book_id,
                         book.asin,
                         "The 'asin' field is not equal to {}".format(book.book_id))

    def test_book_id_as_isbn10(self):
        book = Book(book_id='1491985577',
                    book_id_type='ISBN',
                    title='Web Scraping with Python')
        book.full_clean()
        self.assertEqual(book.book_id,
                         book.isbn10,
                         "The isbn10 field is not equal to {}".format(book.book_id))
        self.assertIsNot(book.isbn13, "", "The isbn13 field is empty")

    def test_book_id_as_isbn13(self):
        book = Book(book_id='9780134853987',
                    book_id_type='ISBN',
                    title='Effective Python: 90 Specific Ways to Write Better '
                          'Python (2nd Edition)')
        book.full_clean()
        self.assertEqual(book.book_id,
                         book.isbn13,
                         "The isbn13 field is not equal to {}".format(book.book_id))
        self.assertIsNot(book.isbn10, "", "The isbn10 field is empty")

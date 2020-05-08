from django.core.validators import RegexValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    series = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    # TODO:
    # - For isbn10 and isbn13, try to use a MaxValueValidator instead of a
    # CharField as explained in https://stackoverflow.com/a/30850101
    #
    # - Also test with PositiveIntegerField, though django doc says that 'Values
    # from 0 to 2147483647 are safe in all databases supported by Django'
    # Ref.: https://bit.ly/2YGsxAI
    isbn10 = models.CharField(max_length=10,
                              validators=[RegexValidator(r'^\d{1,10}$')])
    isbn13 = models.CharField(max_length=13,
                              validators=[RegexValidator(r'^\d{1,10}$')])
    pub_date = models.DateTimeField('Date published')


class Author(models.Model):
    books = models.ManyToManyField(Book)

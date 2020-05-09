from django.core.validators import RegexValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    series = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')
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
    pages = models.IntegerField()
    # Size is given in multiples of bytes, and the unit symbol is shown beside
    # the file size, e.g. 660 KB
    size = models.CharField(max_length=10)
    format = models.CharField(max_length=10)
    md5 = models.CharField(max_length=32)
    sha256 = models.CharField(max_length=64)
    add_date = models.DateTimeField('Date added')
    update_date = models.DateTimeField('Date updated')
    # TODO: ImageField required the Pillow library
    thumbnail_cover_image = models.ImageField()
    enlarged_cover_image = models.ImageField()


class Author(models.Model):
    books = models.ManyToManyField(Book)


class Rating(models.Model):
    # TODO: primary key is (book_id, source)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    source = models.CharField('Source of rating', max_length=200)
    # TODO: FloatField instead of DecimalField?,
    # see https://docs.djangoproject.com/en/3.0/ref/models/fields/#floatfield
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    nb_ratings = models.PositiveIntegerField('Number of ratings')
    update_date = models.DateTimeField('Date updated')


class Tags(models.Model):
    books = models.ManyToManyField(Book)
    source = models.CharField('Source of tag', max_length=200)


class Categories(models.Model):
    books = models.ManyToManyField(Book)
    source = models.CharField('Source of category', max_length=200)



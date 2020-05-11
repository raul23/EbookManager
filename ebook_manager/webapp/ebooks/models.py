from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Book(models.Model):

    class TypeOfBookId(models.TextChoices):
        ISBN10 = 'I10'
        ISBN13 = 'I13'
        ASIN = 'A'

    class BookFormat(models.TextChoices):
        Hardcover = 'H'
        Paperback = 'P'

    # Primary key, e.g. ISBN-10 or ASIN
    book_id = models.CharField(max_length=13,
                               default="",
                               blank=True,
                               primary_key=True)
    id_type = models.CharField('Type of Book Id',
                               max_length=10,
                               choices=TypeOfBookId.choices)
    # Title is required
    title = models.CharField(max_length=200)
    series = models.CharField(max_length=200, default="", blank=True)
    publisher = models.CharField(max_length=200, default="", blank=True)
    pub_date = models.DateTimeField('Date published',
                                    default=None,
                                    blank=True,
                                    null=True)
    pages = models.IntegerField(default=None, blank=True, null=True)
    language = models.CharField(max_length=50, default="", blank=True)
    # Book format. For example, hardcover and paperback
    book_format = models.CharField(max_length=10,
                                   default="",
                                   blank=True,
                                   choices=BookFormat.choices)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)
    # TODO: ImageField required the Pillow library
    thumbnail_cover_image = models.ImageField(default=None, blank=True)
    enlarged_cover_image = models.ImageField(default=None, blank=True)

    def __str__(self):
        return self.title


class BookFile(models.Model):
    # Automatic primary key
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    pages = models.IntegerField(default=None, blank=True, null=True)
    # Size is given in multiples of bytes, and the unit symbol is shown beside
    # the file size, e.g. 660 KB
    size = models.CharField(max_length=10, default="", blank=True)
    # File extension. For example, PDF, EPUB, or MOBI
    extension = models.CharField(max_length=10, default="", blank=True)
    # md5 and sha256 are in hexadecimal
    # TODO: test that md5 and sha256 should be unique
    md5 = models.CharField(max_length=32,
                           default="",
                           blank=True)
    sha256 = models.CharField(max_length=64, default="", blank=True, unique=True)
    # TODO: Should file_path be CharField with max_length (but what)?
    file_path = models.TextField()
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)
    thumbnail_cover_image = models.ImageField(default=None, blank=True)
    enlarged_cover_image = models.ImageField(default=None, blank=True)


class Author(models.Model):
    # TODO: test primary key if automatic set
    books = models.ManyToManyField(Book, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Category(models.Model):

    class Meta:
        unique_together = (("category", "source"),)
        verbose_name_plural = "categories"

    books = models.ManyToManyField(Book, blank=True)
    # TODO: check that category is unique
    category = models.CharField(max_length=200, unique=True)
    # TODO: add choices such as amazon, goodreads, personal
    source = models.CharField('Source of category', max_length=200)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return self.category


class Rating(models.Model):

    class SourceOfRating(models.TextChoices):
        AMAZON = 'A'
        GOODREADS = 'G'
        PERSONAL = 'P'

    # TODO: primary key is (book_id, source)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # TODO: add choices such as amazon, goodreads
    source = models.CharField('Source of rating',
                              max_length=200,
                              primary_key=True)
    # TODO: FloatField instead of DecimalField?,
    # see https://docs.djangoproject.com/en/3.0/ref/models/fields/#floatfield
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(Decimal('1')),
                    MaxValueValidator(Decimal('5'))])
    nb_ratings = models.PositiveIntegerField('Number of ratings')
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{}: {}/5 [{}]".format(self.book.title, self.rating, self.source)


class Tag(models.Model):

    class SourceOfTag(models.TextChoices):
        AMAZON = 'A'
        GOODREADS = 'G'
        PERSONAL = 'P'

    class Meta:
        unique_together = (("tag", "source"),)

    books = models.ManyToManyField(Book, blank=True)
    # TODO: check tag is unique
    tag = models.CharField(max_length=200, unique=True)
    # TODO: add choices such as amazon, personal
    source = models.CharField('Source of tag',
                              max_length=200,
                              choices=SourceOfTag.choices)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} [{}]".format(self.tag, self.get_source_display())

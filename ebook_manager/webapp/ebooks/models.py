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
    # TODO: change to id
    book_id = models.CharField(max_length=13,
                               default="",
                               blank=True,
                               primary_key=True)
    # TODO: based on type of book id, check that the book id is valid
    # Required field
    id_type = models.CharField('Type of Book Id',
                               max_length=10,
                               choices=TypeOfBookId.choices)
    # Required field
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
        return "{} [{}]".format(self.title, self.book_id)


class BookFile(models.Model):

    class Meta:
        unique_together = (("book", "md5", "file_path"), ("md5", "file_path"),)

    # Automatic primary key
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    pages = models.IntegerField(default=None, blank=True, null=True)
    # Size is given in multiples of bytes, and the unit symbol is shown beside
    # the file size, e.g. 660 KB
    size = models.CharField(max_length=10, default="", blank=True)
    # File extension. For example, PDF, EPUB, or MOBI
    extension = models.CharField(max_length=10, default="", blank=True)
    # Required fields
    # md5 and sha256 are in hexadecimal
    md5 = models.CharField(max_length=32)
    sha256 = models.CharField(max_length=64)
    # TODO: Should file_path be CharField with max_length (but what)?
    # Required field
    file_path = models.TextField()
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)
    thumbnail_cover_image = models.ImageField(default=None, blank=True)
    enlarged_cover_image = models.ImageField(default=None, blank=True)

    def __str__(self):
        return "{} [{}]: {}".format(self.book.title,
                                    self.book.book_id,
                                    self.file_path)


class Author(models.Model):
    # TODO: test primary key if automatic set
    books = models.ManyToManyField(Book, blank=True)
    # Required fields
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Category(models.Model):

    class SourceOfCategory(models.TextChoices):
        AMAZON = 'A'
        GOODREADS = 'G'
        PERSONAL = 'P'
        WIKIPEDIA = 'W'

    class Meta:
        unique_together = (("category", "source"),)
        verbose_name_plural = "categories"

    books = models.ManyToManyField(Book, blank=True)
    # TODO: check that category is unique
    category = models.CharField(max_length=200)
    # TODO: add choices such as amazon, goodreads, personal
    source = models.CharField('Source of category',
                              max_length=200,
                              choices=SourceOfCategory.choices)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} [{}]".format(self.category, self.get_source_display())


class Rating(models.Model):

    class SourceOfRating(models.TextChoices):
        AMAZON = 'A'
        GOODREADS = 'G'
        PERSONAL = 'P'

    class Meta:
        unique_together = (("book", "source"),)

    # TODO: primary key is (book_id, source)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # TODO: add choices such as amazon, goodreads
    source = models.CharField('Source of rating',
                              max_length=200,
                              choices=SourceOfRating.choices)
    # TODO: FloatField instead of DecimalField?,
    # see https://docs.djangoproject.com/en/3.0/ref/models/fields/#floatfield
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(Decimal('1')),
                    MaxValueValidator(Decimal('5'))])
    nb_ratings = models.PositiveIntegerField('Number of ratings')
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{}: {}/5, {} ratings [{}]".format(self.book.title,
                                                  self.rating,
                                                  self.nb_ratings,
                                                  self.get_source_display())


class Tag(models.Model):

    class SourceOfTag(models.TextChoices):
        AMAZON = 'A'
        GOODREADS = 'G'
        PERSONAL = 'P'

    class Meta:
        unique_together = (("tag", "source"),)

    books = models.ManyToManyField(Book, blank=True)
    # TODO: check tag is unique
    tag = models.CharField(max_length=200)
    # TODO: add choices such as amazon, personal
    source = models.CharField('Source of tag',
                              max_length=200,
                              choices=SourceOfTag.choices)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} [{}]".format(self.tag, self.get_source_display())

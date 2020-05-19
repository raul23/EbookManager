import os
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    RegexValidator)
from django.db import models

from . import filtered_iso_639_languages


def validate_ebook_file(filepath):
    # Check that the file exists
    if os.path.exists(filepath):
        # Check that it is a file and not a directory
        if os.path.isfile(filepath):
            # Check that it is a valid ebook file, i.e. valid extension
            # TODO: check scripts.tools._split_fname()
            root, ext = os.path.splitext(filepath)
            ext = ext[1:]
            if ext not in BookFile.allowed_extensions:
                # TODO: ugettext_lazy as _ (like in languages module)?
                raise ValidationError(
                    '{} is not a valid ebook file extension. Allowed '
                    'extensions: {}'.format(ext, BookFile.allowed_extensions)
                )
        else:
            raise ValidationError('Not a file: {}'.format(filepath))
    else:
        raise ValidationError("File doesn't exist: {}".format(filepath))


def validate_positive_number(value):
    if value <= 0:
        raise ValidationError('Ensure this value is greater than 0.')


class AbstractBook(models.Model):
    # TODO: check if better way than repeat type
    type_of_book_id = [(t, t) for t in ['ASIN', 'ISBN10', 'ISBN13']]

    class Meta:
        abstract = True

    # TODO:
    # - isbn10 can be converted to isbn13, see https://bit.ly/3bxdP1y [Wikipedia]
    # - validate book identifiers
    book_id = models.CharField('Book Identifier (e.g. ISBN-10 or ASIN)',
                               max_length=20)
    # TODO: based on type of book id, check that the book id is valid
    book_id_type = models.CharField('Type of Book Identifier',
                                    max_length=10,
                                    choices=type_of_book_id)
    # Title is required
    title = models.CharField(max_length=200)
    # TODO: get edition too
    series = models.CharField(max_length=200, default="", blank=True)
    publisher = models.CharField(max_length=200, default="", blank=True)
    pub_year = models.PositiveIntegerField(
        'Year published',
        default=None,
        null=True,
        blank=True,
        validators=[MinValueValidator(1000),
                    MaxValueValidator(datetime.now().year + 1)],
        help_text="Use the following format: YYYY")
    # NOTE: isbn10, isbn, and asin are required and readonly (see admin.py)
    #
    # TODO:
    # - For isbn10 and isbn13, try to use a MaxValueValidator instead of a
    # CharField as explained in https://stackoverflow.com/a/30850101
    #
    # - Also test with PositiveIntegerField, though django doc says that 'Values
    # from 0 to 2147483647 are safe in all databases supported by Django'
    # Ref.: https://bit.ly/2YGsxAI
    #
    # - Test these fields' validators even though editable is False
    isbn10 = models.CharField('ISBN-10',
                              max_length=10,
                              validators=[RegexValidator(r'^\d{1,10}$')],
                              default="",
                              blank=True)
    isbn13 = models.CharField('ISBN-13',
                              max_length=13,
                              validators=[RegexValidator(r'^\d{1,10}$')],
                              default="",
                              blank=True)
    # TODO: add validators for asin
    asin = models.CharField('ASIN', max_length=10, default="", blank=True)
    # pages > 0
    pages = models.IntegerField(default=None,
                                null=True,
                                blank=True,
                                validators=[validate_positive_number])
    language = models.CharField(max_length=100,
                                default="",
                                blank=True,
                                choices=filtered_iso_639_languages.LANGUAGES)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)
    # TODO: ImageField requires the Pillow library
    # TODO: test images are loaded
    thumbnail_cover_image = models.ImageField(upload_to='cover_images',
                                              default=None,
                                              blank=True)
    enlarged_cover_image = models.ImageField(upload_to='cover_images',
                                             default=None,
                                             blank=True)


class Book(AbstractBook):

    class BookFormat(models.TextChoices):
        Hardcover = 'H'
        Kindle = 'K'
        Paperback = 'P'

    # NOTE: Automatic primary key
    # Book format is required
    # For example, hardcover and paperback
    book_format = models.CharField(max_length=10,
                                   default="",
                                   blank=True,
                                   choices=BookFormat.choices)

    def __str__(self):
        if self.book_id:
            return "{} [{}]".format(self.title, self.book_id)
        else:
            return self.title


class BookFile(AbstractBook):
    # TODO: extensions already found in scripts/tools.py
    allowed_extensions = ('azw', 'azw3', 'cbz', 'chm', 'djvu', 'docx', 'epub',
                          'gz', 'mobi', 'pdf', 'rar', 'zip',)

    class Meta:
        # TODO: test combinations
        unique_together = (("md5", "file_path"),)

    # Automatic primary key
    # book is required field
    # TODO: test on_delete
    books = models.ManyToManyField(Book, blank=True)
    # TODO: Should file_path be CharField with max_length (but what)?
    # file_path is required field
    file_path = models.TextField(validators=[validate_ebook_file])
    # Size is given in multiples of bytes, and the unit symbol is shown beside
    # the file size, e.g. 660 KB
    # TODO: should be IntegerField
    size = models.CharField('File size',
                            max_length=10,
                            default="MB",
                            editable=False)
    size_unit = models.CharField('Size unit',
                                 max_length=2,
                                 default="MB",
                                 editable=False)
    # md5 and sha256 are in hexadecimal
    # TODO: validate these two fields
    md5 = models.CharField('MD5', max_length=32, default="")
    sha256 = models.CharField('SHA256', max_length=64, default="")

    def __str__(self):
        return "{} [{}]: {}".format(self.title,
                                    self.book_id,
                                    self.file_path)


class Author(models.Model):
    # TODO: test primary key if set automatic
    books = models.ManyToManyField(Book, blank=True)
    # Required fields
    name = models.CharField(max_length=200)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return self.name


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
    source = models.CharField('Source of category',
                              max_length=200,
                              choices=SourceOfCategory.choices)
    # Automatic fields
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

    # TODO: primary key is (book_id, source)?
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    source = models.CharField('Source of rating',
                              max_length=200,
                              choices=SourceOfRating.choices)
    # TODO: FloatField instead of DecimalField?,
    # see https://docs.djangoproject.com/en/3.0/ref/models/fields/#floatfield
    # 1 <= avg_rating <= 1
    avg_rating = models.FloatField(
        'Average rating',
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)])
    # nb_ratings >= 0
    nb_ratings = models.PositiveIntegerField('Number of ratings',
                                             validators=[MinValueValidator(1)])
    # Automatic fields
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{}: {}/5, {} ratings [{}]".format(self.book.title,
                                                  self.avg_rating,
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
    # Automatic fields
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} [{}]".format(self.tag, self.get_source_display())

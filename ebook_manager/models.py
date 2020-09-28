import os
import re
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models.signals import m2m_changed
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.template.defaultfilters import slugify

import pyisbn

from .data import filtered_iso_639_languages


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


class UniqueErrorMessage(models.Model):
    class Meta:
        abstract = True

    def unique_error_message(self, model_class, unique_check):
        error = super(UniqueErrorMessage, self).unique_error_message(
            model_class, unique_check)
        if len(unique_check) > 1:
            name_value = []
            for n in unique_check:
                value = getattr(self, n)
                # TODO: accessing protected property
                vn = self._meta.get_field(n)._verbose_name
                if vn:
                    name_value.append("{}='{}'".format(vn, value))
                else:
                    name_value.append("{}='{}'".format(n, value))
            error.message = "{model_name} with <{unique_fields}> already exists".format(
                model_name=str(model_class).split('.')[-1][:-2],
                unique_fields=', '.join(name_value))
        return error


class AbstractBook(models.Model):
    class Meta:
        abstract = True

    # TODO: check if better way than repeat type
    allowed_book_id_types = ('ASIN', 'ISBN')
    choices_book_id_types = [(t, t) for t in allowed_book_id_types]

    book_id = models.CharField('Book Identifier (e.g. ISBN-10 or ASIN)',
                               primary_key=True,
                               max_length=20)
    book_id_type = models.CharField('Type of Book Identifier',
                                    max_length=10,
                                    choices=choices_book_id_types)
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
    thumbnail_cover_image = models.ImageField(upload_to='cover_images',
                                              default=None,
                                              blank=True)
    enlarged_cover_image = models.ImageField(upload_to='cover_images',
                                             default=None,
                                             blank=True)

    # TODO: only Book not BookFile
    def clean(self):
        self._validate_book_id()

    def _validate_book_id(self):
        # TODO: add check constraints
        # Validate book identifier
        if self.book_id_type == 'ISBN':
            if pyisbn.validate(self.book_id):
                if len(self.book_id) == 10:
                    self.isbn10 = self.book_id
                    self.isbn13 = pyisbn.convert(self.book_id)
                else:
                    self.isbn13 = self.book_id
                    self.isbn10 = pyisbn.convert(self.book_id)
            else:
                raise ValidationError(
                    {'book_id': '{} is an invalid ISBN'.format(self.book_id)})
        elif self.book_id_type == 'ASIN':
            regex = r"[A-Z0-9]{10}"
            # Remove whitespaces
            self.book_id = self.book_id.strip()
            if len(self.book_id) == 10 and re.fullmatch(regex, self.book_id):
                self.asin = self.book_id
            else:
                raise ValidationError(
                    {'book_id': '{} is an invalid ASIN'.format(self.book_id)})
        else:
            raise ValidationError(
                {'book_id_type': 'Allowed Book Id types: {}'.format(
                    self.allowed_book_id_types)})


class Book(AbstractBook):
    class BookFormat(models.TextChoices):
        Hardcover = 'H'
        Kindle = 'K'
        Paperback = 'P'

    # Book format is required
    # For example, hardcover and paperback
    book_format = models.CharField(max_length=10,
                                   default="",
                                   blank=True,
                                   choices=BookFormat.choices)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return "{} [{}]".format(self.title, self.book_id)


class BookFile(AbstractBook, UniqueErrorMessage):
    class Meta:
        # TODO: remove this and use unique on md5 and sha256 only
        # TODO: test combinations
        unique_together = (("md5", "filepath"),)

    # TODO: extensions already found in scripts/tools.py
    allowed_extensions = ('azw', 'azw3', 'cbz', 'chm', 'djvu', 'docx', 'epub',
                          'gz', 'mobi', 'pdf', 'rar', 'zip',)

    # Fields
    # Automatic primary key
    book_id = models.CharField('Book Identifier (e.g. ISBN-10 or ASIN)', max_length=20)
    # book is required field
    # TODO: test on_delete
    books = models.ManyToManyField(Book, blank=True)
    # TODO: Should filepath be CharField with max_length (but what)?
    # filepath is required field
    filepath = models.TextField('File path', validators=[validate_ebook_file])
    # Size is given in multiples of bytes, and the unit symbol is shown beside
    # the file size, e.g. 660 KB
    size = models.CharField('File size',
                            max_length=10,
                            default="0",
                            editable=False)
    # TODO: remove this variable
    size_unit = models.CharField('Size unit',
                                 max_length=2,
                                 default="MB",
                                 editable=False)
    # md5 and sha256 are in hexadecimal
    # TODO: validate both fields
    # TODO: use unique on both files
    md5 = models.CharField('MD5', max_length=32, default="")
    sha256 = models.CharField('SHA256', max_length=64, default="")

    def __str__(self):
        return "{} [{}]: {}".format(self.title,
                                    self.book_id,
                                    self.filepath)


class Author(models.Model):
    # TODO: test primary key if set automatic
    books = models.ManyToManyField(Book,
                                   blank=True,
                                   related_name='authors',
                                   through='Authorship')
    # Required fields
    name = models.CharField(max_length=200)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)
    slug_name = models.SlugField(max_length=200, null=True, blank=True)

    # Ref.: https://www.fullstackpython.com/django-db-models-slugfield-examples.html
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_name = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Authorship(UniqueErrorMessage):
    class Meta:
        # TODO: doesn't do anything
        # TODO: it is recommended to use UniqueConstraint. In the docs there is
        # a note stating unique_together may be deprecated in the future
        # Ref.: https://stackoverflow.com/a/49817401
        unique_together = (("author", "book"),)
        verbose_name_plural = "Authorship"

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def clean(self):
        # TODO: do something
        pass

    def __str__(self):
        return ' '


# TODO: where is it used?
@receiver(m2m_changed, sender=Author.books.through)
def verify_uniqueness(sender, **kwargs):
    author = kwargs.get('instance', None)
    action = kwargs.get('action', None)
    books = kwargs.get('pk_set', None)

    if action == 'pre_add':
        for book in books:
            if Author.objects.filter(name=author.name).filter(books=book):
                raise IntegrityError("Author with name '{author_name}' already "
                                     "exists for book '{book_title}'".format(
                                      author_name=author.name,
                                      book_title=Book.objects.get(pk=book)))


class Category(UniqueErrorMessage):
    class Meta:
        unique_together = (("category", "source"),)
        verbose_name_plural = "categories"

    class SourceOfCategory(models.TextChoices):
        AMAZON = 'A'
        GOODREADS = 'G'
        USER = 'U'
        WIKIPEDIA = 'W'

    # TODO: check that category is unique
    category = models.CharField(max_length=200)
    source = models.CharField('Source of category',
                              max_length=200,
                              choices=SourceOfCategory.choices)
    # books = models.ManyToManyField(Book, blank=True)
    # Automatic fields
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} [{}]".format(self.category, self.get_source_display())


class Rating(UniqueErrorMessage):
    class Meta:
        unique_together = (("book", "source"),)

    class SourceOfRating(models.TextChoices):
        AMAZON = 'A'
        GOODREADS = 'G'
        USER = 'U'

    # TODO: primary key is (book_id, source)?
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    source = models.CharField('Source of rating',
                              max_length=200,
                              choices=SourceOfRating.choices)
    # TODO: FloatField instead of DecimalField?,
    # see https://docs.djangoproject.com/en/3.0/ref/models/fields/#floatfield
    # 1 <= avg_rating <= 5
    avg_rating = models.FloatField(
        'Average rating',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    # nb_ratings >= 1
    nb_ratings = models.PositiveIntegerField('Number of ratings',
                                             null=True,
                                             blank=True,
                                             validators=[MinValueValidator(1)])
    user_rating = models.FloatField(
        'User rating',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    # Automatic fields
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    # TODO: validate ratings, e.g. if user rating, other fields (avg_rating
    # and nb_ratings) should be blanked
    def clean(self):
        if self.source == 'User':
            pass
        else:
            pass

    def __str__(self):
        return "{} [{}]: {}/5, {} ratings [{}]".format(self.book.title,
                                                       self.book.book_id,
                                                       self.avg_rating,
                                                       self.nb_ratings,
                                                       self.get_source_display())


class Tag(UniqueErrorMessage):
    class Meta:
        unique_together = (("tag", "source"),)

    class SourceOfTag(models.TextChoices):
        AMAZON = 'A'
        GOODREADS = 'G'
        USER = 'U'

    # TODO: check tag is unique
    tag = models.CharField(max_length=200)
    # TODO: add choices such as amazon, personal
    source = models.CharField('Source of tag',
                              max_length=200,
                              choices=SourceOfTag.choices)
    # books = models.ManyToManyField(Book, blank=True)
    # Automatic fields
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} [{}]".format(self.tag, self.get_source_display())


"""
<form action="{% url 'ebook-manager:upload_files' %}" method="post" enctype="multipart/form-data">
  {% csrf_token %}
  <div class="form-group">
    <label for="UploadFiles">Add ebooks:</label>
    <input type="file" name="files" class="form-control-file" id="UploadFiles" multiple>
    <input type="submit" value="Upload">
  </div>
</form>

"""
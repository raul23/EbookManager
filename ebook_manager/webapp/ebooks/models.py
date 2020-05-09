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
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)
    # TODO: ImageField required the Pillow library
    thumbnail_cover_image = models.ImageField()
    enlarged_cover_image = models.ImageField()

    def __str__(self):
        return self.title


class Author(models.Model):
    books = models.ManyToManyField(Book)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Rating(models.Model):
    # TODO: primary key is (book_id, source)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    source = models.CharField('Source of rating', max_length=200)
    # TODO: FloatField instead of DecimalField?,
    # see https://docs.djangoproject.com/en/3.0/ref/models/fields/#floatfield
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    nb_ratings = models.PositiveIntegerField('Number of ratings')
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return self.rating


class Tag(models.Model):
    books = models.ManyToManyField(Book)
    tag = models.CharField(max_length=200)
    source = models.CharField('Source of tag', max_length=200)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return self.tag


class Category(models.Model):
    books = models.ManyToManyField(Book)
    category = models.CharField(max_length=200)
    source = models.CharField('Source of category', max_length=200)
    add_date = models.DateTimeField('Date added', auto_now_add=True)
    update_date = models.DateTimeField('Date updated', auto_now=True)

    def __str__(self):
        return self.category

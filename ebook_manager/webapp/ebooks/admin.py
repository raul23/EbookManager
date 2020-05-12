from django.contrib import admin

# Register your models here.
from .models import Author, Book, BookFile, Category, Rating, Tag
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookFile)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Tag)

import json
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from ebooks.models import Author, Book, BookFile, Category, Rating, Tag


def generate_iso_639_lang():
    from languages import languages
    # Get list of ISO 639 languages and sort them by language name
    # (they are already sorted by language codes)
    iso_639_lang = list(languages.LANGUAGES)
    print("Sorting ...")
    iso_639_lang.sort(key=lambda tup: tup[1])

    # Save languages as a tuple of tuples to a .py file
    print("Writing ...")
    with open('iso_639_languages.py', 'w') as f:
        f.write("# -*- coding: utf-8 -*-\n\n\n")
        f.write("# Sorted by language name, taken from languages module\n")
        f.write("# Ref.: https://pypi.org/project/django-language-fields\n")
        f.write("LANGUAGES = (\n")
        for tup in iso_639_lang:
            line = '    ("{}", "{}"),\n'.format(tup[0], tup[1])
            f.write(line)
        f.write(")\n")
    print("Done!")


def load_iso_639_lang():
    # Load data
    from iso_639_languages import ISO_639_LANGUAGES
    print("There are {} language codes".format(len(ISO_639_LANGUAGES)))


def populate_db():

    def save_data_with_mtom_rel(tb_data, class_):
        for d in tb_data:
            books = d['books']
            del d['books']
            tb_obj = class_.objects.create(**d)
            for b_id in books:
                try:
                    book = Book.objects.get(book_id=b_id)
                    tb_obj.books.add(book)
                except Book.DoesNotExist:
                    continue

    def save_data_with_foreign_rel(tb_data, class_):
        for d in tb_data:
            b_id = d['book']
            try:
                book = Book.objects.get(book_id=b_id)
                d['book'] = book
                class_.objects.create(**d)
            except Book.DoesNotExist:
                continue

    with open('test_data.json') as f:
        data = json.load(f)

    # Save books
    for book_data in data['Books']:
        Book.objects.create(**book_data)

    save_data_with_mtom_rel(data['BookFiles'], BookFile)
    save_data_with_mtom_rel(data['Authors'], Author)
    save_data_with_mtom_rel(data['Categories'], Category)
    save_data_with_mtom_rel(data['Tags'], Tag)
    save_data_with_foreign_rel(data['Ratings'], Rating)


def clear_tb():
    Book.objects.all().delete()
    Author.objects.all().delete()
    BookFile.objects.all().delete()
    Category.objects.all().delete()
    Rating.objects.all().delete()
    Tag.objects.all().delete()


if __name__ == '__main__':
    # generate_iso_639_lang()
    # load_iso_639_lang()
    populate_db()
    # clear_tb()

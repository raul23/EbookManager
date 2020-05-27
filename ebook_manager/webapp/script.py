import json
import os

import django
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
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
        for obj_data in tb_data:
            try:
                books = obj_data['books']
                del obj_data['books']
                tb_obj = class_(**obj_data)
                tb_obj.full_clean()
            except KeyError as e:
                print(e)
                continue
            except ValidationError as e:
                for msg in e.message_dict['__all__']:
                    print(msg)
                continue
            else:
                tb_obj.save()
            # tb_obj = class_.objects.create(**obj_data)
            for b_id in books:
                try:
                    book = Book.objects.get(book_id=b_id)
                    tb_obj.books.add(book)
                except (Book.DoesNotExist, IntegrityError) as e:
                    print(e)

    def save_data_with_foreign_rel(tb_data, class_):
        for obj_data in tb_data:
            try:
                b_id = obj_data['book']
                book = Book.objects.get(book_id=b_id)
                obj_data['book'] = book
                tb_obj = class_(**obj_data)
                tb_obj.full_clean()
                # class_.objects.create(**obj_data)
            except (KeyError, Book.DoesNotExist) as e:
                print(e)
            except ValidationError as e:
                for msg in e.message_dict['__all__']:
                    print(msg)
            else:
                tb_obj.save()

    with open('test_data.json') as f:
        data = json.load(f)

    # Save books
    for book_data in data['Books']:
        try:
            book = Book.objects.get(book_id=book_data['book_id'])
        except KeyError as e:
            print(e)
        except ObjectDoesNotExist:
            book = Book(**book_data)
            book.full_clean()
            book.save()
            # Book.objects.create(**book_data)
        else:
            print("Book '{}' already exists".format(str(book)))

    save_data_with_mtom_rel(data['Authors'], Author)
    save_data_with_mtom_rel(data['BookFiles'], BookFile)
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

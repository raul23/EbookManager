import json
import os

import django
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.mysite.settings")
django.setup()

from ebook_manager import data
from ebook_manager.models import Author, Book, BookFile, Category, Rating, Tag

DATA_DIRPATH = data.__path__[0]
TEST_DATA_FILEPATH = "test_data.json"


def clear_tb():
    Author.objects.all().delete()
    Book.objects.all().delete()
    BookFile.objects.all().delete()
    Category.objects.all().delete()
    Rating.objects.all().delete()
    Tag.objects.all().delete()


def populate_db():

    def save_data_in_db(tb_data, class_):
        for obj_data in tb_data:
            try:
                books = obj_data.get('books', [])
                if books:
                    del obj_data['books']
                filepath = obj_data.get('filepath')
                if filepath:
                    obj_data['filepath'] = os.path.expanduser(filepath)
                tb_obj = class_(**obj_data)
                tb_obj.full_clean()
            except KeyError as e:
                print(e)
            except ValidationError as e:
                for msg in e.message_dict['__all__']:
                    print(msg)
            else:
                tb_obj.save()
                for b_id in books:
                    try:
                        book = Book.objects.get(book_id=b_id)
                        tb_obj.books.add(book)
                    except (Book.DoesNotExist, IntegrityError) as e:
                        print(e)

    filepath = os.path.join(DATA_DIRPATH, TEST_DATA_FILEPATH)
    with open(filepath) as f:
        data = json.load(f)

    save_data_in_db(data['Categories'], Category)
    save_data_in_db(data['Tags'], Tag)

    # Save books
    for book_data in data['Books']:
        book_already_exists = False
        try:
            book = Book.objects.get(book_id=book_data['book_id'])
        except KeyError as e:
            print(e)
        except ObjectDoesNotExist:
            book_already_exists = True
        else:
            print("Book '{}' already exists".format(str(book)))
        if book_already_exists:
            try:
                categories = book_data['categories']
                del book_data['categories']
                tags = book_data['tags']
                del book_data['tags']
                book = Book(**book_data)
                book.full_clean()
            except KeyError as e:
                print(e)
            except ValidationError as e:
                for msg in e.message_dict['__all__']:
                    print(msg)
            else:
                book.save()
                all_objects = [(Category, 'category', categories), (Tag, 'tag', tags)]
                for (class_, objects) in all_objects:
                    for obj_name in objects:
                        try:
                            obj = class_.objects.get(category=obj_name)
                            book.books.add(book)
                        except (Book.DoesNotExist, IntegrityError) as e:
                            print(e)

    save_data_in_db(data['Authors'], Author)
    save_data_in_db(data['BookFiles'], BookFile)
    save_data_in_db(data['Ratings'], Rating)


if __name__ == '__main__':
    # TODO: add command-line arguments
    populate_db()
    # clear_tb()

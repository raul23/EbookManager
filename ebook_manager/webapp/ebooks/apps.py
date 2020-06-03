from django.apps import AppConfig

# TODO: remove package import
from ebooks.data.remove_chars_in_filename import LIST_CHARS


class EbooksConfig(AppConfig):
    name = 'ebooks'
    # TODO: remove package import
    # remove_chars_in_filename = ['- chars to remove', ]
    unwanted_chars = LIST_CHARS

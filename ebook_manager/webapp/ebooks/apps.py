from django.apps import AppConfig

# TODO: remove package import
from ebooks.data.remove_chars_in_filename import LIST_CHARS


class EbooksConfig(AppConfig):
    name = 'ebooks'
    # TODO: remove package import
    process_file_cfg = {'unwanted_chars': LIST_CHARS}

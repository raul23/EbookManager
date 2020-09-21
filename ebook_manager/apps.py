from django.apps import AppConfig

# TODO: remove package import
from ebook_manager.data.remove_chars_in_filename import LIST_CHARS


class EbookManagerConfig(AppConfig):
    name = 'ebook_manager'
    # TODO: remove package import
    file_processor_cfg = {
        'unwanted_chars_in_filename': LIST_CHARS,
        'filename_templates': ["AUTHOR - TITLE (YEAR)",
                               "TITLE BY AUTHOR (YEAR)"]}

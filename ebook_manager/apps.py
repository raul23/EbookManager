from django.apps import AppConfig

# TODO: remove package import
from ebook_manager.data.remove_chars_in_filename import LIST_CHARS


class EbookManagerConfig(AppConfig):
    name = "ebook_manager"
    label = "ebook-manager"
    verbose_name = "Ebook Manager"
    # TODO: remove package import
    file_processor_cfg = {
        'unwanted_chars_in_filename': LIST_CHARS,
        'filename_templates': [
            "(?P<AUTHORS>.+) - (?P<TITLE>.+) (?P<YEAR>\\(.+\\))",
            "(?P<TITLE>.+) [BY|by] (?P<AUTHORS>.+) (?P<YEAR>\\(.+\\))"]}

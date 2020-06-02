# Built-in modules
import hashlib
import re
# Third-party modules
import pyisbn
# Personal modules
from ebooks.apps import EbooksConfig


class ProcessFile:
    def __init__(self, file):
        self.file = file
        self.chunk_size = 8192
        self.isbn = None
        self.asin = None
        self._unwanted_chars = EbooksConfig.unwanted_chars

    def _get_hash(self):
        # Ref.: https://stackoverflow.com/a/38719060
        hash = hashlib.md5()
        for chunk in self.file.chunks(chunk_size=self.chunk_size):
            hash.update(chunk)
        return hash.hexdigest()

    def check_hash_in_db(self):
        # Compute file's md5 and sha256
        hash = self._get_hash()
        # Check if computed hash is already in db

    def get_isbn_from_filename(self):
        # TODO: getter?
        if self.isbn:
            return self.isbn
        # Extract ISBN or ASIN from filename using regex
        regex_isbn10 = r"[A-Z0-9]{10}"
        regex_isbn13 = r"[\-A-Z0-9]{13,}"
        for isbn in re.findall(regex_isbn13, filename):
            if pyisbn.validate(isbn):
                pass
        # Get ISBN or ASIN by doing an Amazon search

    def remove_chars_in_filename(self):
        pass

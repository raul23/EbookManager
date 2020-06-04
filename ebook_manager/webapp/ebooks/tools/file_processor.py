import hashlib
import re

import pyisbn


class FileProcessor:
    def __init__(self, file, chunk_size=128 * hashlib.md5().block_size,
                 unwanted_chars=None):
        self.file = file
        self.file_hash = None
        # Ref.: https://stackoverflow.com/a/11143944
        self.chunk_size = chunk_size
        self.isbn = None
        self.asin = None
        self.unwanted_chars = unwanted_chars

    def _is_hash_in_db(self):
        # Check if file hash is already in db
        pass

    def _compute_hash(self, hash_factory=hashlib.md5):
        # Ref.:
        # - https://stackoverflow.com/a/38719060
        # - https://stackoverflow.com/a/4213255
        hash = hash_factory()
        for chunk in self.file.chunks(chunk_size=self.chunk_size):
            hash.update(chunk)
        return hash.hexdigest()

    def _get_isbn_from_filename(self):
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

    def _remove_chars_in_filename(self):
        pass

    def start_processing(self):
        # Compute file's md5
        self._compute_hash()
        # Check if file hash is in db
        if not self._is_hash_in_db():
            pass
        #


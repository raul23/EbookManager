import hashlib
import re

import pyisbn


class ProcessFile:
    def __init__(self, file, chunk_size=128 * hashlib.md5().block_size,
                 unwanted_chars=None):
        self.file = file
        # Ref.: https://stackoverflow.com/a/11143944
        self.chunk_size = chunk_size
        self.isbn = None
        self.asin = None
        self.unwanted_chars = unwanted_chars

    def _get_hash(self, hash_factory=hashlib.md5):
        # Ref.:
        # - https://stackoverflow.com/a/38719060
        # - https://stackoverflow.com/a/4213255
        hash = hash_factory()
        for chunk in self.file.chunks(chunk_size=self.chunk_size):
            hash.update(chunk)
        return hash.hexdigest()

    def check_hash_in_db(self):
        # Compute file's md5 and sha256
        md5_hash = self._get_hash()
        sha256_hash = self._get_hash(hashlib.sha256)
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


def process_file(file, **kargs):
    pf = ProcessFile(file, **kargs)

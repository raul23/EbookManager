import hashlib
import re

import pyisbn


class FileProcessor:
    def __init__(self, file, chunk_size=128 * hashlib.md5().block_size,
                 unwanted_chars=None):
        # TODO: make sure file is of valid type
        self.file = file
        self.filename = file.name
        self.size = file.size
        self.content_type = file.content_type
        self.md5 = None
        self.sha256 = None
        # Ref.: https://stackoverflow.com/a/11143944
        self.chunk_size = chunk_size
        self.isbn10 = None
        self.isbn13 = None
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

    def _search_amazon(self, keywords):
        pass

    def _set_asin_from_filename(self):
        # Extract ASIN from filename using regex
        pass

    def _set_isbns_from_filename(self):
        # Extract ISBN from filename using regex
        def _get_isbn(regex):
            for isbn in re.findall(regex, self.filename):
                if pyisbn.validate(isbn):
                    return isbn, pyisbn.convert(isbn)
            return None
        regex_isbn10 = r"[A-Z0-9]{10}"
        regex_isbn13 = r"[\-A-Z0-9]{13,}"
        for r in [regex_isbn10, regex_isbn13]:
            isbns = _get_isbn(r)
            if isbns:
                self.isbn10 = isbns[0]
                self.isbn13 = isbns[1]
                return True
        return False

    def _remove_chars_in_filename(self):
        for chars in self.unwanted_chars:
            self.filename = self.filename.replace(chars, '')

    def start_processing(self):
        # TODO: check first if file has already been processed
        # Compute file's md5
        self._compute_hash()
        # TODO: compute file's sha256
        # Check if file hash is in db
        if self._is_hash_in_db():
            pass
        # Since file hash is not found in db, file is new and we will do the
        # following to get the ISBN or ASIN:
        # 1. Pre-processing on the filename
        # 2. Get th ISBN from the filename
        # 3. If no ISBN found, get the ASIN from the filename
        # 4. If no ISBN or ASIN from filname, get ISBN or ASIN by doing an
        #    Amazon search based on the filename
        # 5. If still no ISBN or ASIN found, do a
        #
        # 1. Pre-processing on the filename
        self._remove_chars_in_filename()
        if self._set_isbns_from_filename():  # 2. ISBN
            self._search_amazon(self.isbn10)
        elif self._set_asin_from_filename():  # 3. ASIN
            self._search_amazon(self.asin)
        elif self._search_amazon(self.filename):  # 4. Amazon search
            pass



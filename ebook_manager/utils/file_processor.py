import hashlib
import re

import ipdb
import pyisbn

from ebook_manager.models import BookFile


class FileProcessor:
    def __init__(self, file, chunk_size=128 * hashlib.md5().block_size,
                 unwanted_chars_in_filename=None, filename_templates=None,
                 enable_txt_conversion=False, enable_ocr=False):
        # TODO: make sure file is of valid type
        self.file = file
        self.original_filename = file.name
        self.filename = file.name
        self.size = file.size
        self.content_type = file.content_type
        # Ref.: https://stackoverflow.com/a/11143944
        self.chunk_size = chunk_size
        self.md5 = self._get_hash()
        self.sha256 = self._get_hash(hashlib.sha256)
        self.isbn10 = None
        self.isbn13 = None
        self.asin = None
        self.unwanted_chars_in_filename = unwanted_chars_in_filename
        self.filename_templates = filename_templates
        self.enable_txt_conversion = enable_txt_conversion
        self.enable_ocr = enable_ocr

    def _get_book_id(self):
        pass

    @staticmethod
    def _get_bookfile_from_db(kwargs):
        # Check if file hash is already in db
        try:
            book_file = BookFile.objects.get(**kwargs)
        except BookFile.DoesNotExist:
            return None
        else:
            return book_file

    def _get_hash(self, hash_factory=hashlib.md5):
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

    def _set_book_ids_from_filename(self):
        # Extract book ids from filename using regex
        pass

    def _set_book_ids_from_ocr_file(self):
        # Extract book ids from content of OCR file
        pass

    def _set_book_ids_from_txt_file(self):
        # Extract book ids from content of txt file
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
        ipdb.set_trace()
        for regex in self.unwanted_chars_in_filename:
            pass

    def start_processing(self):
        # Preprocess the filename
        self._remove_chars_in_filename()
        # Check if filename satisfies one of the template
        for template in self.filename_templates:
            pass
        # Check if file hash is in db
        bookfile = self._get_bookfile_from_db(dict(md5=self.md5))
        if bookfile:
            return bookfile
        # Since file hash is not found in db, file is new and we will do the
        # following to get the book id (e.g. ISBN or ASIN):
        # 1. Get th book id from the filename
        # 3. If no book id from filename, get it by doing an Amazon search
        #    based on the filename
        # 4. If still no book id found, get it directly from the txt conversion
        #    of the ebook file
        # 5. If the txt conversion couldn't work, then OCR the file and try to
        #    get the book id from the OCRed file
        #
        # 1. Get the book id from the filename
        if self._set_book_ids_from_filename():
            # Get book info by doing an Amazon search based on the book id
            self._search_amazon(self.isbn10)
        else:
            # 2. No ISBN or ASIN could be retrieved, do an Amazon search based
            #    on the filename
            if not self._search_amazon(self.filename):
                # 4. Get book id from txt conversion
                if self.enable_txt_conversion and \
                        self._set_book_ids_from_txt_file():
                    self._search_amazon(self._get_book_id())
                # 5. Get book id from OCR file
                elif self.enable_ocr and self._set_book_ids_from_ocr_file():
                    self._search_amazon(self._get_book_id())
                else:
                    # Nothing worked!
                    pass

import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from languages import languages
import ipdb


def generate_iso_639_lang():
    ipdb.set_trace()
    # Get list of ISO 639 languages and sort them by language name
    # (they are already sorted by language codes)
    iso_639_lang = list(languages.LANGUAGES)
    iso_639_lang.sort(key=lambda tup: tup[1])

    # Save languages as a tuple of tuples to a .py file
    with open('iso_639_lang', 'w') as f:
        f.write("# -*- coding: utf-8 -*-\n\n\n")
        f.write("# Sorted by language name, taken from languages module\n")
        f.write("# Ref.: https://pypi.org/project/django-language-fields\n")
        f.write("ISO_639_LANGUAGES = (")
        for tup in iso_639_lang:
            line = '    ("{}", "{}"),\n'.format(tup[0], tup[1])
            f.write(line)
        f.write(")\n")

    """
    # Only keep two-letter codes
    iso_6391_lang = [tup for tup in iso_639_lang if len(tup[0]) == 2]
    iso_6391_lang_names = [tup[1] for tup in iso_6391_lang]

    rejected = []
    popular_iso_6391_lang = []
    for tup in iso_6391_lang:
        if tup[1] in google_popular_lang:
            popular_iso_6391_lang.append(tup)
        else:
            rejected.append(tup)

    set(google_popular_lang).difference(set(iso_6391_lang_names))
    """


if __name__ == '__main__':
    generate_iso_639_lang()
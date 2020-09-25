import os

from languages import languages

from data import filtered_iso_639_languages
from data import google_languages
from data import iso_639_languages


def filter_iso_639_lang():
    iso_639_lang = iso_639_languages.LANGUAGES
    google_lang = google_languages.LANGUAGES

    # Filter iso_639_lang: only keep google language names
    filtered_iso_639_lang = []
    lang_names = []
    rejected_lang = []
    for tup in iso_639_lang:
        if tup[1] in google_lang and tup[1] not in lang_names:
            filtered_iso_639_lang.append(tup)
            lang_names.append(tup[1])
        else:
            rejected_lang.append(tup)
    # Add these languages not found in iso_639_languages but found in google_lang
    missing_lang = [('ug', 'Uyghur'), ('pa', 'Punjabi'), ('ps', 'Pashto'),
                    ('el', 'Greek'), ('or', 'Odia (Oriya)'),
                    ('gd', 'Scots Gaelic'), ('ny', 'Chichewa'),
                    ('fy', 'Frisian'), ('ky', 'Kyrgyz'),
                    ('my', 'Myanmar (Burmese)'), ('ku', 'Kurdish (Kurmanji)'),
                    ('st', 'Sesotho'), ('zh', 'Chinese'),
                    ('ht', 'Haitian Creole')]
    lang_names.extend([tup[1] for tup in missing_lang])
    filtered_iso_639_lang.extend(missing_lang)
    # diff1 = set(google_lang).difference(set(lang_names))
    # diff2 = set(lang_names).difference(set(google_lang))

    print("Sorting ...")
    filtered_iso_639_lang.sort(key=lambda tup: tup[1])

    # Save languages as a tuple of tuples to a .py file
    print("Writing ...")
    filepath = os.path.join(os.getcwd(), 'data', 'filtered_iso_639_languages.py')
    with open(filepath, 'w') as f:
        f.write("# -*- coding: utf-8 -*-\n\n\n")
        f.write("# Built from iso_639_languages.py\n")
        f.write("# Sorted by language name and only most popular ones based on\n")
        f.write("# https://translate.google.com\n")
        f.write("# NOTE: using (zh, Chinese) instead of Chinese (Simplified) and\n")
        f.write("# Chinese (Traditional) like Google does\n")
        f.write("LANGUAGES = (\n")
        for tup in filtered_iso_639_lang:
            line = '    ("{}", "{}"),\n'.format(tup[0], tup[1])
            f.write(line)
        f.write(")\n")
    print("Done!")


def generate_iso_639_lang():
    # Get list of ISO 639 languages and sort them by language name
    # (they are already sorted by language codes)
    iso_639_lang = list(languages.LANGUAGES)
    print("Sorting ...")
    iso_639_lang.sort(key=lambda tup: tup[1])

    # Save languages as a tuple of tuples to a .py file
    print("Writing ...")
    with open('iso_639_languages.py', 'w') as f:
        f.write("# -*- coding: utf-8 -*-\n\n\n")
        f.write("# Sorted by language name, taken from languages module\n")
        f.write("# Ref.: https://pypi.org/project/django-language-fields\n")
        f.write("LANGUAGES = (\n")
        for tup in iso_639_lang:
            line = '    ("{}", "{}"),\n'.format(tup[0], tup[1])
            f.write(line)
        f.write(")\n")
    print("Done!")


def load_filtered_iso_639_lang():
    # Load data
    lang = filtered_iso_639_languages.LANGUAGES
    print("There are {} language codes".format(len(lang)))


def load_iso_639_lang():
    # Load data
    lang = iso_639_languages.LANGUAGES
    print("There are {} language codes".format(len(lang)))


if __name__ == '__main__':
    pass

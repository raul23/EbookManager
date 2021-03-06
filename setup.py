"""setup.py file for the package `ebook_manager`.

The PyPi project name is EbookManager and the package name is `ebook_manager`.

"""

import os
from setuptools import find_packages, setup


# Directory of this file
dirpath = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(dirpath, "README.rst")) as f:
    README = f.read()

# TODO: get the version programmatically
setup(name='django-ebook-manager',
      version='0.1',
      description='Python Ebook Manager',
      long_description=README,
      long_description_content_type='text/x-rst',
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
      ],
      keywords='ebook manager',
      url='https://github.com/raul23/django-ebook-manager',
      author='Raul C.',
      author_email='rchfe23@gmail.com',
      license='GPLv3',
      packages=find_packages(exclude=['tests']),
      entry_points={
        'console_scripts': ['db_ebooks=ebook_manager.scripts.db_ebooks:main']
      },
      zip_safe=False)

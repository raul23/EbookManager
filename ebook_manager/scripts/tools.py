#!/usr/script/env python
"""Script for .

"""

import argparse
import logging
import os
import pathlib
import re
import shutil
from collections import namedtuple
from logging import NullHandler

import ipdb

from ebook_manager import __version__


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

_doc_types = ['azw', 'azw3', 'cbz', 'chm', 'djvu', 'docx', 'epub', 'gz', 'mobi', 'pdf',
              'rar', 'zip']
_upper_doc_types = [t.upper() for t in _doc_types]


# TODO: add logging message at the start of each function


def _get_filenames(dirpath, doc_types=_doc_types):
    """TODO

    Parameters
    ----------
    dirpath
    doc_types

    Returns
    -------

    """
    # TODO: explain code
    results = namedtuple("results", "valid_fnames rejected_fnames rejected_ext")
    valid_filenames = set()
    rejected_filenames = set()
    rejected_ext = set()
    for filename in os.listdir(dirpath):
        ext = os.path.splitext(filename)[-1][1:]
        if ext in doc_types:
            valid_filenames.add(filename)
        else:
            rejected_filenames.add(filename)
            rejected_ext.add(ext)
    results.valid_fnames = valid_filenames
    results.rejected_fnames = rejected_filenames
    results.rejected_ext = rejected_ext
    return results


def _show_results(results):
    """TODO

    Parameters
    ----------
    results

    Returns
    -------

    """
    # TODO: explain code
    print("Number of valid files: {}".format(len(results.valid_fnames)))
    print("Rejected files:")
    [print("- {}".format(f)) for f in sorted(list(results.rejected_fnames))]
    print("Rejected ext: {}".format(results.rejected_ext))


def copy_documents(src_dirpath, dst_dirpath, doc_types=_doc_types):
    """TODO

    Parameters
    ----------
    src_dirpath
    dst_dirpath
    doc_types

    Returns
    -------

    """
    # TODO: do it with mv *.pdf ...
    ipdb.set_trace()
    for filename in os.listdir(src_dirpath):
        ext = os.path.splitext(filename)[-1][1:]
        if ext in doc_types:
            src_filepath = os.path.join(src_dirpath, filename)
            dst_filepath = os.path.join(dst_dirpath, filename)
            shutil.copyfile(src_filepath, dst_filepath)
    return 0


def diff_sets_of_documents(dirpath_set1, dirpath_set2, doc_types=_doc_types):
    """TODO

    Parameters
    ----------
    dirpath_set1
    dirpath_set2
    doc_types

    Returns
    -------

    """
    # TODO: explain code
    try:
        results1 = _get_filenames(dirpath_set1, doc_types)
        results2 = _get_filenames(dirpath_set2, doc_types)
    except OSError as e:
        print(e)
        return 1
    whole_results = [results1, results2]

    for i, dirpath in enumerate([dirpath_set1, dirpath_set2]):
        print("Results for set{}: {}".format(i+1, dirpath))
        results = whole_results[i]
        _show_results(results)

        other_idx = 1 if i == 0 else 0
        print("Difference between set{} and set{}: {}".format(
            i+1,
            other_idx+1,
            results.valid_fnames - whole_results[other_idx].valid_fnames))
        print()
    return 0


def fix_extensions(dirpath, doc_types=_doc_types):
    """TODO

    Parameters
    ----------
    dirpath
    doc_types

    Returns
    -------

    """
    # TODO: explain code
    ipdb.set_trace()

    return 0


def group_documents_into_folders(src_dirpath, dst_dirpath, group_size=30,
                                 doc_types=_doc_types,
                                 prefix_fname='group_'):
    """TODO

    Parameters
    ----------
    src_dirpath
    dst_dirpath
    group_size
    doc_types
    prefix_fname

    Returns
    -------

    """
    # TODO: explain code
    # TODO: use Unix command mv
    metadata = namedtuple("metadata", "retcode src_dirpath folderpaths")
    metadata.src_dirpath = src_dirpath
    folderpaths = []
    # Get list of documents and keep valid document types
    list_filenames = []
    # TODO: use get_filenames()
    for filename in os.listdir(src_dirpath):
        ext = os.path.splitext(filename)[-1][1:]
        if ext in doc_types:
            list_filenames.append(filename)
    # Group valid documents into folders
    group_id = 0
    for i in range(0, len(list_filenames), group_size):
        group = list_filenames[i:i+group_size]
        # Create folder for the group of documents
        group_folderpath = os.path.join(dst_dirpath,
                                        "{}{}".format(prefix_fname, group_id))
        group_id += 1
        # TODO: use create_dir() from pyutils.genutils
        # TODO: case where group folder already exists
        pathlib.Path(group_folderpath).mkdir(parents=True)
        folderpaths.append(group_folderpath)
        for filename in group:
            src_filepath = os.path.join(src_dirpath, filename)
            dst_filepath = os.path.join(group_folderpath, filename)
            shutil.move(src_filepath, dst_filepath)
    metadata.retcode = 0
    metadata.folderpaths = folderpaths
    return metadata


def modify_filenames(dirpath, doc_types=_doc_types):
    """TODO

    Parameters
    ----------
    dirpath
    doc_types

    Returns
    -------

    """
    # Iterate recursively through each folder within the `dirpath` directory
    ipdb.set_trace()
    for root, dirs, files in os.walk(dirpath):
        # Remove parentheses and brackets at the beginning of the filename along
        # with their content
        pass
    return 0


def reset_group_documents_into_folders(metadata):
    """TODO

    Parameters
    ----------
    metadata

    Returns
    -------

    """
    # TODO: explain code
    # TODO: add message if AssertError
    assert metadata.retcode == 0
    src_dirpath = metadata.src_dirpath
    folderpaths = metadata.folderpaths
    for group_folderpath in folderpaths:
        for filename in os.listdir(group_folderpath):
            src_filepath = os.path.join(group_folderpath, filename)
            dst_filepath = os.path.join(src_dirpath, filename)
            shutil.move(src_filepath, dst_filepath)
        os.rmdir(group_folderpath)
    return 0


def show_results_about_documents(dirpath, doc_types=_doc_types):
    """

    Parameters
    ----------
    dirpath
    doc_types

    Returns
    -------

    """
    # TODO: explain code
    try:
        results = _get_filenames(dirpath, doc_types)
    except OSError as e:
        print(e)
        return 1

    print("Results for {}".format(dirpath))
    _show_results(results)
    print()

    return 0


def setup_argparser():
    """Setup the argument parser for the command-line script.

    Some of the important actions that can be performed with the script are:

    - TODO,
    - TODO or
    - TODO.

    Returns
    -------
    args : argparse.Namespace
        Simple class used by default by `parse_args()` to create an object
        holding attributes and return it [1]_.

    References
    ----------
    .. [1] `argparse.Namespace
       <https://docs.python.org/3.7/library/argparse.html#argparse.Namespace>`_.

    """
    # Help message that is used in various arguments
    common_help = '''Provide 'log' (without the quotes) for the logging config 
    file or 'main' (without the quotes) for the main config file.'''
    # Setup the parser
    parser = argparse.ArgumentParser(
        # usage="%(prog)s [OPTIONS]",
        prog=os.path.basename(__file__).split(".")[0],
        description='''\
TODO.\n
IMPORTANT: these are only some of the most important options. Open the main 
config file to have access to the complete list of options, i.e. 
%(prog)s -e main''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # ===============
    # General options
    # ===============
    parser.add_argument("--version", action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Enable quiet mode, i.e. nothing will be print.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print various debugging information, e.g. print "
                             "traceback when there is an exception.")
    parser.add_argument("-nc", "--no-color", action="store_true",
                        help="Don't print color codes in output")
    # help=argparse.SUPPRESS)
    # Group arguments that are closely related
    # =============
    # Cache options
    # =============
    cache_group = parser.add_argument_group('Cache options')
    cache_group.add_argument(
        "--cache-dir", dest="dir",
        help='''Location in the filesystem where ebook_manager can store 
        downloaded webpages permanently. By default ~/.cache/ebook_manager is
        used.''')
    cache_group.add_argument("--no-cache-dir", action="store_true",
                             help="Disable caching")
    cache_group.add_argument("--clr-cache-dir", action="store_true",
                             help="Delete all cache files")
    # ===============
    # Group documents
    # ===============
    start_group = parser.add_argument_group('Group documents into folders')
    start_group.add_argument(
        "-s", "--start_scraper", action="store_true",
        help='''Scrape lyrics from webpages and save them locally in a SQLite 
        database''')
    # ===========
    # Edit config
    # ===========
    edit_group = parser.add_argument_group('Edit a configuration file')
    edit_group.add_argument(
        "-e", "--edit", choices=["log", "main"],
        help="Edit a configuration file. {}".format(common_help))
    edit_group.add_argument(
        "-a", "--app-name", default=None, dest="app",
        help='''Name of the application to use for editing the file. If no 
        name is given, then the default application for opening this type of 
        file will be used.''')
    # =================
    # Reset/Undo config
    # =================
    reset_group = parser.add_argument_group(
        'Reset or undo a configuration file')
    reset_group.add_argument(
        "-r", "--reset", choices=["log", "main"],
        help='''Reset a configuration file with factory default values. 
        {}'''.format(common_help))
    reset_group.add_argument(
        "-u", "--undo", choices=["log", "main"],
        help='''Undo the LAST RESET. Thus, the config file will be restored 
        to what it was before the LAST reset. {}'''.format(common_help))
    return parser.parse_args()


def main():
    """Main entry-point to the script.

    Some of the actions that the script can perform:

    - Group documents into folders,
    - Save list of filenames, or
    - Modify filenames according to a template.

    Notes
    -----
    Only one action at a time can be performed.

    """

    return 0


if __name__ == '__main__':
    """
    copy_documents(
        src_dirpath=os.path.expanduser('~/test/ebook_manager/ungrouped_docs'),
        dst_dirpath='/Volumes/Seagate Backup Plus Drive 3TB/ebooks/_tmp')
    """
    show_results_of_documents(
        dirpath=os.path.expanduser('~/Downloads'),
    )
    diff_sets_of_documents(
        dirpath_set1=os.path.expanduser('~/Downloads'),
        dirpath_set2='/Volumes/Seagate Backup Plus Drive 3TB/ebooks/_tmp',
    )
    fix_extensions(os.path.expanduser('~/Downloads'))
    metadata = group_documents_into_folders(
        # src_dirpath=os.path.expanduser('~/Downloads'),
        src_dirpath=os.path.expanduser('~/test/ebook_manager/ungrouped_docs'),
        dst_dirpath=os.path.expanduser('~/test/ebook_manager/grouped_docs'),
        group_size=5)
    reset_group_documents_into_folders(metadata)
    """
    retcode = main()
    msg = "\nProgram exited with <color>{}</color>".format(retcode)
    if retcode == 1:
        logger.error(msg)
    else:
        logger.debug(msg)
    """

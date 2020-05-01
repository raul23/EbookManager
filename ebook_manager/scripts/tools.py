#!/usr/script/env python
"""Script for .

"""

import argparse
import logging
import math
import os
import pathlib
import re
import shutil
from collections import namedtuple
from logging import NullHandler

import ipdb

from ebook_manager import __version__
from pyutils import uninstall_colored_logger
from pyutils.logutils import setup_basic_logger


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

_doc_types = ['azw', 'azw3', 'cbz', 'chm', 'djvu', 'docx', 'epub', 'gz', 'mobi', 'pdf',
              'rar', 'zip']


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
    valid_filenames = []
    rejected_filenames = []
    rejected_ext = set()
    for filename in os.listdir(dirpath):
        ext = os.path.splitext(filename)[-1][1:]
        if ext in doc_types:
            valid_filenames.append(filename)
        else:
            rejected_filenames.append(filename)
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
    # TODO: log only some of the filenames if not verbose. Otherwise log
    # the first 25
    [print("- {}".format(f)) for f in sorted(results.rejected_fnames)]
    print("Rejected ext: {}".format(
        None if not results.rejected_ext else results.rejected_ext))


def _split_filename(filename):
    """TODO

    Parameters
    ----------
    filename

    Returns
    -------

    """
    # TODO: explain code
    root, ext = os.path.splitext(filename)
    ext = ext[1:]
    return root, ext


def copy_docs(src_dirpath, dst_dirpath, doc_types=_doc_types):
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


def diff_sets_of_docs(dirpath_set1, dirpath_set2, doc_types=_doc_types):
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
        diff = set(results.valid_fnames) - \
               set(whole_results[other_idx].valid_fnames)

        print("There are {} differences between set{} and set{}".format(
            len(diff),
            i + 1,
            other_idx + 1))
        if len(diff) > 10:
            print("Some of the differences between set{} and set{}:".format(
                i + 1,
                other_idx + 1))
            [print("- {}".format(f)) for f in list(diff)[:10]]
        elif len(diff) > 1:
            print("Difference between set{} and set{}: {}".format(
                i+1,
                other_idx+1,
                diff))
        if i == 0:
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
    metadata = namedtuple("metadata", "retcode new_filepaths")
    metadata.new_filepaths = []
    new_filepaths = []
    for filename in os.listdir(dirpath):
        src_filepath = os.path.join(dirpath, filename)
        root, ext = _split_filename(filename)
        if os.path.isfile(src_filepath) and ext not in doc_types:
            if ext.lower() in doc_types:
                ext = ext.lower()
            elif filename.count('.') > 1:
                # Fix 2: remove everything after the extension
                # e.g. file.pdf.sb1-383921a --> file.pdf
                root2, ext2 = _split_filename(root)
                ext2 = ext2.lower()
                if ext2 in doc_types:
                    root = root2
                    ext = ext2
                else:
                    continue
            else:
                continue
            new_filename = "{}.{}".format(root, ext)
            dst_filepath = os.path.join(dirpath, new_filename)
            shutil.move(src_filepath, dst_filepath)
            new_filepaths.append((src_filepath, dst_filepath))
    metadata.new_filepaths = new_filepaths
    metadata.retcode = 0
    return metadata


def group_docs_into_folders(src_dirpath, dst_dirpath, group_size=30,
                            doc_types=_doc_types, prefix_fname='group_'):
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
    # TODO: use mv command
    metadata = namedtuple("metadata", "retcode src_dirpath folderpaths")
    metadata.src_dirpath = src_dirpath
    folderpaths = []
    # Get list of documents and keep only valid documents (based on types)
    try:
        results = _get_filenames(src_dirpath, doc_types)
    except OSError as e:
        print(e)
        return 1

    valid_fnames = results.valid_fnames
    # Group valid documents into folders
    group_id = 0
    n_groups = math.ceil(len(valid_fnames)/group_size)
    print("Number of groups: ", n_groups)
    print("Group size: ", group_size)
    print()
    for i in range(0, len(valid_fnames), group_size):
        print("Group {}".format(group_id))
        group = valid_fnames[i:i+group_size]
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
    metadata.folderpaths = folderpaths
    metadata.retcode = 0
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
    # TODO: explain code
    # Iterate recursively through each folder within the `dirpath` directory
    ipdb.set_trace()
    for root, dirs, files in os.walk(dirpath):
        # Remove parentheses and brackets at the beginning of the filename along
        # with their content
        pass
    return 0


def show_results_about_docs(dirpath, doc_types=_doc_types):
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


def undo_fix_extensions(metadata):
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
    new_filepaths = metadata.new_filepaths
    for old_filepath, new_filepath in new_filepaths:
        shutil.move(new_filepath, old_filepath)
    return 0


def undo_group_docs_into_folders(metadata):
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


def setup_argparser():
    """Setup the argument parser for the command-line script.

    Some of the important actions that can be performed with the script are:

    - Fix documents extensions, or
    - Group documents into folders,
    - Modify filenames according to a template.

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
    # Setup the parser
    parser = argparse.ArgumentParser(
        # usage="%(prog)s [OPTIONS]",
        prog=os.path.basename(__file__).split(".")[0],
        description='''\
Useful tools to be used on documents such as fixing extensions, grouping 
documents into folders, and modifying filenames based on a template.''',
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
    # ====================================
    # Difference between sets of documents
    # ====================================
    diff_sets_group = parser.add_argument_group("Print differences between two "
                                                "sets of documents")
    diff_sets_group.add_argument(
        "--diff_dirs", nargs=2, dest="diff_dirpaths",
        help='''Directory paths to the first and second sets of documents.''')
    # ==============
    # Fix extensions
    # ==============
    fix_ext_group = parser.add_argument_group("Fix extensions of documents")
    fix_ext_group.add_argument(
        "-fix", "--fix_dir", dest="fix_dirpath",
        help='''Directory path containing documents whose extensions will be 
        checked and fixed.''')
    # ===============
    # Group documents
    # ===============
    group_docs = parser.add_argument_group("Group documents into folders")
    group_docs.add_argument(
        "--group_dirs", nargs=2, dest="group_dirpaths",
        help='''Source and destination directory paths.''')
    group_docs.add_argument(
        "--group_size", default=30, dest="group_size", type=int,
        help='''Size for each group of documents.''')
    group_docs.add_argument(
        "-p", "--prefix", default='group_', dest="prefix_fname",
        help='''Prefix to be used when naming the folders.''')
    # ================
    # Modify filenames
    # ================
    # TODO: add template in group's description
    modify_group = parser.add_argument_group("Modify filenames based on the "
                                             "template TEMPLATE")
    modify_group.add_argument(
        "-mod", "--modify_dir", dest="modify_dirpath",
        help='''Directory path containing the documents whose filenames will 
        be modified if necessary.''')
    # ============
    # Show results
    # ============
    show_group = parser.add_argument_group("Show basic results about documents "
                                           "such as number of valid filenames "
                                           "and rejected extensions")
    show_group.add_argument(
        "-show", "--show_dir", dest="show_dirpath",
        help='''Directory path containing the documents whose filenames will 
        be modified if necessary.''')
    # ==========
    # Undo tasks
    # ==========
    undo_group = parser.add_argument_group("Undo some of the tasks such as "
                                           "fixing the extensions and grouping "
                                           "documents")
    undo_group.add_argument(
        "--undo_fix", action="store_true",
        help='''Undo the LAST fixing of extensions..''')
    undo_group.add_argument(
        "--undo_group", action="store_true",
        help='''Undo the LAST grouping of documents''')
    return parser.parse_args()


def main():
    """Main entry-point to the script.

    Some of the actions that the script can perform:

    - Fix documents extensions, or
    - Group documents into folders,
    - Modify filenames according to a template.

    Notes
    -----
    Only one action at a time can be performed.

    """
    args = setup_argparser()
    # ==============
    # Logging config
    # ==============
    # NOTE: if quiet and verbose are both activated, only quiet will have an
    # effect
    if args.quiet:  # Logging disabled
        # TODO: check why 2nd option is not already set to True by default
        logger = setup_basic_logger(__name__, remove_all_initial_handlers=True)
        logger.addHandler(NullHandler())
    else:  # Logging enabled
        if args.no_color:  # Color disabled
            uninstall_colored_logger()
        logger = setup_basic_logger(
            name=__name__,
            add_console_handler=True,
            remove_all_initial_handlers=True)
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    # =======
    # Actions
    # =======
    retcode = 1
    try:
        # TODO: make it so that we can perform more than 1 action at a time
        # NOTE: only one action at a time can be performed
        if args.diff_dirpaths:
            retcode = diff_sets_of_docs(args.diff_dirpaths[0],
                                        args.diff_dirpaths[1])
        elif args.fix_dirpath:
            retcode = fix_extensions(args.fix_dirpath)
        elif args.group_dirs:
            retcode = group_docs_into_folders(args.group_dirs[0],
                                              args.group_dirs[1],
                                              args.group_size)
        elif args.modify_dirpath:
            retcode = modify_filenames(args.modify_dirpath)
        elif args.show_dirpath:
            retcode = show_results_about_docs(args.show_dirpath)
        elif args.undo_fix:
            retcode = undo_fix_extensions(None)
        elif args.undo_group:
            retcode = undo_group_docs_into_folders(None)
        else:
            # TODO: default when no action given is to start scraping?
            print("No action selected: edit (-e), reset (-r) or start the "
                  "scraper (-s)")
    except (AssertionError, AttributeError, FileNotFoundError,
            KeyboardInterrupt, OSError) as e:
        # TODO: explain this line
        # traceback.print_exc()
        e = "<color>{}</color>".format(e)
        if args.verbose:
            logger.exception(e)
        else:
            logger.error(e)
    finally:
        return retcode


if __name__ == '__main__':
    retcode = main()
    msg = "\nProgram exited with <color>{}</color>".format(retcode)
    if retcode == 1:
        logger.error(msg)
    else:
        logger.debug(msg)
    """
    copy_documents(
        src_dirpath=os.path.expanduser('~/test/ebook_manager/ungrouped_docs'),
        dst_dirpath='/Volumes/Seagate Backup Plus Drive 3TB/ebooks/_tmp')
    # Examples: Coup.PDF and [Borel Comprendre physique].pdf.sb-ae97b7c9-d1SEqI
    # metadata = fix_extensions(os.path.expanduser('~/Downloads'))
    # undo_fix_extensions(metadata)
    show_results_about_docs(
        dirpath=os.path.expanduser('~/Downloads'),
    )
    diff_sets_of_docs(
        dirpath_set1=os.path.expanduser('~/Downloads'),
        dirpath_set2='/Volumes/Seagate Backup Plus Drive 3TB/ebooks/_tmp',
    )
    metadata = group_docs_into_folders(
        # src_dirpath=os.path.expanduser('~/Downloads'),
        # dst_dirpath=os.path.expanduser('~/Documents/ebooks/grouped_docs'),
        src_dirpath=os.path.expanduser('~/test/ebook_manager/ungrouped_docs'),
        dst_dirpath=os.path.expanduser('~/test/ebook_manager/grouped_docs'),
        group_size=5)
    undo_group_docs_into_folders(metadata)
    """

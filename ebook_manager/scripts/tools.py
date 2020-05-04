#!/usr/script/env python
"""Script for .

"""

import argparse
import glob
import logging
import math
import os
import pathlib
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
# For printing
_nb_items = 20
_nb_chars = 100


# TODO: add try except to functions


def _add_plural(list_or_number, pair=('', 's')):
    """TODO

    Parameters
    ----------
    list_
    pair

    Returns
    -------

    """
    # TODO: explain code
    if isinstance(list_or_number, list):
        nb_items = len(list_or_number)
    else:
        assert isinstance(list_or_number, int)
        nb_items = list_or_number
    return pair[1] if nb_items > 1 else pair[0]


def _copy_docs(src_dirpath, dst_dirpath, doc_types=_doc_types):
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


def _get_fnames(dirpath, doc_types=_doc_types, recursive=False):
    """TODO: filename rejected if it belongs to a directory

    Parameters
    ----------
    dirpath
    doc_types
    recursive

    Returns
    -------

    """
    # TODO: explain code
    results = namedtuple("results", "valid_fnames rejected_fnames rejected_ext")
    valid_fnames = []
    rejected_fnames = []
    rejected_ext = set()

    def process_fname(fname):
        """TODO

        Parameters
        ----------
        fname

        Returns
        -------

        """
        ext = os.path.splitext(fname)[-1][1:]
        # Reject if filename is associated to a directory
        if os.path.isfile(os.path.join(dirpath, fname)):
            if ext in doc_types:
                valid_fnames.append(fname)
            else:
                rejected_fnames.append(fname)
                rejected_ext.add(ext)

    if recursive:
        logger.info("Directory iterated <color>recursively</color>")
        for fname in glob.iglob(os.path.join(dirpath, '**/*'), recursive=True):
            if os.path.isfile(fname):
                process_fname(fname)
    else:
        for fname in os.listdir(dirpath):
            process_fname(fname)
    results.valid_fnames = valid_fnames
    results.rejected_fnames = rejected_fnames
    results.rejected_ext = rejected_ext
    return results


def _log_main_msg(msg, sign='='):
    """TODO

    Parameters
    ----------
    msg
    sign

    Returns
    -------

    """
    # TODO: explain code
    # 4 because of # at the beginning and end of middle message (+ space)
    nb_signs = len(msg) + 4
    signs = "<color>{}</color>".format(sign * nb_signs)
    # Log first line of signs
    logger.info(signs)
    # Log middle message
    logger.info("<color># {} #</color>".format(msg))
    # Log second line of signs
    logger.info(signs)


def _shorten_fname(fname, nb_chars=_nb_chars):
    """TODO

    Parameters
    ----------
    filename
    nb_chars

    Returns
    -------

    """
    # TODO: explain code
    root, ext = _split_fname(fname)
    short_root = "{}{}".format(root[:nb_chars],
                               "[...]" if len(root) > nb_chars else "")
    # Return short filename
    return "{}{}".format(short_root, ".{}".format(ext) if ext else "")


def _show_fnames_from_coll(coll, nb_items=_nb_items, nb_chars=_nb_chars, sort=True):
    """TODO

    Parameters
    ----------
    coll
    nb_items
    nb_chars
    sort

    Returns
    -------

    """
    # TODO: explain code
    coll = list(coll) if isinstance(coll, set) else coll
    coll = sorted(coll) if sort else coll
    if len(coll):
        coll = coll[:nb_items]
        for fname in coll:
            new_fname = _shorten_fname(fname, nb_chars)
            logger.info("- {}".format(new_fname))
    return 0


def _show_basic_fnames_results(results, nb_items=_nb_items, nb_chars=_nb_chars):
    """TODO

    Parameters
    ----------
    results
    nb_items
    nb_chars

    Returns
    -------

    """
    # TODO: explain code
    logger.info("Number of valid files: {}".format(len(results.valid_fnames)))
    # TODO: log only some of the filenames if not verbose. Otherwise log
    # the first 25
    # TODO: simulate TypeError with results.rejected_fnames (no len)
    nb_rejected_fnames = len(results.rejected_fnames)
    if nb_rejected_fnames > 0:
        logger.warning("<color>There {} {} rejected file{}</color>".format(
            _add_plural(nb_rejected_fnames, ('is', 'are')),
            nb_rejected_fnames,
            _add_plural(nb_rejected_fnames)))
        if nb_rejected_fnames > nb_items:
            msg = "Some of the rejected files:"
        else:
            msg = "Rejected files:"
        logger.info(msg)
        _show_fnames_from_coll(results.rejected_fnames,
                               nb_items=nb_items,
                               nb_chars=nb_chars,
                               sort=True)
    else:
        logger.info("There are 0 rejected files")
    nb_rejected_exts = len(results.rejected_ext)
    if nb_rejected_exts > 0:
        logger.warning("<color>There are {} rejected extensions</color>".format(
            nb_rejected_exts))
        logger.info("Rejected extensions: {}".format(results.rejected_ext))
    else:
        logger.info("There are 0 rejected extensions")


def _split_fname(fname):
    """TODO

    Parameters
    ----------
    fname

    Returns
    -------

    """
    # TODO: explain code
    root, ext = os.path.splitext(fname)
    ext = ext[1:]
    return root, ext


def _undo_fix_extensions(metadata):
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


def _undo_group_docs_into_folders(metadata):
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


def diff_sets_of_docs(dirpath_set1, dirpath_set2, doc_types=_doc_types,
                      nb_items=_nb_items, nb_chars=_nb_chars, recursive=False):
    """TODO

    Parameters
    ----------
    dirpath_set1
    dirpath_set2
    doc_types
    nb_items
    nb_chars
    recursive

    Returns
    -------

    """
    # TODO: explain code
    _log_main_msg(msg="Difference between two sets of documents")
    results1 = _get_fnames(dirpath_set1, doc_types, recursive=recursive)
    results2 = _get_fnames(dirpath_set2, doc_types, recursive=recursive)
    ipdb.set_trace()
    whole_results = [results1, results2]
    for i, dirpath in enumerate([dirpath_set1, dirpath_set2]):
        logger.info("Results for set{}: <color>{}</color>".format(i+1, dirpath))
        results = whole_results[i]
        _show_basic_fnames_results(results, nb_items=nb_items, nb_chars=nb_chars)
        other_idx = 1 if i == 0 else 0
        diff = set(results.valid_fnames) - \
               set(whole_results[other_idx].valid_fnames)
        nb_diff = len(diff)
        if nb_diff > 0:
            logger.warning("<color>There {} {} difference{} between set{} and "
                           "set{}</color>".format(
                            _add_plural(nb_diff, ('is', 'are')),
                            nb_diff,
                            _add_plural(nb_diff),
                            i + 1,
                            other_idx + 1))
            if nb_diff > nb_items:
                msg = "Some of the differences"
            else:
                msg = "Difference"
            logger.info("{} between set{} and set{}:".format(
                msg,
                i+1,
                other_idx+1))
            _show_fnames_from_coll(coll=diff,
                                   nb_items=nb_items,
                                   nb_chars=nb_chars,
                                   sort=True)
        else:
            logger.info("There are 0 differences between set{} and set{}".format(
                i + 1,
                other_idx + 1))
        if i == 0:
            logger.info("")
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
    _log_main_msg(msg="Fix file extensions in {}".format(dirpath))
    metadata = namedtuple("metadata", "retcode new_filepaths")
    metadata.new_filepaths = []
    new_filepaths = []
    for filename in os.listdir(dirpath):
        src_filepath = os.path.join(dirpath, filename)
        root, ext = _split_fname(filename)
        if ext and os.path.isfile(src_filepath) and ext not in doc_types:
            fixed = False
            logger.debug("<color>Trying to fix {} ...</color>".format(filename))
            if ext.lower() in doc_types:
                # Fix 1: lowercase extension
                logger.debug("<color>Fixed file extension with lowercase"
                             "</color>")
                ext = ext.lower()
                fixed = True
            elif filename.count('.') > 1:
                # Fix 2: remove everything after the extension and lowercase
                # newly found extension
                # e.g. file.pdf.sb1-383921a --> file.pdf
                root2, ext2 = _split_fname(root)
                ext2 = ext2.lower()
                if ext2 in doc_types:
                    logger.debug("<color>Fixed file extension by removing outer "
                                 "extension</color>")
                    root = root2
                    ext = ext2
                    fixed = True
            if fixed:
                new_filename = "{}.{}".format(root, ext)
                dst_filepath = os.path.join(dirpath, new_filename)
                logger.info("<color>Fixed filename:</color> {} <color>TO</color> "
                            "{}".format(
                             filename,
                             new_filename))
                shutil.move(src_filepath, dst_filepath)
                new_filepaths.append((src_filepath, dst_filepath))
            else:
                logger.warning("<color>Filename couldn't be fixed:</color> "
                               "{}".format(filename))
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
    _log_main_msg(msg="Group documents into folders")
    metadata = namedtuple("metadata", "retcode src_dirpath folderpaths")
    metadata.src_dirpath = src_dirpath
    folderpaths = []
    # Get list of documents and keep only valid documents (based on types)
    results = _get_fnames(src_dirpath, doc_types)
    valid_fnames = results.valid_fnames
    # Group valid documents into folders
    group_id = 0
    n_groups = math.ceil(len(valid_fnames)/group_size)
    logger.info("<color>Source directory:</color> {}".format(src_dirpath))
    logger.info("<color>Destination directory:</color> {}".format(dst_dirpath))
    logger.info("Number of valid documents: {}".format(len(valid_fnames)))
    logger.info("Number of groups: {}".format(n_groups))
    logger.info("Group size: {}".format(group_size))
    logger.debug("")
    for i in range(0, len(valid_fnames), group_size):
        logger.debug("<color>Group {}</color>".format(group_id))
        group = valid_fnames[i:i+group_size]
        # Create folder for the group of documents
        group_folderpath = os.path.join(dst_dirpath,
                                        "{}{}".format(prefix_fname, group_id))
        group_id += 1
        # TODO: use create_dir() from pyutils.genutils
        # TODO: case where group folder already exists
        if not os.path.exists(group_folderpath):
            logger.debug("<color>Creating folder:</color> {}".format(
                group_folderpath))
        pathlib.Path(group_folderpath).mkdir(parents=True)
        folderpaths.append(group_folderpath)
        for filename in group:
            src_filepath = os.path.join(src_dirpath, filename)
            dst_filepath = os.path.join(group_folderpath, filename)
            logger.debug("<color>Moving file</color> {}".format(
                _shorten_fname(filename)))
            shutil.move(src_filepath, dst_filepath)
        # TODO: simulate error by not proving msg to logger, e.g. logger.debug()
        logger.debug("")
    metadata.folderpaths = folderpaths
    metadata.retcode = 0
    return metadata


def modify_fnames(dirpath, doc_types=_doc_types, recursive=False):
    """TODO

    Parameters
    ----------
    dirpath
    doc_types
    recursive

    Returns
    -------

    """
    # TODO: explain code
    _log_main_msg(msg="Modify filenames from {}".format(dirpath))
    ipdb.set_trace()
    results = _get_fnames(dirpath, doc_types)
    for root, dirs, files in os.walk(dirpath):
        # Remove parentheses and brackets at the beginning of the filename along
        # with their content
        pass
    return 0


def show_results_about_docs(dirpath, doc_types=_doc_types, nb_items=_nb_items,
                            nb_chars=_nb_chars, recursive=False):
    """

    Parameters
    ----------
    dirpath
    doc_types
    nb_items
    nb_chars
    recursive

    Returns
    -------

    """
    # TODO: explain code
    _log_main_msg(msg="Show basic results about documents: {}".format(dirpath))
    results = _get_fnames(dirpath, doc_types, recursive=recursive)
    _show_basic_fnames_results(results, nb_items=nb_items, nb_chars=nb_chars)
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
    # TODO: explain code
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
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Recursively iterate through directories")
    # help=argparse.SUPPRESS)
    # Group arguments that are closely related
    # ======================================
    # Difference between 2 sets of documents
    # ======================================
    diff_sets_group = parser.add_argument_group("Print differences between two "
                                                "sets of documents")
    diff_sets_group.add_argument(
        "--diff_dirs", nargs=2, dest="diff_dirpath",
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
        "--group_dirs", nargs=2, dest="group_dirpath",
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
    # TODO: explain code
    # TODO: global logger?
    args = setup_argparser()
    # ==============
    # Logging config
    # ==============
    # NOTE: if quiet and verbose are both activated, only quiet will have an
    # effect
    if args.quiet:  # Logging disabled
        # Reset logger by removing all handlers and add a null handler
        logger = setup_basic_logger(__name__, remove_all_initial_handlers=True)
        logger.addHandler(NullHandler())
    else:  # Logging enabled
        if args.no_color:  # Color disabled
            uninstall_colored_logger()
        # Setup a basic CONSOLE logger with DEBUG as log level
        logger = setup_basic_logger(
            name=__name__,
            add_console_handler=True,
            remove_all_initial_handlers=True)
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    if args.recursive:
        logger.debug("<color>Recursive is ON</color>")
    # =======
    # Actions
    # =======
    retcode = 1
    try:
        # TODO: make it so that we can perform more than 1 action at a time
        # NOTE: only one action at a time can be performed
        if args.diff_dirpath:
            retcode = diff_sets_of_docs(args.diff_dirpath[0],
                                        args.diff_dirpath[1],
                                        recursive=args.recursive)
        elif args.fix_dirpath:
            metadata = fix_extensions(args.fix_dirpath)
            retcode = metadata.retcode
            # TODO: comment if finished testing
            # retcode = _undo_fix_extensions(metadata)
        elif args.group_dirpath:
            metadata = group_docs_into_folders(args.group_dirpath[0],
                                               args.group_dirpath[1],
                                               args.group_size)
            retcode = metadata.retcode
            # TODO: comment if finished testing
            # retcode = _undo_group_docs_into_folders(metadata)
        elif args.modify_dirpath:
            retcode = modify_fnames(args.modify_dirpath)
        elif args.show_dirpath:
            retcode = show_results_about_docs(args.show_dirpath,
                                              recursive=args.recursive)
        else:
            logger("No action selected")
    except Exception as e:
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
    # python -m ebook_manager.scripts.tools --diff_dirs ~/Downloads ~/Documents/ebooks/ebooks_01/
    # python -m ebook_manager.scripts.tools --fix_dir ~/test/ebook_manager/fix_extensions/
    # python -m ebook_manager.scripts.tools --group_dirs ~/test/ebook_manager/ungrouped_docs/ ~/test/ebook_manager/grouped_docs/
    # python -m ebook_manager.scripts.tools -show ~/Downloads/chrome_downloads/
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

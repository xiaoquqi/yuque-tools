#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Program to Download Images from Yuque Markdown Documents
#
# This program downloads images embedded in Yuque markdown
# documents and saves them locally.
# Additionally, it ensures that the markdown formatting is
# preserved by adding necessary line breaks.
#
# Author: Ray Sun <xiaoquqi@gmail.com>
# Version: 0.1
# Date: June 19, 2024


import argparse
import logging
import os
import shutil
import sys

from yuque_tools.utils import init_logging
from yuque_tools.yuque import Yuque

DEFAULT_IMAGE_PATH = "_images"
DEFAULT_BACKUP_PATH = ".bak"


def parse_sys_args(argv):
    """Parses commaond-line arguments"""
    parser = argparse.ArgumentParser(
        description="Yuque images downlaoder.")
    parser.add_argument(
        "-d", "--debug", action="store_true", dest="debug",
        default=False, help="Enable debug message.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", dest="verbose",
        default=True, help="Show message in standard output.")
    parser.add_argument(
        "-p", "--markdown-dir",
        type=str,
        help="Directory containing Yuque exported markdown files"
    )
    parser.add_argument(
        "-i", "--image-download-dir",
        type=str,
        default=DEFAULT_IMAGE_PATH,
        help=(
            f"Directory to save downloaded images (default is "
            f"{DEFAULT_IMAGE_PATH} at the same level of markdown "
            f"file)"
        )
    )
    parser.add_argument(
        "-b", "--backup",
        action="store_true",
        default=False,
        help="Backup original markdown files before processing "
             "(default: False, backup to .bak in the same level as "
             "markdown dir)"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        return vars(parser.parse_args(argv[1:]))


def handle_markdown(markdown_dir, image_download_dir):
    yuque = Yuque(markdown_dir, image_download_dir)
    yuque.format()


def backup(src_dir):
    """Backup given markdown dir"""
    src_filename = os.path.basename(src_dir)
    src_full_path = os.path.abspath(src_dir)

    backup_filename = "%s%s" % (src_filename, DEFAULT_BACKUP_PATH)
    backup_full_path = os.path.join(
        os.path.dirname(src_full_path), backup_filename)

    if os.path.exists(backup_full_path):
        logging.warning(f"Removing backup dir {backup_full_path}")
        shutil.rmtree(backup_full_path)
        logging.info(f"Removed backup dir {backup_full_path}")

    logging.info(f"Backuping {src_full_path} to {backup_full_path}...")
    shutil.copytree(src_full_path, backup_full_path)
    logging.info(f"Success to backup {src_full_path} to {backup_full_path}.")


def main():
    args = parse_sys_args(sys.argv)
    init_logging(debug=args["debug"], verbose=args["verbose"])

    markdown_dir = args["markdown_dir"]
    image_download_dir = args["image_download_dir"]

    if not os.path.exists(markdown_dir):
        logging.error(f"{markdown_dir} is not exists, please check.")
        sys.exit(1)

    if args["backup"]:
        backup(markdown_dir)

    handle_markdown(markdown_dir, image_download_dir)


if __name__ == "__main__":
    main()

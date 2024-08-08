#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Program to Format Markdown
#
# Author: Ray Sun <xiaoquqi@gmail.com>
# Version: 0.1
# Date: June 19, 2024


import argparse
import logging
import os
import shutil
import sys

from yuque_tools.utils import utils
from yuque_tools.utils.markdown_formatter import MarkdownFormatter

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


def main():
    args = parse_sys_args(sys.argv)
    utils.init_logging(debug=args["debug"], verbose=args["verbose"])

    markdown_dir = args["markdown_dir"]
    markdown_path = str(os.path.abspath(markdown_dir))

    if not os.path.exists(markdown_dir):
        logging.error(f"{markdown_dir} is not exists, please check.")
        sys.exit(1)

    if args["backup"]:
        utils.backup(markdown_dir)

    md_files = utils.find_md_files(markdown_path)
    if not md_files:
        logging.warning("No markdown file found")
        sys.exit(1)

    for md_file in md_files:
        logging.info(f"Starting to format markdown for {md_file}")
        image_downloader = MarkdownFormatter(md_file)
        image_downloader.format()
        logging.info(f"Finish formatting markdown for {md_file}")


if __name__ == "__main__":
    main()
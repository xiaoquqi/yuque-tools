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
import sys

from yuque_tools.utils import utils
from yuque_tools.utils.markdown_handler import MarkdownHandler


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
    converted_path = markdown_path + ".converted"

    if not os.path.exists(markdown_dir):
        logging.error(f"{markdown_dir} is not exists, please check.")
        sys.exit(1)

    if not os.path.exists(converted_path):
        os.makedirs(converted_path)
        logging.info(f"Created converted directory at {converted_path}")

    md_files = utils.find_md_files(markdown_path)
    if not md_files:
        logging.warning("No markdown file found")
        sys.exit(1)

    for md_file in md_files:
        logging.info(f"Converting {md_file} to Word document...")
        
        # Get the relative path from markdown_path
        rel_path = os.path.relpath(md_file, markdown_path)
        rel_path_parts = rel_path.split(os.sep)
        
        # Process and rename directories/files
        current_path = markdown_path
        processed_parts = []
        
        for i, part in enumerate(rel_path_parts):
            # Process name - replace brackets and remove spaces
            processed = part.replace('［', '(').replace('］', ')')  # Full-width
            processed = processed.replace('[', '(').replace(']', ')')  # Half-width
            processed = processed.replace(' ', '')
            
            old_path = os.path.join(current_path, part)
            new_path = os.path.join(current_path, processed)
            
            # Rename if needed
            if old_path != new_path and os.path.exists(old_path):
                os.rename(old_path, new_path)
                logging.debug(f"Renamed {old_path} to {new_path}")
            
            current_path = new_path
            processed_parts.append(processed)
        
        processed_rel_path = os.path.join(*processed_parts)
        processed_full_path = os.path.join(markdown_path, processed_rel_path)
        
        # Create output path with .docx extension
        output_file = os.path.join(
            converted_path,
            os.path.splitext(processed_rel_path)[0] + '.docx'
        )
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        logging.debug(f"Output file will be saved to {output_file}")

        md_handler = MarkdownHandler(processed_full_path)
        markdown_content = md_handler.to_docx(output_file)
        logging.info(
            f"Successfully converted {processed_full_path} to {output_file}"
        )


if __name__ == "__main__":
    main()

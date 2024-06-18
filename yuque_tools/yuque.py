import glob
import logging
import os
import re
import requests


class Yuque:

    def __init__(self, markdown_dir, image_download_dir):
        self.markdown_dir = markdown_dir
        self.image_download_dir = image_download_dir

        self.markdown_path = str(os.path.abspath(self.markdown_dir))

    def _find_md_files(self, search_path, ext_name="md"):
        logging.info(f"Searching markdown files in {search_path}")
        search_pattern = "*.%s" % ext_name
        md_files = glob.glob(
            os.path.join(search_path, "**", search_pattern),
            recursive=True)
        return md_files

    def _handle_markdown(self, md_path):
        base_file_path = os.path.dirname(md_path)
        image_full_path = os.path.join(base_file_path, self.image_download_dir)
        image_relative_path = "./%s" % self.image_download_dir

        # Ensure images path is exists
        if not os.path.exists(image_full_path):
            os.makedirs(image_full_path)

        with open(md_path, "r") as rfhd:
            lines = rfhd.readlines()

            # if we need to add \n after line
            is_add_newline = False

            # In code area, ignore start #
            is_code_start = False

            for index, line in enumerate(lines):
                logging.debug("----------------")
                logging.debug("Current Line is: %s" % line.strip())
                logging.debug("----------------")

                # Ignore code start or markdown metdata start
                if re.match(r"^\s*```", line) or re.match(r"^\s*---", line):
                    is_code_start = not is_code_start
                logging.debug("if code start: [%s]%s" % (index, is_code_start))

                # We only add newline for content line, by default:
                #
                #   1. Empty Line
                #   2. Start with > Line
                #
                # will be ignored
                if re.match(r"^\s*$", line.strip()) or re.match(r"^\>", line):
                    logging.debug("Ignore line: %s" % line)
                    is_add_newline = False
                else:
                    if not is_code_start:
                        is_add_newline = True
                logging.debug("Need to add newline: %s" % is_add_newline)

                if is_add_newline:
                    logging.debug("Orig replace line is: |%s|" % line)
                    logging.debug("Will replace line to: %s\n" % line)
                    lines[index] = "%s\n" % line

                # Replace image, by default the image url will be:
                # ![image.png](https://cdn.nlark.com/yuque/path/xxxx.png#REMOVED_PART
                if re.match(r"!\[(.*?)\].*yuque", line):
                    find_pattern = re.compile(
                        r'https://.*?\.(jpeg|jpg|gif|png|svg|webp)')
                    match = find_pattern.search(line)
                    image_url = match.group()

                    md_basename = os.path.splitext(
                        os.path.basename(md_path))[0]
                    image_extname = os.path.splitext(
                        os.path.basename(image_url))[1]

                    image_name = "%s-%s%s" % (
                        md_basename, str(index), image_extname)
                    save_path = os.path.join(image_full_path, image_name)

                    logging.info("Downloading image %s to %s..." % (
                        image_url, save_path))

                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(save_path, "wb") as file:
                            file.write(response.content)
                    else:
                        logging.warning(
                            f"Skip to download image, status code "
                            f"is {response.status_code}")
                        continue

                    replace_image_line = "![%s](%s/%s)\n\n" % (
                        image_name, image_relative_path, image_name)
                    logging.debug("Old image line: %s" % line)
                    logging.debug("New image line: %s" % replace_image_line)
                    lines[index] = replace_image_line

            with open(md_path, "w+") as wfhd:
                wfhd.writelines(lines)

    def format(self):
        md_files = self._find_md_files(self.markdown_path)
        if not md_files:
            logging.warning("No markdown file found")
            return

        for md_file in md_files:
            logging.info(f"Handling markdown file {md_file}")
            self._handle_markdown(md_file)

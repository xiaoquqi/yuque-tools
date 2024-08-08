import logging
import os
import re
import requests


class YuqueImageDownloder(object):

    def __init__(self, md_path, image_download_dir):
        self.md_path = md_path
        self.image_download_dir = image_download_dir

    def download(self):
        base_file_path = os.path.dirname(self.md_path)

        with open(self.md_path, "r") as rfhd:
            lines = rfhd.readlines()
            lines = self._download_images(lines, base_file_path)

            with open(self.md_path, "w+") as wfhd:
                wfhd.writelines(lines)

    def _download_images(self, lines, base_file_path):
        """Download images and modify image links in markdown"""
        image_full_path = os.path.join(base_file_path, self.image_download_dir)
        image_relative_path = "./%s" % self.image_download_dir

        # Ensure images path is exists
        if not os.path.exists(image_full_path):
            os.makedirs(image_full_path)

        for index, line in enumerate(lines):
            # Replace image, by default the image url will be:
            # ![image.png](https://cdn.nlark.com/yuque/path/xxxx.png#REMOVED_PART
            if re.match(r"!\[(.*?)\].*yuque", line):
                logging.debug(f"Found image line: {line}")
                find_pattern = re.compile(
                    r'https://.*?\.(jpeg|jpg|gif|png|svg|webp)')
                match = find_pattern.search(line)
                image_url = match.group()

                md_basename = os.path.splitext(
                    os.path.basename(self.md_path))[0]
                image_extname = os.path.splitext(
                    os.path.basename(image_url))[1]

                # Use index line number for image name
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

        return lines
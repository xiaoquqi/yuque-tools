import logging
import os
import re
import requests
from pypinyin import lazy_pinyin

from yuque_tools.utils.image_converter import convert_image_to_png


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
                
                # Convert Chinese to pinyin and keep only alphanumeric characters
                md_basename = ''.join(lazy_pinyin(md_basename))
                md_basename = re.sub(r'[^a-zA-Z0-9]', '', md_basename)

                image_extname = os.path.splitext(
                    os.path.basename(image_url))[1]

                # Use index line number for image name
                image_name = "%s-%s%s" % (
                    md_basename, str(index), image_extname)
                save_path = os.path.join(image_full_path, image_name)

                if os.path.exists(save_path):
                    logging.warn(f"Skip to download image from {image_url} "
                                 f"due to image is already exists in {save_path}")
                    continue

                logging.info("Downloading image %s to %s..." % (
                    image_url, save_path))

                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(save_path, "wb") as file:
                        file.write(response.content)
                        
                    # Convert the downloaded image to PNG format
                    try:
                        converted_path = convert_image_to_png(save_path)
                        if converted_path != save_path:
                            # Update image name and path if conversion was successful
                            image_name = os.path.basename(converted_path)
                            save_path = converted_path
                    except Exception as e:
                        logging.error(f"Failed to convert image {save_path}: {str(e)}")
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
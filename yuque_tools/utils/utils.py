import glob
import logging
import os

# Log settings
DEFAULT_PATH = "logs"
LOG_FORMAT = "%(asctime)s %(process)s %(levelname)s [-] (%(threadName)-9s) %(message)s"

# Backup
DEFAULT_BACKUP_PATH = ".bak"


def init_logging(debug=False, verbose=True,
                 log_file=None, log_path=None):
    """Initilize logging for common usage

    By default, log will save at logs dir under current running path.
    """

    logger = logging.getLogger()

    # Clean all logger register to root
    for handler in logger.handlers:
        logger.removeHandler(handler)

    log_level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(log_level)

    # Set console handler
    if verbose:
        console = logging.StreamHandler()
        console.setLevel(log_level)
        console.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
        logger.addHandler(console)

    if log_file:
        if not log_path:
            log_path = DEFAULT_PATH

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_path = os.path.join(log_path, log_file)

        fileout = logging.FileHandler(log_path, "a")
        fileout.setLevel(log_level)
        fileout.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
        logger.addHandler(fileout)


def get_proxies(kwargs={}):
    """Return proxies dict with http proxy and https proxy"""
    http_proxy = kwargs.get("http_proxy",
                            os.environ.get("HTTP_PROXY", None))
    https_proxy = kwargs.get("https_proxy",
                             os.environ.get("HTTPS_PROXY", None))

    return {
        "http_proxy": http_proxy,
        "https_proxy": https_proxy
    }

def backup(source_dir):
    """Backup source dir to backup dir"""
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

def find_md_files(search_path, ext_name="md"):
    logging.info(f"Searching markdown files in {search_path}")
    search_pattern = "*.%s" % ext_name
    md_files = glob.glob(
        os.path.join(search_path, "**", search_pattern),
        recursive=True)
    return md_files
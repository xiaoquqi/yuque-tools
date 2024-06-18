import logging
import os

# Log settings
DEFAULT_PATH = "logs"
LOG_FORMAT = "%(asctime)s %(process)s %(levelname)s [-] (%(threadName)-9s) %(message)s"


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


def get_proxies(self, kwargs={}):
    """Return proxies dict with http proxy and https proxy"""
    http_proxy = kwargs.get("http_proxy",
                            os.environ.get("HTTP_PROXY", None))
    https_proxy = kwargs.get("https_proxy",
                             os.environ.get("HTTPS_PROXY", None))

    return {
        "http_proxy": http_proxy,
        "https_proxy": https_proxy
    }

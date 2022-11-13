import logging

from pizza_place_insights.config import get_settings


def configure_logging() -> None:
    """Configure logs for the entire package"""

    log = logging.getLogger(__package__)
    log.handlers = []
    log.setLevel(get_settings().log_level)

    # [time][level(number)]: message
    LOGFORMAT = "[%(asctime)s][%(levelno)s]: %(message)s"
    formatter = logging.Formatter(LOGFORMAT)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(0)
    log.addHandler(handler)

    # save logs to file if a file path is defined
    if file_path := get_settings().log_file_path:
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(0)
        log.addHandler(file_handler)

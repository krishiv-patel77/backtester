import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = (
    "%(asctime)s %(levelname)s %(message)s "
    "[%(pathname)s:%(funcName)s:%(lineno)d]"
)

class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(log_level: str = LogLevels.error):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]       # Make a list of all possible log level values

    # if the user passed in an invalid log_level, then configure an error which immediately just logs an error to console
    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    # if the user passed in "DEBUG" then we start it up in debug mode and use the format we specified above
    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    # otherwise just instantiate it with whatever other log level (Info or Warn)
    logging.basicConfig(level=log_level)

"""Utility module for this application logger."""


# Official Libraries
import logging
import logging.handlers
import os
import sys


# My Modules
from stobu.systempaths import USR_CACHE_DIR


# Define Formatters
FILE_FORMATTER = logging.Formatter("[%(levelname)s:%(asctime)s:%(module)s]: %(message)s")
"""Format for a log file."""

SIMPLE_FORMATTER = logging.Formatter("%(asctime)s: %(message)s")
"""Format as a simple style."""

DEBUG_FORMATTER = logging.Formatter("%(levelname)-8s %(asctime)s [%(module)s.%(funcName)s:%(lineno)s]:%(message)s")
"""Format for debug."""


# Define Application Directories
APP_CACHE_DIR = os.path.join(USR_CACHE_DIR, 'storybuilder')
"""str: path of this application cache directory."""

if not os.path.exists(USR_CACHE_DIR):
    os.makedirs(USR_CACHE_DIR)

if not os.path.exists(APP_CACHE_DIR):
    os.makedirs(APP_CACHE_DIR)


# Setup Log file
LOG_FILENAME = os.path.join(APP_CACHE_DIR, "storybuilder.log")
loghandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20971520, backupCount=5)
loghandler.setFormatter(FILE_FORMATTER)


# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(loghandler)


# Set the logging level to show debug messages.
console_handler = logging.StreamHandler(stream=sys.stderr)
console_handler.setFormatter(SIMPLE_FORMATTER)
logger.addHandler(console_handler)


# Set the debug level for this application.
if __debug__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

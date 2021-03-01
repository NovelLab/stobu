"""System paths defined."""


# Official Libraries
import os


# Define basic system paths
HOME = os.environ['HOME']
"""str: path of user home directory."""

USR_CACHE_DIR = os.path.join(HOME, '.cache')
"""str: path of user cache directory."""

USR_CONFIG_DIR = os.path.join(HOME, '.config')
"""str: path of user config directory."""


"""Define paths of user."""

# Official Libraries
import os


# Define Constants
HOME = os.environ['HOME']
"""str: path of user home directory."""

USER_CACHE_DIR = os.path.join(HOME, '.cache')
"""str: path of user cache directory."""

USER_CONFIG_DIR = os.path.join(HOME, '.config')
"""str: path of user config directory."""

from enum import Enum


class Action(Enum):
    COPY_FILE = "copy file"
    DELETE_PATH = "delete path"
    COUNT_FILES = "count files"
    FIND_FILES = "find files"
    ADD_CREATION_DATE = "add creation date"
    ANALYSE_FOLDER = "analyse folder"


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

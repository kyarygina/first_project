import os
from os.path import getsize, join
import re
import shutil
from datetime import datetime


def copy_file(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    directory, filename = os.path.split(path)
    name, ext = os.path.splitext(filename)

    new_filename = f"{name}_copy{ext}"
    new_path = os.path.join(directory, new_filename)

    shutil.copy2(path, new_path)
    return new_path


def delete_path(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")

    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)


def count_files(path: str):
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: {path}")

    total = 0
    for root, _, files in os.walk(path):
        total += len(files)

    return total


def find_files(path: str, pattern: str):
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: {path}")

    regex = re.compile(pattern)
    matched = []

    for root, _, files in os.walk(path):
        for file in files:
            if regex.search(file):
                matched.append(os.path.join(root, file))

    return matched


def add_creation_date(path: str, recursive: bool = False):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    paths = []

    if os.path.isfile(path):
        paths = [path]
    else:
        if recursive:
            for root, _, files in os.walk(path):
                for f in files:
                    paths.append(os.path.join(root, f))
        else:
            for f in os.listdir(path):
                full = os.path.join(path, f)
                if os.path.isfile(full):
                    paths.append(full)

    renamed = []

    for file_path in paths:
        stat = os.stat(file_path)
        created = datetime.fromtimestamp(stat.st_ctime)
        date_str = created.strftime("%Y-%m-%d")

        directory, filename = os.path.split(file_path)
        new_name = f"{date_str}_{filename}"
        new_path = os.path.join(directory, new_name)

        os.rename(file_path, new_path)
        renamed.append(new_path)

    return renamed


def analyse_folder(path: str):
    if not os.path.isdir(path):
        raise NotADirectoryError(path)

    total_size = 0
    level_data = {}

    for item in os.listdir(path):
        full_path = os.path.join(path, item)

        size = 0
        if os.path.isfile(full_path):
            size = os.path.getsize(full_path)
        else:
            for root, _, files in os.walk(full_path):
                for f in files:
                    file_path = join(root, f)
                    size += getsize(file_path)

        level_data[item] = size
        total_size += size

    return total_size, level_data

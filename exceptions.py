import os


class FileError(Exception):
    pass


def assert_file_exist(file_path):
    if not os.path.exists(file_path):
        raise FileError('File {} not exist'.format(file_path))


def assert_file_from_format(file_path, _format):
    if os.path.basename(file_path).split('.')[1] != _format:
        raise FileError('File {0} should be in {1} format'.format(file_path, _format))

import inspect


def print_link_to_modules(file=None, line=None):
    """ Print a link in PyCharm to a line in file.
        Defaults to line where this function was called. """
    if file is None:
        file = inspect.stack()[1].filename
    if line is None:
        line = inspect.stack()[1].lineno
    string = f'{file}:{max(line, 1)}: '.replace("\\", "/")
    return string

import functools

from custom_moduls.console_design.colors import ConsoleColors as CCol
from custom_moduls.console_design.indentation_levels import indentation_levels as Ilvl


def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        start_creating_files = time.time()
        print(f'{Ilvl(1)}Start: "{func.__name__}".')

        res = func(*args, **kwargs)

        end_creating_files = time.time() - start_creating_files
        print(f'{Ilvl(1)}End: "{func.__name__}". Time:', round(end_creating_files, 3), end='\n\n')

        return res
    return wrapper


def response_status_code_color(status_code):

    if 200 <= status_code <= 299:
        return CCol.txt_grn(status_code)
    elif 400 <= status_code <= 599:
        return CCol.txt_red(status_code)
    else:
        return CCol.txt_yel(status_code)


def log_api_status(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):

        input_data = args[2]

        func_name = func.__name__.capitalize().replace('_', ' ')
        system_file_name = input_data.get('system_file_name')

        console_log = f'{Ilvl(2)}{func_name}: "{system_file_name}"'

        print(f'{console_log}...', end=' ')

        response = func(*args, **kwargs)

        status_code = response_status_code_color(response.status_code)

        print(f'\r{console_log} {status_code}')

        return response

    return _wrapper


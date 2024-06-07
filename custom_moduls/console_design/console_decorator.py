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


def _response_status_code_and_data(response):
    status_code = response.status_code

    if 200 <= status_code <= 299:
        colored_status_code = CCol.txt_grn(status_code)

    elif 400 <= status_code <= 499:
        colored_status_code = CCol.txt_red(status_code)
        status_code_data = f'{colored_status_code}\n{response.content}'

        return status_code_data

    elif 500 <= status_code <= 599:
        colored_status_code = CCol.txt_red(status_code)

    else:
        colored_status_code = CCol.txt_yel(status_code)

    return colored_status_code


def log_api_status(indentation_levels: int = 0):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):

            system_file_name = ''

            if len(args) >= 3:

                input_data = args[2]

                system_file_name = input_data.get('system_file_name')
                system_file_name = f': "{system_file_name}"'

            func_name = func.__name__.capitalize().replace('_', ' ')

            console_log = f'{Ilvl(indentation_levels)}{func_name}{system_file_name}'

            print(f'{console_log}...', end=' ')

            response = func(*args, **kwargs)

            print(f'\r{console_log} {_response_status_code_and_data(response)}')

            return response

        return _wrapper

    return _decorator


def log_file_operation(indentation_levels: int = 0, main_func: bool = False):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):

            file_name = ''

            if not main_func:

                attr = 'file_name'
                attrs = list(func.__code__.co_varnames)[:len(args)]

                if attr in attrs:

                    file_name_index = attrs.index(attr)
                    file_name = f': "{args[file_name_index]}"'

            func_name = func.__name__.lstrip('_').capitalize().replace('_', ' ')

            console_log = f'{Ilvl(indentation_levels)}{func_name}{file_name}'

            ending_text = ('...', ':')[main_func]

            print(f'{console_log}{ending_text}', end=(' ', '\n')[main_func])

            response = func(*args, **kwargs)

            if not main_func:

                if isinstance(response, Exception):

                    print(f'\r{console_log} {CCol.txt_red("FAIL")}')
                    print(f'{Ilvl(indentation_levels + 1)}Error: {CCol.txt_red(str(response))}')

                else:

                    print(f'\r{console_log} {CCol.txt_grn("DONE")}')
            else:
                print()

            return response

        return _wrapper

    return _decorator

import functools
import inspect

from dataclasses import dataclass, field
from datetime import datetime

from custom_moduls.console_design.colors import ConsoleColors as CCol
from custom_moduls.console_design.indentation_levels import indentation_levels as Ilvl


def benchmark(func):
    import time

    def wrapper(*args, **kwargs):

        # perf_counter() - float
        # perf_counter_ns() - int

        start_creating_files = time.time()
        print(f'{Ilvl(1)}Start: "{func.__name__}".')

        res = func(*args, **kwargs)

        end_creating_files = time.time() - start_creating_files
        print(f'{Ilvl(1)}End: "{func.__name__}". Time:', round(end_creating_files, 3), end='\n\n')

        return res
    return wrapper

def _time(spaces: bool = False) -> str:

    time_string = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]}]'

    if not spaces:
        return time_string

    return ' ' * len(time_string)

def _response_status_code_and_data(response, indentation_levels=0):
    status_code = response.status_code

    if 200 <= status_code <= 299:
        colored_status_code = CCol.txt_grn(status_code)

    elif 400 <= status_code <= 499:

        colored_status_code = CCol.txt_red(status_code)
        error_text = response.text

        if '\n' in error_text:

            error_text = error_text.split('\n')[:5] + ['...']
            error_text = [' ' * (indentation_levels + 1) + line for line in error_text]
            error_text = '\n' + '\n'.join(error_text)

        status_code_data = f'{colored_status_code}\n{_time()}{Ilvl(indentation_levels + 1)}Error: {error_text}'

        return status_code_data

    elif 500 <= status_code:
        colored_status_code = CCol.txt_red(status_code)

    else:
        colored_status_code = CCol.txt_yel(status_code)

    return colored_status_code


@dataclass
class FunctionData:
    class_name: str
    console_class_name: str
    args: dict = field(default_factory=dict)
    kwargs: dict = field(default_factory=dict)


def inspect_decorator(func, args, kwargs):

    func_name = func.__name__

    console_func_name = func_name.replace('_', ' ').lstrip().capitalize()

    args_name = inspect.getfullargspec(func).args

    full_args = dict(zip(args_name, args))

    return FunctionData(func_name, console_func_name, full_args, kwargs)

    # funcname = func.__name__
    # print("function {}()".format(funcname))
    #
    # # get description of function params expected
    # argspec = inspect.getfullargspec(func)
    #
    # # go through each position based argument
    # counter = 0
    # if argspec.args and type(argspec.args is list):
    #     for arg in args:
    #         # when you run past the formal positional arguments
    #         try:
    #             print(str(argspec.args[counter]) + "=" + str(arg))
    #             counter += 1
    #         except IndexError as e:
    #             # then fallback to using the positional varargs name
    #             if argspec.varargs:
    #                 varargsname = argspec.varargs
    #                 print("*" + varargsname + "=" + str(arg))
    #             pass

    # finally show the named varargs
    # if argspec.keywords:
    #     kwargsname = argspec.keywords
    #     for k, v in kwargs.items():
    #         print("**" + kwargsname + " " + k + "=" + str(v))


def log_api_status(indentation_levels: int = 0, additional_info: list = None):

    def _decorator(func):

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):

            func_info = inspect_decorator(func, args, kwargs)

            system_file_name = ''

            if 'input_data' in func_info.args:

                system_file_name = func_info.args['input_data'].get('system_file_name')
                system_file_name = f' "{system_file_name}"'

            add_info = ''

            if additional_info is not None:

                args_kwargs = {}
                args_kwargs.update(func_info.args)
                args_kwargs.update(func_info.kwargs)

                add_info =': ' + ' '.join([f'[{args_kwargs[info]}]' for info in additional_info if info in args_kwargs])

                # for info in additional_info:
                #
                #     if info in args_kwargs:
                #         add_info += f'[{args_kwargs[info]}]'

            console_log = f'{Ilvl(indentation_levels)}{func_info.console_class_name}{system_file_name}{add_info}'

            print(f'{_time()}{console_log}...', end=' ')

            response = func(*args, **kwargs)

            if isinstance(response, Exception):

                print(f'\r{_time()}{console_log}: {CCol.txt_red("FAIL")}')
                print(f'{_time(True)}{Ilvl(indentation_levels + 1)}Error: {CCol.txt_red(str(response))}')

            else:

                print(f'\r{_time()}{console_log}: {_response_status_code_and_data(response, indentation_levels)}')

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

            print(f'{_time()}{console_log}{ending_text}', end=(' ', '\n')[main_func])

            response = func(*args, **kwargs)

            if not main_func:

                if isinstance(response, Exception):

                    print(f'\r{_time()}{console_log}: {CCol.txt_red("FAIL")}')
                    print(f'{_time(True)}{Ilvl(indentation_levels + 1)}Error: {CCol.txt_red(str(response))}')

                else:

                    print(f'\r{_time()}{console_log}: {CCol.txt_grn("DONE")}')
            else:
                print()

            return response

        return _wrapper

    return _decorator

def _print_log_validation_rules_comparison(data: str, indent: str):

    for input_name, input_data in data.items():

        print(f'{_time()}{indent}Input name: {CCol.txt_vio(input_name)}', end='')

        if isinstance(input_data, str):

            print(f' - {CCol.txt_red(input_data)}')

        else:
            print()
            for column_name, column_data in input_data.items():

                print(f'{_time()}{indent * 2}Column name: {CCol.txt_blu(column_name)}', end='')

                if isinstance(column_data, str):
                    print(f' - {CCol.txt_red(column_data)}')

                else:

                    for option in column_data:
                        print(f'\n{_time()}{indent * 3}Option: {CCol.txt_cyn(option)}')

                        file_value = column_data[option]['file_value']
                        saved_value = column_data[option]['saved_value']

                        print(f'{_time()}{indent * 4}File value - {CCol.txt_yel(file_value)}')
                        print(f'{_time()}{indent * 4}Saved value - {CCol.txt_yel(saved_value)}', end='')

                    print()
        print()


def log_validation_rules_comparison(indentation_levels: int = 0):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):

            func_info = inspect_decorator(func, args, kwargs)

            console_log = f'{Ilvl(indentation_levels)}{func_info.console_class_name}: '

            print(f'{_time()}{console_log}...', end=' ')

            result = func(*args, **kwargs)

            if result is None:

                print(f'\r{_time()}{console_log}{CCol.txt_grn("PASS")}')

            else:

                print(f'\r{_time()}{console_log}{CCol.txt_red("HAVE INCONSISTENCIES")}')

                indent = Ilvl(indentation_levels + 2, symbol=' ')

                miss_data = result.get('miss_data')
                extra_data = result.get('extra_data')

                if miss_data:
                    print(f'{_time(True)}{Ilvl(indentation_levels + 1)}MISS DATA:')
                    _print_log_validation_rules_comparison(miss_data, indent)

                if extra_data:
                    print(f'{_time(True)}{Ilvl(indentation_levels + 1)}EXTRA DATA:')
                    _print_log_validation_rules_comparison(extra_data, indent)

            return result

        return _wrapper

    return _decorator

from custom_moduls.console_design.colors import ConsoleColors

import pytest


def test_errors_logs_comparison(input_name, errors):

    error_result = {}

    for error_type, error_values in errors.items():

        if error_values:

            for key, value in error_values.items():

                if value:

                    error_result.setdefault(error_type, {}).update({key: value})

    if error_result:

        text = []

        for error_type, error_values in error_result.items():

            error_type = ConsoleColors.txt_blu(f'{error_type} errors:'.capitalize())

            text.append(error_type)

            for not_have_error_from, list_errors in error_values.items():

                not_have_error_from = not_have_error_from.replace('_', ' ').capitalize()
                not_have_error_from = ConsoleColors.txt_vio(not_have_error_from)

                list_errors = ConsoleColors.txt_yel(list_errors)

                text.append(f'  {not_have_error_from}: {list_errors}')

        assert False, '\n' + '\n'.join(text)




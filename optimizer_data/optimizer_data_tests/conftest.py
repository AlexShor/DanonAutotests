import ast

import pytest


def pytest_addoption(parser):
    parser.addoption('--comparison_result', default='nan', action='store')


def pytest_generate_tests(metafunc):

    args_name = ['input_name', 'errors']

    if not set(args_name).difference(metafunc.fixturenames):

        comparison_result = metafunc.config.getoption("comparison_result")

        if comparison_result != 'nan':

            option_value = ast.literal_eval(comparison_result)
            metafunc.parametrize(args_name, option_value.items(), ids=option_value.keys())


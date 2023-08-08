import time
import os
import random
import io
from collections import Counter

from py_google_sheets.gsheets import GoogleSheets
from input_data import FillData, DataTypes, Spreadsheets, DataTypesErrorExceptions, InputTypeNameMatch
from input_data import ErrorLogTexts
from pages.site_data.urls import BaseUrls
from pages.api.base_api_requests import BaseApiRequests as ApiReq
from pages.site_data.credentials import Credentials as Creds
from console_design.colors import ConsoleColors as CCol

import pandas as pd
import ast

errors_regarding_obligatory_fields = []
type_errors = []
errors_with_non_negative_values = []


def extract_list_from_error_log(data, error_log_txt_obl, error_log_txt_type, error_log_txt_neg):
    data = data.split('\n\n')
    answer = [[error_log_txt_obl, []],
              [error_log_txt_type, []],
              [error_log_txt_neg, []]]

    for i in range(len(data)):
        if error_log_txt_obl in data[i]:
            data[i] = data[i][data[i].index(error_log_txt_obl) + len(error_log_txt_obl):]
            answer[0][1].extend(ast.literal_eval(data[i]))

        if error_log_txt_type in data[i]:
            data[i] = data[i][data[i].index(error_log_txt_type) + len(error_log_txt_type):]
            answer[1][1].extend(ast.literal_eval(data[i]))

        if error_log_txt_neg in data[i]:
            data[i] = data[i][data[i].index(error_log_txt_neg) + len(error_log_txt_neg):]
            answer[2][1].extend(ast.literal_eval(data[i]))

    return answer


def save_error_log(list_errors_regarding_obligatory_fields,
                   list_type_errors,
                   list_errors_with_non_negative_values,
                   file_name,
                   folder,
                   worksheets_name,
                   error_log_txt):
    data = []
    if len(list_errors_regarding_obligatory_fields) > 0:
        data.append(f'{error_log_txt.OBLIGATION} {str(list_errors_regarding_obligatory_fields)}')
    if len(list_type_errors) > 0:
        data.append(f'{error_log_txt.TYPE} {str(list_type_errors)}')
    if len(list_errors_with_non_negative_values) > 0:
        data.append(f'{error_log_txt.NEGATIVE} {str(list_errors_with_non_negative_values)}')

    file_path = rf'files/{folder}/error_logs/{worksheets_name}/'
    new_file_name = f'errors_{file_name}.txt'

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if os.path.exists(file_path + new_file_name):
        os.remove(file_path + new_file_name)

    error_txt_file = io.open(file_path + new_file_name, "w", encoding='utf-8')
    for i in range(len(data)):
        error_txt_file.write(data[i])
        if i < len(data) - 1:
            error_txt_file.write('\n\n')
    error_txt_file.close()

    print(f', "error_logs/{worksheets_name}/{new_file_name}".', end=' ')


def data_type_in_error_exceptions(file_name, column_name):
    for file_column in DataTypesErrorExceptions.DATA:
        if file_column == [file_name, column_name]:
            return True
    return False


def create_error_log(data_type, current_row, column_name, validity, del_value_nan,
                     negativity, nan_value, inverse_integrity, file_name, error_log_txt):
    error_text = f'{error_log_txt.ROW} {current_row + 2} - ' \
                 f'{error_log_txt.COLUMN} {column_name.lower()}'

    if inverse_integrity and data_type == DataTypes.INT:
        type_errors.append(error_text)
    elif data_type == DataTypes.DATE and del_value_nan:
        type_errors.append(error_text)
    else:
        if not validity:
            if not data_type_in_error_exceptions(file_name, column_name):
                type_errors.append(error_text)
        if del_value_nan and 'FALSE' in nan_value:
            errors_regarding_obligatory_fields.append(error_text)
        if negativity and (data_type == DataTypes.INT or data_type == DataTypes.DECIMAL):
            errors_with_non_negative_values.append(error_text)


# def increase_data_values(i, data_values, options_increasing_data_values):
#     for key, value in options_increasing_data_values.items():
#         if i % value['step'] == 0:
#             data_values[key] =


def negative_type(validity_of_type, negative_value, value, negativity):
    if 'FALSE' in negative_value:
        if validity_of_type:
            if negativity:
                return '-' + value
            else:
                return value
        else:
            return value
    elif 'TRUE' in negative_value:
        if negativity:
            return '-' + value
        else:
            return value
    return value


def nan_type(validity_of_type, nan_value, value, del_value):
    if 'FALSE' in nan_value:
        if validity_of_type:
            if del_value:
                return ''
            else:
                return value
        elif del_value:
            return ''
        else:
            return value
    elif 'TRUE' in nan_value:
        if del_value:
            return ''
        else:
            return value


def create_data(file_name, column_name, current_row, error_log_txt,
                data_type, nan_value, negative, create_error_logs, data_values,
                validity,
                del_value_nan=False,
                negativity=False,
                inverse_integrity=False,
                bool_false=False):
    if data_values is None:
        if data_type == '':
            return 'NO_DATA_TYPE'
        value = FillData.get_value(data_type, validity)
        if not validity:
            negativity = False
        value = nan_type(validity, nan_value, value, del_value_nan)
        if value != '':
            if data_type == DataTypes.BOOL and validity:
                if bool_false:
                    value = value.split(':')[0]
                    value = value.split('|')[random.randrange(2)]
                else:
                    value = value.split(':')[1]
                    value = value.split('|')[random.randrange(2)]
            if data_type == DataTypes.DECIMAL:
                value = negative_type(validity, negative, value, negativity)
                if inverse_integrity:
                    value = value[:value.index('.')]
            elif data_type == DataTypes.INT:
                value = negative_type(validity, negative, value, negativity)
                if inverse_integrity:
                    value += '.45'
        if create_error_logs:
            create_error_log(data_type, current_row, column_name, validity,
                             del_value_nan, negativity, nan_value, inverse_integrity, file_name, error_log_txt)
    else:
        value = data_values.get(column_name)
    return value


class InputFiles:
    @staticmethod
    def create_files(check_input_url,
                     error_log_txt=ErrorLogTexts.Eng,
                     params=None,
                     folder='files',
                     miss_worksheets=None,
                     invert_miss_worksheets=False,
                     only_files=None,
                     create_error_logs=True,
                     data_values=None,
                     increasing_data_values=False,
                     options_increasing_data_values=None):

        if params is None:
            # validity, del_value_nan=False, negativity=False, inverse_integrity=False, bool_false, [Fill 1//2 row]
            params = [[False, False, False, False, False],
                      [True, True, False, False, True, True],
                      [True, False, False, False, True, True],
                      [True, False, True, False, False],
                      [True, False, False, True, True],
                      [True, False, False, False, False]]

        tables, worksheets_names = GoogleSheets.pars(check_input_url, miss_worksheets, invert_miss_worksheets)
        start_creating_files = time.time()
        print('====Start creating files')

        for table in range(len(tables)):
            file_names = Counter([row[0].strip() for row in tables[table]][1:])

            if only_files is not None:
                file_names = {k: v for k, v in file_names.items() if k in only_files}

            folder_name = f'files/{folder}/{worksheets_names[table]}'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            for file_name in file_names.keys():
                start_creating = time.time()
                print(f'========Creating files: "{worksheets_names[table]}/{file_name}.csv"', end='')

                column_names = [row[1].strip() for row in tables[table] if row[0].strip() == file_name]
                data = [[] for _ in range(len(params))]
                for i in range(len(params)):
                    current_row = i
                    for column_name in column_names:
                        for row in tables[table]:
                            table_file_name = row[0].strip()
                            table_column_name = row[1].strip()
                            table_data_type = row[2].strip().upper()
                            table_nan_value = row[3].strip().upper()
                            table_negative = row[4].strip().upper()
                            if table_file_name == file_name and table_column_name == column_name:
                                if len(params[i]) > 5 and params[i][5]:
                                    params[i][1] = not params[i][1]
                                    data[i].append(create_data(file_name, column_name, current_row,
                                                               error_log_txt,
                                                               table_data_type,
                                                               table_nan_value,
                                                               table_negative,
                                                               create_error_logs,
                                                               data_values,
                                                               *params[i][:-1]))
                                    break
                                else:
                                    data[i].append(create_data(file_name, column_name, current_row,
                                                               error_log_txt,
                                                               table_data_type,
                                                               table_nan_value,
                                                               table_negative,
                                                               create_error_logs,
                                                               data_values,
                                                               *params[i]))
                                    break
                    # if data_values is not None and increasing_data_values:
                    #     data_values = increase_data_values(i, data_values, options_increasing_data_values)

                if create_error_logs:
                    save_error_log(errors_regarding_obligatory_fields,
                                   type_errors,
                                   errors_with_non_negative_values,
                                   file_name,
                                   folder,
                                   worksheets_names[table],
                                   error_log_txt)

                errors_regarding_obligatory_fields.clear()
                type_errors.clear()
                errors_with_non_negative_values.clear()

                file_path = rf'{folder_name}/{file_name}.csv'
                if os.path.exists(file_path):
                    os.remove(file_path)

                df = pd.DataFrame(data, columns=column_names)
                df.to_csv(file_path, index=False, encoding="utf_8_sig")

                end_creating = time.time() - start_creating
                print(f' =={CCol.txt_grn("DONE")}: ', round(end_creating, 3))

        end_creating_files = time.time() - start_creating_files
        print('====End creating files. Time:', round(end_creating_files, 3), end='\n\n')

    @staticmethod
    def get_input_file_from_spreadsheet(check_input_url,
                                        folder='files',
                                        miss_worksheets=None,
                                        invert_miss_worksheets=False):

        spreadsheet, worksheets_names = GoogleSheets.pars(check_input_url, miss_worksheets, invert_miss_worksheets)
        start_time = time.time()
        print('==Start creating files')

        folder_name = 'files/' + folder
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for i in range(len(spreadsheet)):
            file_name = worksheets_names[i].strip()

            start_creating_file = time.time()
            print(f'====Creating file: "{file_name}.csv".', end=' ')

            column_names = spreadsheet[i][0]
            data = spreadsheet[i][1:]

            file_path = rf'{folder_name}/{file_name}.csv'
            if os.path.exists(file_path):
                os.remove(file_path)

            df = pd.DataFrame(data, columns=column_names)
            df.to_csv(file_path, index=False, encoding="utf_8_sig")

            end_creating_file = time.time() - start_creating_file
            print(f'=={CCol.txt_grn("DONE")}: ', round(end_creating_file, 3))

        end_time = time.time() - start_time
        print('====End creating files. Time:', round(end_time, 3), end='\n\n')

    class ViaAPI:
        @staticmethod
        def errors_logs_comparison(scenario_id,
                                   path,
                                   input_types,
                                   token,
                                   error_log_txt=ErrorLogTexts.Eng,
                                   errors_row_len=5,
                                   count=0,
                                   env='DEV'):
            print(f'==Start errors logs comparison')
            comparison_pass = 0
            comparison_fail = 0
            comparison_skip = 0
            for input_name, input_type in input_types.items():
                count += 1
                url_input_type = input_type.get('url_path')
                params_input_type = input_type.get('parameter')
                file_name = input_type.get('system_file_name')
                type_scenarios = input_type.get('type_scenarios')

                response = ApiReq.get_input_log(tetris_scenario_id=scenario_id,
                                                url_input_type=url_input_type,
                                                type_scenarios=type_scenarios,
                                                token=token,
                                                params_input_type=params_input_type,
                                                env=env)

                url_input_type = (f'{url_input_type} - ', '')[url_input_type is None]
                if response.text != '' and response.status_code < 299:
                    request_data = extract_list_from_error_log(response.text,
                                                               error_log_txt.OBLIGATION,
                                                               error_log_txt.TYPE,
                                                               error_log_txt.NEGATIVE)

                    folder_path = rf'files/{path}/'
                    error_log_file_name = f'errors_{file_name}.txt'

                    error_log_file = io.open(folder_path + error_log_file_name, "r", encoding='utf-8')
                    log_file_data = error_log_file.read()
                    error_log_file.close()

                    log_file_data = extract_list_from_error_log(log_file_data,
                                                                error_log_txt.OBLIGATION,
                                                                error_log_txt.TYPE,
                                                                error_log_txt.NEGATIVE)

                    for m in range(len(request_data)):
                        request_data[m][1] = set(request_data[m][1])

                    for m in range(len(log_file_data)):
                        log_file_data[m][1] = set(log_file_data[m][1])

                    result = []
                    for k in range(len(request_data)):
                        set_difference = str(request_data[k][1].difference(log_file_data[k][1]))
                        if set_difference != 'set()':
                            result.append(f'{request_data[k][0]} {set_difference}')

                    if len(result) > 0:
                        comparison_fail += 1
                        status = CCol.txt_red("FAIL")
                        print(f'====[{count}] Check: {url_input_type}{input_name} {status}')
                        for err in result:
                            print('========' + err)
                    else:
                        comparison_pass += 1
                        status = CCol.txt_grn("PASS")
                        print(f'====[{count}] Check: {url_input_type}{input_name} {status}')
                else:
                    comparison_skip += 1
                    if 200 <= response.status_code < 300:
                        status = CCol.txt_yel("EMPTY RESPONSE")
                        print(f'====[{count}] Check: {url_input_type}{input_name} {status}')
                    else:
                        status = CCol.txt_red("FAIL")
                        print(f'====[{count}] Check: {url_input_type}{input_name} {status}')
                        if chr(10) in response.text:
                            print('========' + '\n        '.join(response.text.split(chr(10))[:errors_row_len]) +
                                  '\n    ...')
                        elif len(response.text) > 0:
                            print(f'========{response.text}')

            comparison_result = {}
            if comparison_pass > 0:
                comparison_result['pass'] = comparison_pass
            if comparison_fail > 0:
                comparison_result['fail'] = comparison_fail
            if comparison_skip > 0:
                comparison_result['skip'] = comparison_skip
            if count > 0:
                comparison_result['count'] = count

            print(f'==End errors logs comparison', end='\n\n')

            return comparison_result

        @staticmethod
        def upload_inputs_files(scenario_id,
                                path,
                                input_types,
                                token,
                                errors_row_len=5,
                                env='DEV',
                                files_format='csv'):

            print(f'==Start upload input files')
            for input_name, input_type in input_types.items():
                url_input_type = input_type.get('url_path')
                params_input_type = input_type.get('parameter')
                file_name = input_type.get('system_file_name')
                type_scenarios = input_type.get('type_scenarios')

                folder_path = rf'files/{path}/'
                file_name = f'{file_name}.{files_format}'
                file_path = folder_path + file_name

                response = ApiReq.upload_input_file(tetris_scenario_id=scenario_id,
                                                    url_input_type=url_input_type,
                                                    type_scenarios=type_scenarios,
                                                    token=token,
                                                    params_input_type=params_input_type,
                                                    file_path=file_path,
                                                    env=env)
                status_code = response.status_code
                if 200 <= status_code <= 299:
                    status = CCol.txt_grn(f'[{status_code}] PASS')
                elif 404 <= status_code <= 599:
                    status = CCol.txt_red(f'[{status_code}] FAIL')
                else:
                    status = CCol.txt_red(f'[{status_code}] FAIL')
                url_input_type = (f'{url_input_type} - ', '')[url_input_type is None]
                print(f'====Upload input: {url_input_type}{input_name} {status}')
                if chr(10) in response.text:
                    print('========' + '\n        '.join(response.text.split(chr(10))[:errors_row_len]) + '\n    ...')
                elif len(response.text) > 0:
                    print(f'========{response.text}')
            print(f'==End upload input files', end='\n')

        @staticmethod
        def delete_inputs_files(scenario_id,
                                input_types,
                                token,
                                errors_row_len=5,
                                env='DEV'):
            print(f'==Start delete input files')
            for input_name, input_type in input_types.items():
                url_input_type = input_type.get('url_path')
                params_input_type = input_type.get('parameter')
                type_scenarios = input_type.get('type_scenarios')

                response = ApiReq.delete_input_file(tetris_scenario_id=scenario_id,
                                                    url_input_type=url_input_type,
                                                    token=token,
                                                    type_scenarios=type_scenarios,
                                                    params_input_type=params_input_type,
                                                    env=env)
                status_code = response.status_code

                if 200 <= status_code <= 299:
                    status = CCol.txt_grn(f'[{status_code}] PASS')
                elif 404 <= status_code <= 599:
                    status = CCol.txt_red(f'[{status_code}] FAIL')
                else:
                    status = CCol.txt_red(f'[{status_code}] FAIL')
                print(f'====Delete input: {url_input_type} - {input_name} {status}')
                if chr(10) in response.text:
                    print('========' + '\n        '.join(response.text.split(chr(10))[:errors_row_len]) + '\n    ...')
                elif len(response.text) > 0:
                    print(f'========{response.text}')
            print(f'==End delete input files', end='\n')


environment = 'DEV'
scen_id = 292
# list_to_miss = ['objective', 'objective_customer', 'objective_product', 'constraint_coef', 'constraint_ratio_first_option', 'constraint_ratio_second_option']
access_token = ApiReq.authorization(*Creds.auth().values(), get='access', env=environment)
if access_token == 502:
    print('access_token', access_token)

tetris_name_matches = {'md': InputTypeNameMatch.Tetris.TYPES_MD,
                       'sourcing': InputTypeNameMatch.Tetris.TYPES_SOURCING,
                       'industry': InputTypeNameMatch.Tetris.TYPES_INDUSTRY,
                       'milkbalance': InputTypeNameMatch.Tetris.TYPES_OPTIMILK}

tetris_spreadsheets = {'md': Spreadsheets.Tetris.INPUT_MD,
                       'sourcing': Spreadsheets.Tetris.INPUT_SOURCING,
                       'industry': Spreadsheets.Tetris.INPUT_INDUSTRY,
                       'milkbalance': Spreadsheets.Tetris.INPUT_MILK_BALANCE}

# def start():
#     pass


# for path, types in tetris_spreadsheets.items():
#     InputFiles.get_input_file_from_spreadsheet(types, folder=f'tetris/input_files/{path}')

# InputFiles.get_input_file_from_spreadsheet(Spreadsheets.CFR.INPUT_CFR, folder=f'cfr/input_files/')

# param = [[True, False, False, False, False] for i in range(100)]
# files = ['dlc']
# data_v = {
#     'CHAIN': 'R0R004',
#     'WH': '5000',
#     'SKU': '54983',
#     'MAX(MIN_DLC)': '9',
#     'Delivery Time, days': '1'
# }
# # options_increasing = {
# #     'CHAIN': {'value': 1, 'step': 100},
# #     'WH': {'value': 1, 'step': 100},
# #     'SKU': {'value': 1, 'step': 10},
# #     'MAX(MIN_DLC)': {'value': 1, 'step': 1},
# #     'Delivery Time, days': {'value': 1, 'step': 1}
# # }
#
# InputFiles.create_files(Spreadsheets.CFR.CHECK_INPUT,
#                                 params=param,
#                                 folder='cfr/test',
#                                 error_log_txt=ErrorLogTexts.Eng,
#                                 only_files=files,
#                                 create_error_logs=False,
#                                 data_values=data_v)

# InputFiles.create_invalid_files(Spreadsheets.Tetris.CHECK_INPUT_OLD,
#                                 folder='tetris/check_input_old',
#                                 error_log_txt=ErrorLogTexts.Eng)
#
# count_all = 0
# for path_items, types_items in tetris_name_matches.items():
#     result_comp = InputFiles.ViaAPI.errors_logs_comparison(error_log_txt=ErrorLogTexts.Eng,
#                                                            input_types=types_items,
#                                                            scenario_id=scenario_id,
#                                                            path=f'tetris/check_input_old/error_logs/{path_items}',
#                                                            token=access_token,
#                                                            count=count_all,
#                                                            env=environment)  # check_input check_input_old
#     count_all = result_comp.get('count')

# result_comp = InputFiles.ViaAPI.errors_logs_comparison(error_log_txt=ErrorLogTexts.Eng,
#                                                        input_types=InputTypeNameMatch.CFR.OBLIGATORY_TYPES,
#                                                        scenario_id=scenario_id,
#                                                        path=f'cfr/check_input/error_logs/cfr_check_data',
#                                                        token=access_token,
#                                                        env=environment)  # check_input check_input_old

# for path, types in tetris_name_matches.items():
#     InputFiles.ViaAPI.upload_inputs_files(scenario_id=scenario_id,
#                                           input_types=types,
#                                           path=f'tetris/valid_input_files/{path}',
#                                           token=access_token,
#                                           env=environment)  # valid_input_files input_files check_input check_input_old

# required_inputs = {t: InputTypeNameMatch.Tetris.TYPES_MD[t] for t in ('materials', 'locations', 'calendars')}

# required_inputs = InputTypeNameMatch.CFR.OBLIGATORY_TYPES.copy()
# required_inputs.update(InputTypeNameMatch.CFR.NOT_OBLIGATORY_TYPES)

# required_inputs = {t: InputTypeNameMatch.Promo.TYPES[t] for t in ('distr_mapping', 'combine_products')}
# required_inputs = InputTypeNameMatch.Promo.TYPES

# InputFiles.ViaAPI.upload_inputs_files(scenario_id=scenario_id,
#                                       input_types=required_inputs,
#                                       path=f'cfr/input_files',
#                                       # tetris/check_input_old/md cfr/input_files check_input/cfr_check_data promo/input_files/csv
#                                       token=access_token,
#                                       env=environment)  # valid_input_files input_files check_input check_input_old

# for types in name_matches.values():
#     InputFiles.ViaAPI.delete_inputs_files(scenario_id=scenario_id,
#                                           input_types=types,
#                                           token=access_token,
#                                           env=environment)

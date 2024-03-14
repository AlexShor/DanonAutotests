import time
import os
import random
import io
from collections import Counter

from py_google_sheets.gsheets import GoogleSheets
from input_data import FillData, DataTypes, Spreadsheets, DataTypesErrorExceptions, InputTypeNameMatch
from input_data import ErrorLogTexts
from pages.api.base_api_requests import BaseApiRequests as ApiReq
from pages.site_data.credentials import Credentials as Creds
from custom_moduls.console_design.colors import ConsoleColors as CCol
from custom_moduls.console_design.indentation_levels import indentation_levels as Ilvl

import pandas as pd
import ast

errors_regarding_obligatory_fields = []
type_errors = []
errors_with_non_negative_values = []


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


def processing(i, params_length, text='Processing:'):
    step = params_length / 20
    if i % step == 0:
        percent = str(100 * i / params_length)
        print(f'\r{Ilvl(2)}{text} {percent}%', sep='', end='')
    if i == params_length - 1:
        print(f'\r{Ilvl(2)}{text} 100.0%', sep='', end='\n')


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
                     negative, negativity, nan_value, inverse_integrity, file_name, error_log_txt):

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
        if negativity and 'FALSE' in negative and (data_type == DataTypes.INT or data_type == DataTypes.DECIMAL):
            errors_with_non_negative_values.append(error_text)


def increase_data_values(i, data_values, options_increasing_data_values):
    result = data_values.copy()
    for key, value in options_increasing_data_values.items():
        if value is not None:
            if i % value['step'] == 0:
                if type(result[key]) == int:
                    if value['value'] == random:
                        result[key] = value['value'].randint(*value['rand_values'])
                    else:
                        result[key] += value['value']
                elif type(result[key]) == str:
                    string, num = result[key].split('_')
                    if value.get('value') is None:
                        result[key] = f"{string}_{result[value['copy_value']]}"
                    else:
                        result[key] = f"{string}_{int(num) + value['value']}"
    return result


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
                data_type, nan_value, negative, create_error_logs,
                validity,
                del_value_nan=False,
                negativity=False,
                inverse_integrity=False,
                bool_false=False):

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
                         del_value_nan, negative, negativity, nan_value,
                         inverse_integrity, file_name, error_log_txt)

    return value


class InputFiles:

    @staticmethod
    @benchmark
    def create_invalid_files(check_input_url,
                             error_log_lang_rus=False,
                             params=None,
                             folder='files',
                             file_name_prefix='',
                             miss_worksheets=None,
                             invert_miss_worksheets=False,
                             only_files=None,
                             create_error_logs=True):

        error_log_txt = (ErrorLogTexts.Eng, ErrorLogTexts.Rus)[error_log_lang_rus]

        if params is None:
            # validity, del_value_nan=False, negativity=False, inverse_integrity=False, bool_false, [Fill 1//2 row]
            params = [[False, False, False, False, False],
                      [True, True, False, False, True, True],
                      [True, False, False, False, True, True],
                      [True, False, True, False, False],
                      [True, False, False, True, True],
                      [True, False, False, False, False]]

        tables, worksheets_names = GoogleSheets.pars(check_input_url, miss_worksheets, invert_miss_worksheets)

        # start_creating_files = time.time()
        # print(f'{Ilvl(1)}Start {}')

        for table in range(len(tables)):
            file_names = Counter([row[0].strip() for row in tables[table]][1:])

            if only_files is not None:
                file_names = {k: v for k, v in file_names.items() if k in only_files}

            folder_name = f'files/{folder}/{worksheets_names[table]}'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            for file_name in file_names.keys():
                start_creating = time.time()
                print(f'{Ilvl(2)}Creating file: "{worksheets_names[table]}/{file_name}{file_name_prefix}.csv"', end='')

                column_names = [row[1].strip() for row in tables[table] if row[0].strip() == file_name]

                params_length = len(params)
                data = [[] for _ in range(params_length)]

                for i in range(params_length):
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
                                                               *params[i][:-1]))
                                    break
                                else:
                                    data[i].append(create_data(file_name, column_name, current_row,
                                                               error_log_txt,
                                                               table_data_type,
                                                               table_nan_value,
                                                               table_negative,
                                                               create_error_logs,
                                                               *params[i]))
                                    break

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

                file_path = rf'{folder_name}/{file_name}{file_name_prefix}.csv'
                if os.path.exists(file_path):
                    os.remove(file_path)

                df = pd.DataFrame(data, columns=column_names)
                df.to_csv(file_path, index=False, encoding="utf_8_sig")

                end_creating = time.time() - start_creating
                print(f' {Ilvl(1)}{CCol.txt_grn("DONE")}: ', round(end_creating, 3))

        # end_creating_files = time.time() - start_creating_files
        # print('====End creating invalid files. Time:', round(end_creating_files, 3), end='\n\n')

    @staticmethod
    @benchmark
    def create_file(count_row, data_values, options_increasing_data_values,
                    folder, file_name, file_name_prefix, write_step=100_000):

        folder_name = f'files/{folder}'
        file_path = rf'{folder_name}/{file_name}{file_name_prefix}.csv'
        if os.path.exists(file_path):
            os.remove(file_path)

        df = pd.DataFrame([data_values])
        df.to_csv(file_path, index=False, header=True, encoding="utf_8_sig")
        rows = count_row
        prec_i = 0
        while rows != 0 and rows >= write_step:
            data = []

            for i in range(write_step):
                data_values = increase_data_values(i, data_values, options_increasing_data_values)
                data.append(data_values)

                processing(i + prec_i, count_row)

            df = pd.DataFrame(data)
            df.to_csv(file_path, mode='a', index=False, header=False, encoding="utf_8_sig")

            prec_i += write_step
            rows -= write_step
            if rows < write_step:
                write_step = rows

    @staticmethod
    @benchmark
    def get_input_file_from_spreadsheet(check_input_url,
                                        folder='files',
                                        miss_worksheets=None,
                                        invert_miss_worksheets=False):

        spreadsheet, worksheets_names = GoogleSheets.pars(check_input_url, miss_worksheets, invert_miss_worksheets)
        # start_time = time.time()
        # print('==Start creating files')

        folder_name = 'files/' + folder
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for i in range(len(spreadsheet)):
            file_name = worksheets_names[i].strip()

            start_creating_file = time.time()
            print(f'{Ilvl(2)}Creating file: "{file_name}.csv".', end=' ')

            column_names = spreadsheet[i][0]
            data = spreadsheet[i][1:]

            file_path = rf'{folder_name}/{file_name}.csv'
            if os.path.exists(file_path):
                os.remove(file_path)

            df = pd.DataFrame(data, columns=column_names)
            df.to_csv(file_path, index=False, encoding="utf_8_sig")

            end_creating_file = time.time() - start_creating_file
            print(f' {Ilvl(1)}{CCol.txt_grn("DONE")}: ', round(end_creating_file, 3))

        # end_time = time.time() - start_time
        # print('====End creating files. Time:', round(end_time, 3), end='\n\n')

    class ViaAPI:
        @staticmethod
        @benchmark
        def errors_logs_comparison(scenario_id,
                                   path,
                                   input_types,
                                   token,
                                   error_log_txt=ErrorLogTexts.Eng,
                                   errors_row_len=5,
                                   count=0,
                                   env='DEV'):
            # print(f'==Start errors logs comparison')
            comparison_pass = 0
            comparison_fail = 0
            comparison_skip = 0
            for input_name, input_type in input_types.items():
                print()
                count += 1
                url_input_type = input_type.get('url_path')
                params_input_type = input_type.get('parameter')
                file_name = input_type.get('system_file_name')
                scenario_type = input_type.get('scenario_type')

                response = ApiReq.get_input_log(tetris_scenario_id=scenario_id,
                                                url_input_type=url_input_type,
                                                scenario_type=scenario_type,
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

                    # result = []
                    request_data_result = []
                    log_file_data_result = []
                    for k in range(len(request_data)):
                        #print(request_data[k][1])

                        # set_difference = str(request_data[k][1].symmetric_difference(log_file_data[k][1]))

                        log_file_data_set_diff = str(request_data[k][1].difference(log_file_data[k][1]))
                        request_data_set_diff = str(log_file_data[k][1].difference(request_data[k][1]))

                        # if set_difference != 'set()':
                        #     result.append(f'{request_data[k][0]} {set_difference}')

                        if request_data_set_diff != 'set()':
                            request_data_result.append(f'{request_data[k][0]} {request_data_set_diff}')
                        if log_file_data_set_diff != 'set()':
                            log_file_data_result.append(f'{request_data[k][0]} {log_file_data_set_diff}')

                    # if len(result) > 0:
                    #     comparison_fail += 1
                    #     status = CCol.txt_red("FAIL")
                    #     print(f'{Ilvl(2)}[{count}] Check: {url_input_type}{input_name} {status}')
                    #     for err in result:
                    #         print(Ilvl(3) + err)

                    if len(request_data_result + log_file_data_result) > 0:
                        comparison_fail += 1
                        status = CCol.txt_red("FAIL")
                        print(f'{Ilvl(2)}[{count}] Check: {url_input_type}{input_name} {status}')
                        if len(request_data_result) > 0:
                            print(Ilvl(3) + 'Request data not have:')
                            for err in request_data_result:
                                print(Ilvl(4) + err)
                        if len(log_file_data_result) > 0:
                            print(Ilvl(3) + 'Log file data not have:')
                            for err in log_file_data_result:
                                print(Ilvl(4) + err)
                    else:
                        comparison_pass += 1
                        status = CCol.txt_grn("PASS")
                        print(f'{Ilvl(2)}[{count}] Check: {url_input_type}{input_name} {status}')
                else:
                    comparison_skip += 1
                    if 200 <= response.status_code < 300:
                        status = CCol.txt_yel("EMPTY RESPONSE")
                        print(f'{Ilvl(2)}[{count}] Check: {url_input_type}{input_name} {status}')
                    else:
                        status = CCol.txt_red("FAIL")
                        print(f'{Ilvl(2)}[{count}] Check: {url_input_type}{input_name} {status}')
                        if chr(10) in response.text:
                            print(Ilvl(3) + f'\n{Ilvl(3, symbol=" ")}'.join(
                                response.text.split(chr(10))[:errors_row_len]) + f'\n{Ilvl(2, symbol=" ")}...')
                        elif len(response.text) > 0:
                            print(f'{Ilvl(3)}{response.text}')

            comparison_result = {}
            if comparison_pass > 0:
                comparison_result['pass'] = comparison_pass
            if comparison_fail > 0:
                comparison_result['fail'] = comparison_fail
            if comparison_skip > 0:
                comparison_result['skip'] = comparison_skip
            if count > 0:
                comparison_result['count'] = count

            # print(f'{Ilvl(1)}End errors logs comparison', end='\n\n')

            return comparison_result

        @staticmethod
        @benchmark
        def upload_inputs_files(scenario_id,
                                path,
                                input_types,
                                token,
                                errors_row_len=5,
                                env='DEV',
                                files_format='csv'):

            # print(f'==Start upload input files')
            for input_name, input_type in input_types.items():
                url_input_type = input_type.get('url_path')
                params_input_type = input_type.get('parameter')
                file_name = input_type.get('system_file_name')
                scenario_type = input_type.get('scenario_type')

                folder_path = rf'files/{path}/'
                file_name = f'{file_name}.{files_format}'
                file_path = folder_path + file_name

                response = ApiReq.upload_input_file(tetris_scenario_id=scenario_id,
                                                    url_input_type=url_input_type,
                                                    scenario_type=scenario_type,
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
                print(f'{Ilvl(2)}Upload input: {url_input_type}{input_name} {status}')
                if chr(10) in response.text:
                    print(Ilvl(3) + f'\n{Ilvl(3, symbol=" ")}'.join(
                        response.text.split(chr(10))[:errors_row_len]) + f'\n{Ilvl(2, symbol=" ")}...')
                elif len(response.text) > 0:
                    print(f'{Ilvl(3)}{response.text}')
            # print(f'==End upload input files', end='\n')

        @staticmethod
        @benchmark
        def delete_inputs_files(scenario_id,
                                input_types,
                                token,
                                errors_row_len=5,
                                env='DEV'):
            # print(f'==Start delete input files')
            for input_name, input_type in input_types.items():
                url_input_type = input_type.get('url_path')
                params_input_type = input_type.get('parameter')
                scenario_type = input_type.get('scenario_type')

                response = ApiReq.delete_input_file(tetris_scenario_id=scenario_id,
                                                    url_input_type=url_input_type,
                                                    token=token,
                                                    scenario_type=scenario_type,
                                                    params_input_type=params_input_type,
                                                    env=env)
                status_code = response.status_code

                if 200 <= status_code <= 299:
                    status = CCol.txt_grn(f'[{status_code}] PASS')
                elif 404 <= status_code <= 599:
                    status = CCol.txt_red(f'[{status_code}] FAIL')
                else:
                    status = CCol.txt_red(f'[{status_code}] FAIL')
                url_input_type = (f'{url_input_type} - ', '')[url_input_type is None]
                print(f'{Ilvl(2)}Delete input: "{url_input_type}{input_name}" {status}')
                if chr(10) in response.text:
                    print(Ilvl(3) + f'\n{Ilvl(3, symbol=" ")}'.join(
                        response.text.split(chr(10))[:errors_row_len]) + f'\n{Ilvl(2, symbol=" ")}...')
                elif len(response.text) > 0:
                    print(f'{Ilvl(3)}{response.text}')
            # print(f'==End delete input files', end='\n')


class Start:
    def __init__(self, scen_id, env='DEV', tetris_new=True):
        self.environment = env
        self.scenario_id = scen_id

        if tetris_new:
            tetris_spreadsheets = {'sourcing': Spreadsheets.TetrisNew.INPUT_SOURCING,
                                   'milk': Spreadsheets.TetrisNew.INPUT_MILK}
            tetris_name_matches = {'sourcing': InputTypeNameMatch.TetrisNew.TYPES_SOURCING,
                                   'milk': InputTypeNameMatch.TetrisNew.TYPES_MILK}
        else:
            tetris_spreadsheets = {'md': Spreadsheets.Tetris.INPUT_MD,
                                   'sourcing': Spreadsheets.Tetris.INPUT_SOURCING,
                                   'industry': Spreadsheets.Tetris.INPUT_INDUSTRY,
                                   'milkbalance': Spreadsheets.Tetris.INPUT_MILK_BALANCE}
            tetris_name_matches = {'md': InputTypeNameMatch.Tetris.TYPES_MD,
                                   'sourcing': InputTypeNameMatch.Tetris.TYPES_SOURCING,
                                   'industry': InputTypeNameMatch.Tetris.TYPES_INDUSTRY,
                                   'milkbalance': InputTypeNameMatch.Tetris.TYPES_OPTIMILK}

        self.tetris_spreadsheets = tetris_spreadsheets
        self.tetris_name_matches = tetris_name_matches

    def auth(self):
        access_token = ApiReq.authorization(*Creds.auth(env=self.environment).values(),
                                            get='access',
                                            env=self.environment)
        if access_token == 502:
            print('access_token', access_token)
        return access_token

    def start_get_input_file_from_spreadsheet_tetris(self, folder='tetris/input_files/'):
        for path, types in self.tetris_spreadsheets.items():
            InputFiles.get_input_file_from_spreadsheet(types, folder=f'{folder}{path}')

    def start_get_input_file_from_spreadsheet_other(self, types, folder='rtm/input_files/', miss_worksheets=None):
        InputFiles.get_input_file_from_spreadsheet(types, folder=folder, miss_worksheets=miss_worksheets)

    def start_create_file(self):
        file_size = 1_048_600  # 1_000_000 23_000_000
        for k, v in {'_test_1048600': file_size}.items():
            # data_v = {
            #     'Plant': 1,
            #     'SKU': 10000,
            #     'SKU Name': 'SKU Name_1',
            #     'Жесткий Карантин(дней)': 1,
            #     'Мягкий карантин(дней)': 1,
            #     'Частота розлива в неделю': 1,
            #     'Срок годности': 1,
            #     'Признак долгосрока': 1,
            #     'Ready to ship': 1
            # }
            # options_increasing = {
            #     'Plant': {'value': 1, 'step': 10},
            #     'SKU': {'value': random, 'rand_values': (0, 10000), 'step': 1},
            #     'SKU Name': {'copy_value': 'SKU', 'step': 1},
            #     'Жесткий Карантин(дней)': {'value': random, 'rand_values': (0, 500), 'step': 1},
            #     'Мягкий карантин(дней)': {'value': random, 'rand_values': (0, 100), 'step': 1},
            #     'Частота розлива в неделю': {'value': random, 'rand_values': (0, 7), 'step': 1},
            #     'Срок годности': {'value': random, 'rand_values': (0, 5000), 'step': 1},
            #     'Признак долгосрока': {'value': random, 'rand_values': (0, 1), 'step': 1},
            #     'Ready to ship': {'value': random, 'rand_values': (0, 5000), 'step': 1},
            # }

            # data_v = {
            #     'ID_ORG_CBU': 5000,
            #     'ID_SAD_PGI_YYYYMMDD': '01-03-2023  00:00:00',
            #     'CD_LOG_SHIPMENT_TYPE': 'Z003',
            #     'DS_LOG_SHIPMENT_TYPE': 'Z Internal Shipmt',
            #     'CD_LOG_SHIPMENT': 1,
            #     'CD_CUS_SHIP_TO': 50010976,
            #     'DS_CUS_SHIP_TO': 'DC 5322 NV2 NOVOSIBIRSK REMOTE',
            #     'CD_SAD_DELIVERY': 5044875394,
            #     'CD_MAT_MATERIAL': 55139,
            #     'CD_MAT_BATCH': 'YL20230823',
            #     'PLANT_PREF': 'YL',
            #     'DS_LOG_ROUTE': '5521-5501 YA1-SD1 Yalutorovsk-Shadrinsk',
            #     'CD_VND_VENDOR': 20092033,
            #     'DS_VND_VENDOR': 'ООО "ДЖИИКСО ЛОДЖИСТИКС"',
            #     'TPP': 5322,
            #     'TPP_NAME': '5000 RU DC Novosibir',
            #     'CD_LOG_SHIPPING_TYPE_HEADER': 5322,
            #     'TRUCK_TYPE': 'Ref truck 20t',
            #     'DELIVERED_KG': 2220.48,
            #     'TRANSPORT_COST_BY_WEIGHT': 2140.14,
            #     'TRANSPORT_COST_SHIPMENT': 17529
            # }
            # options_increasing = {
            #     'ID_ORG_CBU': None,
            #     'ID_SAD_PGI_YYYYMMDD': None,
            #     'CD_LOG_SHIPMENT_TYPE': None,
            #     'DS_LOG_SHIPMENT_TYPE': None,
            #     'CD_LOG_SHIPMENT': {'value': 1, 'step': 1},
            #     'CD_CUS_SHIP_TO': {'value': 1, 'step': 5},
            #     'DS_CUS_SHIP_TO': None,
            #     'CD_SAD_DELIVERY': {'value': 1, 'step': 10},
            #     'CD_MAT_MATERIAL': {'value': 1, 'step': 12},
            #     'CD_MAT_BATCH': None,
            #     'PLANT_PREF': None,
            #     'DS_LOG_ROUTE': None,
            #     'CD_VND_VENDOR': None,
            #     'DS_VND_VENDOR': None,
            #     'TPP': {'value': 1, 'step': 5},
            #     'TPP_NAME': None,
            #     'CD_LOG_SHIPPING_TYPE_HEADER': None,
            #     'TRUCK_TYPE': None,
            #     'DELIVERED_KG': None,
            #     'TRANSPORT_COST_BY_WEIGHT': None,
            #     'TRANSPORT_COST_SHIPMENT': None,
            # }

            data_v = {
                'Product ID': 1,
                'Location ID': 1,
                'Date ID': '2023M01',
                'Total KG': 1000
            }
            options_increasing = {
                'Product ID': {'value': 1, 'step': 1},
                'Location ID': {'value': 1, 'step': 1},
                'Date ID': None,
                'Total KG': None
            }

            InputFiles.create_file(count_row=v,
                                   data_values=data_v,
                                   options_increasing_data_values=options_increasing,
                                   folder='tetris/big',
                                   file_name='Demand',
                                   file_name_prefix=k)

    def start_create_invalid_files(self, spreadsheet, folder, error_log_lang_rus=False):
        InputFiles.create_invalid_files(check_input_url=spreadsheet,
                                        folder=folder,
                                        error_log_lang_rus=error_log_lang_rus)

    def start_errors_logs_comparison_tetris(self, folder, error_log_lang_rus=False):
        error_log_txt = (ErrorLogTexts.Eng, ErrorLogTexts.Rus)[error_log_lang_rus]
        count_all = 0
        for path_items, types_items in self.tetris_name_matches.items():
            result_comp = InputFiles.ViaAPI.errors_logs_comparison(error_log_txt=error_log_txt,
                                                                   input_types=types_items,
                                                                   scenario_id=self.scenario_id,
                                                                   path=f'{folder}/{path_items}',
                                                                   token=self.auth(),
                                                                   count=count_all,
                                                                   env=self.environment)  # check_input check_input_old
            count_all = result_comp.get('count')

    def start_errors_logs_comparison_other(self, required_inputs, folder):
        result_comp = InputFiles.ViaAPI.errors_logs_comparison(error_log_txt=ErrorLogTexts.Eng,
                                                               input_types=required_inputs,
                                                               scenario_id=self.scenario_id,
                                                               path=folder,
                                                               token=self.auth(),
                                                               env=self.environment)  # check_input check_input_old

    def start_upload_valid_inputs_files_tetris(self, folder):
        for path, types in self.tetris_name_matches.items():
            InputFiles.ViaAPI.upload_inputs_files(scenario_id=self.scenario_id,
                                                  input_types=types,
                                                  path=f'{folder}/{path}',
                                                  token=self.auth(),
                                                  env=self.environment)
            # valid_input_files input_files check_input check_input_old

    def start_upload_invalid_inputs_files_tetris(self, folder):
        for path, types in self.tetris_name_matches.items():
            InputFiles.ViaAPI.upload_inputs_files(scenario_id=self.scenario_id,
                                                  input_types=types,
                                                  path=f'{folder}/{path}',
                                                  token=self.auth(),
                                                  env=self.environment)
            # valid_input_files input_files check_input check_input_old

    def start_upload_inputs_files_other(self, required_inputs, folder):
        # required_inputs = {t: InputTypeNameMatch.Tetris.TYPES_MD[t] for t in ('materials', 'locations', 'calendars')}

        # required_inputs = InputTypeNameMatch.CFR.TYPES

        # required_inputs = {t: InputTypeNameMatch.Promo.TYPES[t] for t in ('distr_mapping', 'combine_products')}
        # required_inputs = InputTypeNameMatch.Promo.TYPES

        InputFiles.ViaAPI.upload_inputs_files(scenario_id=self.scenario_id,
                                              input_types=required_inputs,
                                              path=folder,
                                              token=self.auth(),
                                              env=self.environment)
        # tetris/check_input_old/md cfr/input_files check_input/cfr_check_data promo/input_files/csv
        # valid_input_files input_files check_input check_input_old

    def start_delete_inputs_files_tetris(self):
        for types in self.tetris_name_matches.values():
            InputFiles.ViaAPI.delete_inputs_files(scenario_id=self.scenario_id,
                                                  input_types=types,
                                                  token=self.auth(),
                                                  env=self.environment)

    def start_delete_inputs_files_other(self, input_types):
        InputFiles.ViaAPI.delete_inputs_files(scenario_id=self.scenario_id,
                                              input_types=input_types,
                                              token=self.auth(),
                                              env=self.environment)


if __name__ == '__main__':
    environment = 'DEV'
    scenario_id = 1661
    miss_worksheets = ['New Farms', 'Regular Supplies', 'Spot Supplies',
                       'Supply Scheme', 'Reco Capabilities', 'Derivation']

    start = Start(scen_id=scenario_id, env=environment, tetris_new=False)

    # start.start_get_input_file_from_spreadsheet_tetris(folder='tetris_new/input_files/')
    # start.start_get_input_file_from_spreadsheet_other(types=Spreadsheets.RTM.INPUT_RTM,
    #                                                   folder='rtm/input_files') # miss_worksheets=miss_worksheets)

    start.start_create_file()
    # start.start_create_invalid_files(Spreadsheets.TetrisNew.CHECK_INPUT, folder='tetris_new/check_input', error_log_lang_rus=True)
    # start.start_create_invalid_files(Spreadsheets.RTM.CHECK_INPUT, folder='rtm/check_input3')

    # cfr/check_input/error_logs/cfr_check_data |
    # start.start_errors_logs_comparison_tetris(folder='tetris_new/check_input/error_logs', error_log_lang_rus=True)
    # start.start_errors_logs_comparison_other(InputTypeNameMatch.CFR.TYPES, folder=f'cfr/check_input/error_logs/cfr_check_data')
    # start.start_errors_logs_comparison_other(InputTypeNameMatch.RTM.TYPES, folder=f'rtm/check_input/error_logs/Sheet1')
    # start.start_errors_logs_comparison_other(InputTypeNameMatch.Promo.TYPES, folder=f'promo/check_input/error_logs/update')

    # start.start_upload_valid_inputs_files_tetris(folder='tetris_new/validation')  # tetris_new/input_files
    # start.start_upload_invalid_inputs_files_tetris(folder='tetris_new/check_input')

    # cfr/check_input/cfr_check_data | cfr/input_files
    # start.start_upload_inputs_files_other(required_inputs=InputTypeNameMatch.RTM.TYPES, folder=f'rtm/input_files')
    # start.start_upload_inputs_files_other(required_inputs=InputTypeNameMatch.CFR.TYPES, folder=f'cfr/check_input/cfr_check_data')
    # start.start_upload_inputs_files_other(required_inputs=InputTypeNameMatch.RTM.TYPES, folder=f'rtm/check_input/Sheet1')
    # start.start_upload_inputs_files_other(required_inputs=InputTypeNameMatch.Promo.TYPES, folder=f'promo/input_files')
    # start.start_upload_inputs_files_other(required_inputs=InputTypeNameMatch.Promo.TYPES, folder=f'promo/check_input/update')

    # start.start_delete_inputs_files_tetris()
    # start.start_delete_inputs_files_other(InputTypeNameMatch.TetrisNew.TYPES)
    # start.start_delete_inputs_files_other(InputTypeNameMatch.CFR.TYPES)
    # start.start_delete_inputs_files_other(InputTypeNameMatch.RTM.TYPES)
    # start.start_delete_inputs_files_other(InputTypeNameMatch.Promo.TYPES)

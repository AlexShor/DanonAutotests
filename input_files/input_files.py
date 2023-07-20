import time
import os
import random
import io
from collections import Counter


from py_google_sheets.gsheets import GoogleSheets
from input_data import FillData, DataTypes, Spreadsheets, DataTypesErrorExceptions, InputTypeNameMatch
from input_data import ErrorLogTexts
from pages.site_data.urls import BaseUrls
from pages.api.api_requests import PublicRequests as PubReq
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
                data_type, nan_value, negative, validity,
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
    create_error_log(data_type, current_row, column_name, validity,
                     del_value_nan, negativity, nan_value, inverse_integrity, file_name, error_log_txt)
    return value


class InputFiles:
    @staticmethod
    def create(check_input_url,
               error_log_txt,
               params=None,
               folder='files',
               miss_worksheets=None,
               invert_miss_worksheets=False):

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

            folder_name = f'files/{folder}/{worksheets_names[table]}'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            for file_name in file_names.keys():
                count_col = file_names.get(file_name)

                start_creating = time.time()
                print(f'========Creating files: "{worksheets_names[table]}/{file_name}.csv"', end='')

                column_names = [row[1].strip() for row in tables[table] if row[0].strip() == file_name]
                data = [[] for _ in range(len(params))]
                for i in range(len(params)):
                    current_row = i
                    count = 0
                    for column_name in column_names:
                        for row in tables[table]:
                            if row[0].strip() == file_name and row[1].strip() == column_name:
                                if len(params[i]) > 5 and params[i][5]:
                                    count += 1
                                    if count <= (count_col // 2):
                                        data[i].append(create_data(file_name, column_name, current_row,
                                                                   error_log_txt,
                                                                   row[2].strip().upper(),
                                                                   row[3].strip().upper(),
                                                                   row[4].strip().upper(),
                                                                   params[i][0],
                                                                   params[i][1],
                                                                   params[i][2],
                                                                   params[i][3],
                                                                   params[i][4]))
                                        break
                                    else:
                                        params[i][1] = not params[i][1]
                                        data[i].append(create_data(file_name, column_name, current_row,
                                                                   error_log_txt,
                                                                   row[2].strip().upper(),
                                                                   row[3].strip().upper(),
                                                                   row[4].strip().upper(),
                                                                   params[i][0],
                                                                   params[i][1],
                                                                   params[i][2],
                                                                   params[i][3],
                                                                   params[i][4]))
                                        break
                                else:
                                    data[i].append(create_data(file_name, column_name, current_row,
                                                               error_log_txt,
                                                               row[2].upper(),
                                                               row[3].upper(),
                                                               row[4].upper(),
                                                               *params[i]))
                                    break

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
        start_creating_files = time.time()
        print('====Start creating files')

        folder_name = 'files/' + folder
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for i in range(len(spreadsheet)):
            file_name = worksheets_names[i].strip()

            start_creating_file = time.time()
            print(f'========Creating file: "{file_name}.csv".', end=' ')

            column_names = spreadsheet[i][0]
            data = spreadsheet[i][1:]

            file_path = rf'{folder_name}/{file_name}.csv'
            if os.path.exists(file_path):
                os.remove(file_path)

            df = pd.DataFrame(data, columns=column_names)
            df.to_csv(file_path, index=False, encoding="utf_8_sig")

            end_creating_file = time.time() - start_creating_file
            print(f'=={CCol.txt_grn("DONE")}: ', round(end_creating_file, 3))

        end_creating_files = time.time() - start_creating_files
        print('====End creating files. Time:', round(end_creating_files, 3), end='\n\n')

    @staticmethod
    def api_comparison_validation_errors(error_log_txt, input_type_name_match, scenario_id, path):
        types = input_type_name_match
        t_folder = 0
        t_url_path = 1
        t_param_input = 2
        t_file_name = 3

        token = PubReq.authorization(*Creds.auth().values(), get='access')

        for i in range(len(types)):
            input_type = types[i][t_url_path]
            input_name = types[i][t_param_input]

            response = PubReq.tetris_input_log(scenario_id, input_type, token, input_name)

            if response.text != '':
                request_data = extract_list_from_error_log(response.text,
                                                           error_log_txt.OBLIGATION,
                                                           error_log_txt.TYPE,
                                                           error_log_txt.NEGATIVE)

                folder_path = rf'files/{path}/{types[i][t_folder]}/'
                error_log_file_name = f'errors_{types[i][t_file_name]}.txt'

                error_log_file = io.open(folder_path + error_log_file_name, "r", encoding='utf-8')
                log_file_data = error_log_file.read()
                error_log_file.close()

                log_file_data = extract_list_from_error_log(log_file_data,
                                                            error_log_txt.OBLIGATION,
                                                            error_log_txt.TYPE,
                                                            error_log_txt.NEGATIVE)

                for m in range(len(request_data)):
                    request_data[m][t_url_path] = set(request_data[m][t_url_path])

                for m in range(len(log_file_data)):
                    log_file_data[m][t_url_path] = set(log_file_data[m][t_url_path])

                result = []
                for k in range(len(request_data)):
                    set_difference = str(request_data[k][t_url_path].difference(log_file_data[k][t_url_path]))
                    if set_difference != 'set()':
                        result.append(f'{request_data[k][0]} {set_difference}')

                if result:
                    print(f'==[{i}] {types[i][t_url_path]} {types[i][t_file_name]} {CCol.txt_red("FAIL")}')
                    for err in result:
                        print('====' + err)
                else:
                    print(f'==[{i}] {types[i][t_url_path]} {types[i][t_file_name]} {CCol.txt_grn("PASS")}')
            else:
                print(f'==[{i}] {types[i][t_url_path]} {types[i][t_file_name]} {CCol.txt_yel("EMPTY RESPONSE")}')

    @staticmethod
    def api_upload_inputs_files(scenario_id, path, input_type_name_match):
        types = input_type_name_match
        t_folder = 0
        t_url_path = 1
        t_param_input = 2
        t_file_name = 3

        token = PubReq.authorization(*Creds.auth().values(), get='access')

        for i in range(len(types)):
            input_type = types[i][t_url_path]
            input_name = types[i][t_param_input]
            folder_path = rf'files/{path}/{types[i][t_folder]}/'
            file_name = f'{types[i][t_file_name]}.csv'
            file_path = folder_path + file_name
            response = PubReq.tetris_upload_input_file(scenario_id, input_type, token, input_name, file_path)
            status_code = response.status_code
            if 200 <= status_code <= 299:
                status = f'[{status_code}] PASS'
                print(f'==[{i}] {types[i][t_url_path]} {types[i][t_file_name]}.csv {CCol.txt_grn(status)}')
            elif 404 <= status_code <= 599:
                status = f'[{status_code}] FAIL'
                print(f'==[{i}] {types[i][t_url_path]} {types[i][t_file_name]}.csv {CCol.txt_red(status)}')
            else:
                status = f'[{status_code}] FAIL'
                print(f'==[{i}] {types[i][t_url_path]} {types[i][t_file_name]}.csv {CCol.txt_red(status)}')
                print(f'===={response.text}')


# list_to_miss = ['objective', 'objective_customer', 'objective_product', 'constraint_coef', 'constraint_ratio_first_option', 'constraint_ratio_second_option']


# InputFiles.get_input_file_from_spreadsheet(Spreadsheets.Tetris.INPUT_MD,
#                                            folder=f'tetris/input_files/{InputTypeNameMatch.Tetris.input_type_md[0]}')
# InputFiles.get_input_file_from_spreadsheet(Spreadsheets.Tetris.INPUT_INDUSTRY,
#                                            folder=f'tetris/input_files/{InputTypeNameMatch.Tetris.input_type_industry[0]}')
# InputFiles.get_input_file_from_spreadsheet(Spreadsheets.Tetris.INPUT_SOURCING,
#                                            folder=f'tetris/input_files/{InputTypeNameMatch.Tetris.input_type_sourcing[0]}')
# InputFiles.get_input_file_from_spreadsheet(Spreadsheets.Tetris.INPUT_MILK_BALANCE,
#                                            folder=f'tetris/input_files/{InputTypeNameMatch.Tetris.input_type_optimilk[0]}')

InputFiles.create(Spreadsheets.Tetris.CHECK_INPUT,
                  folder='tetris/check_input2',
                  error_log_txt=ErrorLogTexts.Tetris)

# InputFiles.api_comparison_validation_errors(error_log_txt=ErrorLogTexts.Tetris,
#                                             input_type_name_match=InputTypeNameMatch.Tetris.TYPES,
#                                             scenario_id=210,
#                                             path='tetris/check_input/error_logs')

# types = [InputTypeNameMatch.Tetris.TYPES[0]]
# types = [['md', 'master-data', 'alt_names_locations', 'AlternativeLocations']]

# InputFiles.api_upload_inputs_files(input_type_name_match=InputTypeNameMatch.Tetris.TYPES,
#                                    scenario_id=210,
#                                    path='tetris/check_input')  # tetris/input_files tetris/check_input

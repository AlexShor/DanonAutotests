import time
import os
from collections import Counter

from py_google_sheets.gsheets import GoogleSheets
from input_data import FillData, DataTypes, Spreadsheets, DataTypesErrorExceptions
import pandas as pd


errors_regarding_obligatory_fields = []
type_errors = []
errors_with_non_negative_values = []


def save_error_log(list_errors_regarding_obligatory_fields,
                   list_type_errors,
                   list_errors_with_non_negative_values,
                   file_name,
                   folder,
                   worksheets_name):

    data = []
    if len(list_errors_regarding_obligatory_fields) > 0:
        data.append(f'Errors regarding obligatory fields: {str(list_errors_regarding_obligatory_fields)}')
    if len(list_type_errors) > 0:
        data.append(f'Type errors: {str(list_type_errors)}')
    if len(list_errors_with_non_negative_values) > 0:
        data.append(f'Errors with non-negative values: {str(list_errors_with_non_negative_values)}')

    file_path = rf'files/{folder}/error_logs/{worksheets_name}/'
    new_file_name = f'errors_{file_name}.txt'

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if os.path.exists(file_path + new_file_name):
        os.remove(file_path + new_file_name)

    error_txt_file = open(file_path + new_file_name, "w")
    for i in range(len(data)):
        error_txt_file.write(data[i])
        if i < len(data) - 1:
            error_txt_file.write('\n\n')
    error_txt_file.close()

    print(f', "error_logs/{worksheets_name}/{new_file_name}.txt".', end=' ')


def data_type_in_error_exceptions(file_name, column_name):
    for file_column in DataTypesErrorExceptions.DATA:
        if file_column == [file_name, column_name]:
            return True
    return False


def create_error_log(data_type, current_row, column_name, validity, del_value_nan,
                     negativity, nan_value, inverse_integrity, file_name):

    error_text = f'row {current_row + 2} - column {column_name.lower()}'

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


def create_data(file_name, column_name, current_row, data_type, nan_value, negative, validity,
                del_value_nan=False,
                negativity=False,
                inverse_integrity=False):
    if data_type == '': return 'NO_DATA_TYPE'
    value = FillData.get_value(data_type, validity)
    if not validity:
        negativity = False
    value = nan_type(validity, nan_value, value, del_value_nan)
    if value != '':
        if data_type == DataTypes.DECIMAL:
            value = negative_type(validity, negative, value, negativity)
            if inverse_integrity:
                value = value[:value.index('.')]
        elif data_type == DataTypes.INT:
            value = negative_type(validity, negative, value, negativity)
            if inverse_integrity:
                value += '.45'
    create_error_log(data_type, current_row, column_name, validity,
                     del_value_nan, negativity, nan_value, inverse_integrity, file_name)
    return value


class InputFiles:
    @staticmethod
    def create(check_input_url,
               params=None,
               folder='files',
               miss_worksheets=None,
               invert_miss_worksheets=False):

        if params is None:
            # validity, del_value_nan=False, negativity=False, inverse_integrity=False, [Fill 1//2 row]
            params = [(False, False, False, False),
                      (True, True, False, False, True),
                      (True, False, False, False, True),
                      (True, False, True, False),
                      (True, False, False, True),
                      (True, False, False, False)]

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
                                if len(params[i]) > 4 and params[i][4]:
                                    count += 1
                                    if count <= (count_col // 2):
                                        data[i].append(create_data(file_name, column_name, current_row,
                                                                   row[2].strip().upper(),
                                                                   row[3].strip().upper(),
                                                                   row[4].strip().upper(),
                                                                   params[i][0],
                                                                   params[i][1],
                                                                   params[i][2],
                                                                   params[i][3]))
                                        break
                                    else:
                                        data[i].append(create_data(file_name, column_name, current_row,
                                                                   row[2].strip().upper(),
                                                                   row[3].strip().upper(),
                                                                   row[4].strip().upper(),
                                                                   params[i][0],
                                                                   not params[i][1],
                                                                   params[i][2],
                                                                   params[i][3]))
                                        break
                                else:
                                    data[i].append(create_data(file_name, column_name, current_row,
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
                               worksheets_names[table])

                errors_regarding_obligatory_fields.clear()
                type_errors.clear()
                errors_with_non_negative_values.clear()

                file_path = rf'{folder_name}/{file_name}.csv'
                if os.path.exists(file_path):
                    os.remove(file_path)

                df = pd.DataFrame(data, columns=column_names)
                df.to_csv(file_path, index=False, encoding="utf_8_sig")

                end_creating = time.time() - start_creating
                print(f' ==Done: ', round(end_creating, 3))

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
            file_name = worksheets_names[i]

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
            print(f' ==Done: ', round(end_creating_file, 3))

        end_creating_files = time.time() - start_creating_files
        print('====End creating files. Time:', round(end_creating_files, 3), end='\n\n')


# list_to_miss = ['objective', 'objective_customer', 'objective_product', 'constraint_coef', 'constraint_ratio_first_option', 'constraint_ratio_second_option']


InputFiles.create(Spreadsheets.Promo.CHECK_INPUT, folder='promo/check_input')


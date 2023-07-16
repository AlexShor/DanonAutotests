import time
import os
from collections import Counter

from py_google_sheets.gsheets import GoogleSheets
from input_data import FillData, DataTypes
import pandas as pd


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


def create_data(data_type, nan, negative, validity, del_value_nan=False, negativity=False, inverse_integrity=False):
    if data_type == '': return 'NO_DATA_TYPE'
    value = FillData.get_value(data_type, validity)
    if not validity:
        negativity = False
    value = nan_type(validity, nan, value, del_value_nan)
    if value != '':
        if data_type == DataTypes.DECIMAL:
            value = negative_type(validity, negative, value, negativity)
            if inverse_integrity:
                value = value[:value.index('.')]
        elif data_type == DataTypes.INT:
            value = negative_type(validity, negative, value, negativity)
            if inverse_integrity:
                value += '.45'

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
                print(f'========Creating file: "{worksheets_names[table]}/{file_name}.csv".', end=' ')

                column_names = [row[1].strip() for row in tables[table] if row[0].strip() == file_name]
                data = [[] for _ in range(len(params))]
                for i in range(len(params)):
                    count = 0
                    for column_name in column_names:
                        for row in tables[table]:
                            if row[0].strip() == file_name and row[1].strip() == column_name:
                                if len(params[i]) > 4 and params[i][4]:
                                    count += 1
                                    if count <= (count_col // 2):
                                        data[i].append(create_data(row[2].strip().upper(),
                                                                   row[3].strip().upper(),
                                                                   row[4].strip().upper(),
                                                                   params[i][0],
                                                                   params[i][1],
                                                                   params[i][2],
                                                                   params[i][3]))
                                        break
                                    else:
                                        data[i].append(create_data(row[2].strip().upper(),
                                                                   row[3].strip().upper(),
                                                                   row[4].strip().upper(),
                                                                   params[i][0],
                                                                   not params[i][1],
                                                                   params[i][2],
                                                                   params[i][3]))
                                        break
                                else:
                                    data[i].append(create_data(row[2].upper(),
                                                               row[3].upper(),
                                                               row[4].upper(),
                                                               *params[i]))
                                    break

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


# InputFiles.create(Spreadsheets.Promo.CHECK_INPUT, folder='promo/check_input')


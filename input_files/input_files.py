import os
from collections import Counter

from py_google_sheets.gsheets import GoogleSheets
from input_data import CheckInputUrls, FillData, DataTypes
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


def create_data(data_type, nan, negative, validity, del_value_nan=False, negativity=False):
    value = FillData.get_value(data_type, validity)
    if not validity:
        negativity = False
    value = nan_type(validity, nan, value, del_value_nan)
    if data_type == DataTypes.DECIMAL or DataTypes.INT:
        if value != '':
            value = negative_type(validity, negative, value, negativity)
    return value


class InputFiles:
    @staticmethod
    def create(check_input_url, params=None):
        if params is None:
            params = [(False, False, False),
                      (True, True, False, True),
                      (True, False, False, True),
                      (True, False, True)]

        table = GoogleSheets.pars(check_input_url)
        file_names = Counter([row[0] for row in table][1:])

        folder_name = 'files'
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        for file_name in file_names.keys():
            count_col = file_names.get(file_name)
            column_names = [row[1] for row in table if row[0] == file_name]
            data = [[] for _ in range(len(params))]
            for i in range(len(params)):
                count = 0
                for column_name in column_names:
                    for row in table:
                        if row[0] == file_name and row[1] == column_name:
                            if len(params[i]) > 3 and params[i][3]:
                                count += 1
                                if count <= (count_col // 2):
                                    data[i].append(create_data(row[2], row[3], row[4],
                                                               params[i][0],
                                                               params[i][1],
                                                               params[i][2]))
                                    break
                                else:
                                    data[i].append(create_data(row[2], row[3], row[4],
                                                               params[i][0],
                                                               not params[i][1],
                                                               params[i][2]))
                                    break
                            else:
                                data[i].append(create_data(row[2], row[3], row[4], *params[i]))
                                break

            file_path = rf'{folder_name}\{file_name}.csv'
            if os.path.exists(file_path):
                os.remove(file_path)

            df = pd.DataFrame(data, columns=column_names)
            df.to_csv(file_path, index=False)


InputFiles.create(CheckInputUrls.PROMO)

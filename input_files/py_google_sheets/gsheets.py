import os
import time

from console_design.colors import ConsoleColors as CCol

import googleapiclient.errors
import pygsheets
import gdown
import pandas


def find_client_secret(path, file_name):
    for rootdir, dirs, files in os.walk(path):
        for file in files:
            if file == file_name:
                return os.path.join(rootdir, file)


def to_matrix(tables):
    result = []
    for table in tables:
        list_for_table = []
        column_name = [*table[0].keys()]
        list_for_table.append(column_name)
        for dict_in_table in table:
            list_for_table.append([*dict_in_table.values()])
        result.append(list_for_table)
    return result


class GoogleSheets:
    @staticmethod
    def download_file_from_google_drive(spreadsheet_link, miss_worksheets=None, invert_miss_worksheets=False):
        if miss_worksheets is None:
            miss_worksheets = []

        file_id = spreadsheet_link[
                  spreadsheet_link.index('/d/') + 3:spreadsheet_link.index('/', spreadsheet_link.index('/d/') + 3)]
        file_name = f"{file_id}.xlsx"

        gdown.download(id=file_id, output=file_name, quiet=False)
        print('====End downloading.')

        spreadsheet = pandas.read_excel(io=file_name,
                                        index_col=None,
                                        sheet_name=None,
                                        dtype=str,
                                        keep_default_na=False)
        worksheets_names = [*spreadsheet.keys()]
        # spreadsheet = {'check': spreadsheet.applymap(lambda x: str(x))}

        tables = []
        for i in range(len(spreadsheet)):
            if len(miss_worksheets) > 0:
                if invert_miss_worksheets:
                    if worksheets_names[i] not in miss_worksheets:
                        print(f'========Worksheet: "{worksheets_names[i]}" {CCol.txt_yel("SKIPPED")}')
                        continue
                else:
                    if worksheets_names[i] in miss_worksheets:
                        print(f'========Worksheet: "{worksheets_names[i]}" {CCol.txt_yel("SKIPPED")}')
                        continue
            print(f'========Reading worksheet: "{worksheets_names[i]}".', end=' ')
            start = time.time()
            tables.append(spreadsheet.get(worksheets_names[i]).to_dict('records'))
            end = time.time() - start
            print(f'=={CCol.txt_grn("DONE")}: ', round(end, 3))

        os.remove(file_name)
        print('====Removed downloaded file.')

        return tables, worksheets_names

    @staticmethod
    def pars(spreadsheet_link, miss_worksheets=None, invert_miss_worksheets=False):
        if miss_worksheets is None:
            miss_worksheets = []

        print('====Start parsing')
        start_pars = time.time()

        try:
            client = pygsheets.authorize(client_secret=find_client_secret(os.getcwd(), 'client_secret.json'),
                                         service_file=find_client_secret(os.getcwd(), 'pygsheets_key.json'))
            spreadsheet = client.open_by_url(spreadsheet_link)
            worksheets_list = spreadsheet.worksheets()
            worksheets_names = [
                str(sheet)[str(sheet).index(" '") + 2:str(sheet).index("' index")].strip() for sheet in worksheets_list]
            tables = []
            for i in range(len(worksheets_list)):
                if len(miss_worksheets) > 0:
                    if invert_miss_worksheets:
                        if worksheets_names[i] not in miss_worksheets:
                            print(f'========Worksheet: "{worksheets_names[i]}" {CCol.txt_yel("SKIPPED")}')
                            continue
                    else:
                        if worksheets_names[i] in miss_worksheets:
                            print(f'========Worksheet: "{worksheets_names[i]}" {CCol.txt_yel("SKIPPED")}')
                            continue
                print(f'========Parsing worksheet: "{worksheets_names[i]}".', end=' ')
                start = time.time()
                tables.append(worksheets_list[i].get_all_records(numericise_data=False))
                end = time.time() - start
                print(f'=={CCol.txt_grn("DONE")}: ', round(end, 3))

            worksheets_names = [elem for elem in worksheets_names if elem not in miss_worksheets]

            end_pars = time.time() - start_pars
            print('====End parsing. Time: ', round(end_pars, 3), end='\n\n')
            return to_matrix(tables), worksheets_names
        except googleapiclient.errors.HttpError:
            txt = "Can't pars google sheet, start downloading..."
            print(f'===={CCol.txt_yel(txt)}')
            tables, worksheets_names = GoogleSheets.download_file_from_google_drive(spreadsheet_link,
                                                                                    miss_worksheets,
                                                                                    invert_miss_worksheets)

            worksheets_names = [elem.strip() for elem in worksheets_names if elem not in miss_worksheets]

            end_pars = time.time() - start_pars
            print('====End parsing. Time: ', round(end_pars, 3), end='\n\n')
            return to_matrix(tables), worksheets_names

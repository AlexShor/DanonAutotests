import os
import pygsheets


def find_client_secret(path, file_mane):
    for rootdir, dirs, files in os.walk(path):
        for file in files:
            if file == file_mane:
                return os.path.join(rootdir, file)


class GoogleSheets:
    @staticmethod
    def pars(spreadsheet_link, pars_range=('A1', '')):
        client = pygsheets.authorize(client_secret=find_client_secret(os.getcwd(), 'client_secret.json'))
        spreadsheet = client.open_by_url(spreadsheet_link)
        worksheet = spreadsheet.sheet1
        if pars_range != ('A1', ''):
            return worksheet.range(f'{":".join(pars_range)}', returnas='matrix')
        else:
            row_count = len(worksheet.get_col(1, returnas='matrix', include_tailing_empty=False))
            return worksheet.range(f'A1:E{row_count}', returnas='matrix')
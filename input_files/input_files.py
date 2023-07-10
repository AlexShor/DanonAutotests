import os
from collections import OrderedDict

from py_google_sheets.gsheets import GoogleSheets
from check_input_urls import CheckInputUrls
import pandas as pd


class InputFiles:
    @staticmethod
    def create():
        table = GoogleSheets.pars(CheckInputUrls.PROMO)
        files = list(OrderedDict.fromkeys([row[0] for row in table]))[1:]

        folder_name = 'files'
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        for file in files:
            # columns = ['Date', 'Model', 'Mark']
            columns = [f[1] for f in table if f[0] == file]

            # data = [
            #     ['2019-02-26', 'CE255X', 'nv print'],
            #     ['2019-02-26', 'CE255X', 'nv print'],
            #     ['2019-02-26', 'CE255X', 'nv print'],
            #     ['2019-02-26', 'CE255X', 'nv print']
            # ]

            data = []

            df = pd.DataFrame(data, columns=columns)
            df.to_csv(rf'{folder_name}\{file}.csv', index=False)

        # print(files)


InputFiles.create()

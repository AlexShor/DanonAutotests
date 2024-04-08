import os
from datetime import date
from typing import Type, Iterable

from custom_moduls.console_design.indentation_levels import indentation_levels as Ilvl
from optimizer_data.data.input_speadsheets_data import Spreadsheets
from optimizer_data.data.input_type_name_matches import InputTypeNameMatch
from optimizer_data.data.default_data_for_filling import ErrorLogText

import pandas as pd
import requests


class OperationsFileData:
    def __init__(self, destination: str = 'files/'):
        if not os.path.exists(destination):
            os.makedirs(destination)
        self.destination = destination

    @staticmethod
    def _get_confirm_token(response: requests.Response) -> str | None:
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    @staticmethod
    def _save_response_content(
        response: requests.Response,
        destination: str,
        file_name: str,
        chunk_size: int = 32768) -> None:

        with open(destination + file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    def get_from_google_drive(self, file_id: str, file_name: str) -> None:
        url = Spreadsheets.GOOGLE_EXPORT_URL

        session = requests.Session()
        response = session.get(url, params={"id": file_id}, stream=True)

        token = self._get_confirm_token(response)
        if token:
            params = {"id": file_id, "confirm": token}
            response = session.get(url, params=params, stream=True)

        self._save_response_content(response, self.destination, file_name)
        print(f'{Ilvl(1)}Downloaded file: "{file_name}".')

    def delete(self, file_name: str) -> None:
        os.remove(self.destination + file_name)
        print(f'{Ilvl(1)}Deleted file: "{file_name}".')

    def read_xlsx(
        self,
        file_name: str,
        worksheet_name: str | int = 0,
        get_columns: int | Iterable[str] | None = None,
        skip_footer_rows: int = 0) -> list[dict]:

        spreadsheet = pd.read_excel(io=self.destination + file_name,
                                    usecols=get_columns,
                                    index_col=None,
                                    sheet_name=worksheet_name,
                                    dtype=str,
                                    keep_default_na=False,
                                    skipfooter=skip_footer_rows)

        return spreadsheet.to_dict('records')

    @staticmethod
    def _convert_valid_rules_data_type(data_type: str, data_type_rules: dict):
        return data_type_rules[data_type]

    @staticmethod
    def _convert_valid_rules_negativity(
        negativity: str,
        negativity_rules: dict,
        data_type: Type[int] | Type[float] | Type[str] | Type[date] | Type[bool] = None):

        if not isinstance(data_type, int | float) and negativity == '':
            return None
        return negativity_rules[negativity]

    @staticmethod
    def _convert_valid_rules_obligatory(obligatory: str, obligatory_rules: dict):

        return obligatory_rules[obligatory]

    @classmethod
    def convert_validation_rules_data_to_dict(cls, validation_rules_data: list[dict], valid_rules: dict):

        converted_validation_rules_data = {}

        for row in validation_rules_data:
            file_name = row[valid_rules['col_names']['system_file_name']]
            col = row[valid_rules['col_names']['col']]
            data_type = cls._convert_valid_rules_data_type(
                row[valid_rules['col_names']['data_type']],
                valid_rules['data_type'])
            negativity = cls._convert_valid_rules_negativity(
                row[valid_rules['col_names']['negativity']],
                valid_rules['negativity'],
                data_type)
            obligatory = cls._convert_valid_rules_obligatory(
                row[valid_rules['col_names']['obligatory']],
                valid_rules['obligatory'])

            converted_validation_rules_data.setdefault(file_name, {}).update(
                {col: {
                    'data_type': data_type,
                    'negativity': negativity,
                    'obligatory': obligatory,
                }}
            )

        return converted_validation_rules_data

    def _read_and_convert_err_log(
        self,
        file_path: str,
        error_log_text: dict,
        file_type: str = 'txt') -> dict:

        with open(f'{file_path}.{file_type}', 'r', encoding='utf8') as file:
            file_data = file.read().rstrip().split('\n\n')

        converted_error_log = {}

        for error_type in file_data:
            error_name, errors_data = error_type.split(" ['")
            errors_data = errors_data.strip("']").split("', '")

            converted_error_log[error_log_text[error_name]] = set(errors_data)

        return converted_error_log

    def read_error_logs(
        self,
        input_name_match: dict,
        folder_path: str = '',
        error_log_lang: str = 'eng') -> dict:

        folder_path = f'{self.destination}/{folder_path}/error_logs'
        error_log_text = {v: k for k, v in ErrorLogText.get(error_log_lang).items()}

        error_logs = {}

        for input_name, input_data in input_name_match.items():
            file_path = f'{folder_path}/{input_data["system_file_name"]}'
            errors_file_data = self._read_and_convert_err_log(file_path, error_log_text=error_log_text)

            error_logs[input_name] = errors_file_data

        return error_logs

    @staticmethod
    def errors_logs_comparison(created_error_logs: dict, received_error_logs: dict):
        pass


if __name__ == "__main__":
    file_id = Spreadsheets.Tetris.CHECK_INPUT_ID
    file_name = "test_file.xlsx"
    # OperationFileData().get_from_google_drive(file_id, file_name)

    # tetris_valid_rules = ValidateRules.Tetris.VALID_RULES
    # columns = tetris_valid_rules['col_names'].values()
    # data = OperationsFileData().read_xlsx(file_name, 'Validation rules', get_columns=columns, skip_footer_rows=291)
    # data2 = OperationsFileData().convert_validation_rules_data_to_dict(data, tetris_valid_rules)

    data3 = OperationsFileData().read_error_logs(InputTypeNameMatch.Tetris.TYPES, folder_path='test', error_log_lang='rus')

    print(data3)

    # print(*data, sep='\n')

    # for fk, fv in data3.items():
    #     print(fk)
    #     for ck, cv in fv.items():
    #         print(ck)
    #         print(cv)

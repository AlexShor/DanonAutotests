import os
from datetime import date
from typing import Type, Iterable

from optimizer_data.data.default_data import ErrorLogText

import pandas as pd
import requests


class OperationsFileData:
    def __init__(self, inputs_data: dict, destination: str) -> None:

        if not os.path.exists(destination):
            os.makedirs(destination)
        self._destination = destination
        self._inputs_data = inputs_data

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

        with open(f'{destination}/{file_name}', "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    def get_from_google_drive(self, spreadsheet_link: str, file_name: str) -> None:

        url, spreadsheet_data = spreadsheet_link
        file_id = spreadsheet_data['id']

        session = requests.Session()
        response = session.get(url, params={"id": file_id}, stream=True)

        token = self._get_confirm_token(response)
        if token:
            params = {"id": file_id, "confirm": token}
            response = session.get(url, params=params, stream=True)

        self._save_response_content(response, self._destination, file_name)

    def delete(self, file_name: str) -> None:

        os.remove(self._destination + file_name)

    def read_xlsx(
        self,
        file_name: str,
        worksheet_name: str | int = 0,
        get_columns: int | Iterable[str] | None = None,
        skip_footer_rows: int = 0) -> list[dict]:

        spreadsheet = pd.read_excel(io=f'{self._destination}/{file_name}',
                                    usecols=get_columns,
                                    index_col=None,
                                    sheet_name=worksheet_name,
                                    dtype=str,
                                    keep_default_na=False,
                                    skipfooter=skip_footer_rows)

        return spreadsheet.to_dict('records')

    class __convert_rules:
        class base:
            @staticmethod
            def str_to_type(
                string: str, type_rule: dict
            ) -> Type[int] | Type[float] | Type[str] | Type[date] | Type[bool]:

                return type_rule[string]

            @staticmethod
            def split_by(validation: str, separator: str = '+') -> list | None:

                if validation:
                    return validation.lower().split(separator)
                return None

        class validate:
            @staticmethod
            def negativity(
                negativity: str,
                negativity_rules: dict,
                data_type: Type[int] | Type[float] | Type[str] | Type[date] | Type[bool] = None) -> bool | None:

                if not isinstance(data_type, int | float) and negativity == '':
                    return None
                return negativity_rules[negativity]

        class preview:
            @staticmethod
            def decimal_places(string: str) -> int | None:

                if string.isdigit():
                    return int(string)
                return None

    def convert_validation_rules_data_to_dict(self, validation_rules_data: list[dict], valid_rules: dict) -> dict:

        input_names = {value['system_file_name']: key for key, value in self._inputs_data.items()}

        converted_validation_rules_data = {}

        for row in validation_rules_data:

            file_name = row[valid_rules['col_names']['system_file_name']]
            system_file_name = input_names[file_name]

            col = row[valid_rules['col_names']['col']]

            data_type = self.__convert_rules.base.str_to_type(
                row[valid_rules['col_names']['data_type']],
                valid_rules['data_type'])

            negativity = self.__convert_rules.validate.negativity(
                row[valid_rules['col_names']['negativity']],
                valid_rules['negativity'],
                data_type)

            obligatory = self.__convert_rules.base.str_to_type(
                row[valid_rules['col_names']['obligatory']],
                valid_rules['obligatory'])

            key = self.__convert_rules.base.str_to_type(
                row[valid_rules['col_names']['key']],
                valid_rules['key'])

            validation = self.__convert_rules.base.split_by(
                row[valid_rules['col_names']['validation']])

            only_for_download_and_preview = self.__convert_rules.base.str_to_type(
                row[valid_rules['col_names']['only_for_download_and_preview']],
                valid_rules['only_for_download_and_preview'])

            auto_mapping = self.__convert_rules.base.split_by(
                row[valid_rules['col_names']['auto_mapping']])

            converted_validation_rules_data.setdefault(system_file_name, {}).update(
                {col: {
                    'data_type': data_type,
                    'negativity': negativity,
                    'obligatory': obligatory,
                    'key': key,
                    'validation': validation,
                    'only_for_download_and_preview': only_for_download_and_preview,
                    'auto_mapping': auto_mapping
                }}
            )

        return converted_validation_rules_data

    @classmethod
    def convert_preview_rules_data_to_dict(cls, preview_rules_data: list[dict], preview_rules: dict) -> dict:

        converted_preview_rules_data = {}

        for row in preview_rules_data:

            col = row[preview_rules['col_names']['col']]

            decimal_places = cls.__convert_rules.preview.decimal_places(
                row[preview_rules['col_names']['decimal_places']])

            percentage = cls.__convert_rules.base.str_to_type(
                row[preview_rules['col_names']['percentage']],
                preview_rules['percentage'])

            separator = cls.__convert_rules.base.str_to_type(
                row[preview_rules['col_names']['separator']],
                preview_rules['separator'])

            converted_preview_rules_data[col] = {
                    'decimal_places': decimal_places,
                    'percentage': percentage,
                    'separator': separator
                }

        return converted_preview_rules_data

    @staticmethod
    def read_txt(file_path: str, file_type: str = 'txt') -> str:
        with open(f'{file_path}.{file_type}', 'r', encoding='utf8') as file:
            file_data = file.read()

        return file_data

    def convert_txt_err_log_to_dict(self, txt_err_logs_data: dict, error_log_lang: str) -> dict:
        error_log_text_lang = {v: k for k, v in ErrorLogText().get(error_log_lang).items()}

        converted_error_logs = {}

        for input_name, txt_err_log in txt_err_logs_data.items():

            if self._inputs_data.get(input_name, {}).get('active'):

                converted_error_log = {}

                for error_type in txt_err_log.rstrip().split('\n\n'):

                    error_name, errors_data = error_type.split(" ['")
                    errors_data = errors_data.strip("']").split("', '")

                    converted_error_log[error_log_text_lang[error_name]] = set(errors_data)

                converted_error_logs[input_name] = converted_error_log

        return converted_error_logs

    def read_error_logs(self, error_log_lang: str = 'eng') -> dict:

        error_logs_text = {}

        for input_name, input_data in self._inputs_data.items():

            file_path = f'{self._destination}/{input_name}'

            error_logs_text[input_name] = self.read_txt(file_path)

        error_logs = self.convert_txt_err_log_to_dict(error_logs_text, error_log_lang)

        return error_logs

    @staticmethod
    def errors_logs_comparison(created_error_logs: dict, received_error_logs: dict) -> None:
        print(created_error_logs)
        print(received_error_logs)

        for input_name, received_error_log_data in received_error_logs.items():
            created_error_log_data = created_error_logs.get(input_name)

            print(input_name.upper())
            for error_type in ('obligation', 'type', 'negative'):

                received_errors = set(received_error_log_data.get(error_type, []))
                created_errors = set(created_error_log_data.get(error_type, []))

                created_not_have_errors = received_errors.difference(created_errors)
                received_not_have_errors = created_errors.difference(received_errors)

                if created_not_have_errors or received_not_have_errors:
                    print(error_type)
                    if created_not_have_errors:
                        print('created_not_have_errors:', created_not_have_errors)
                    if received_not_have_errors:
                        print('received_not_have_errors:', received_not_have_errors)


# if __name__ == "__main__":
#     optimizer_type = 'tetris'
#     inputs_data = InputData(optimizer_type).get_from_json()
#
#     preview_rules_path = FileDirectory(optimizer_type).input_files_error_logs
#
#
#     operation = OperationsFileData(preview_rules_path)
#
#     created_error_logs = operation.read_error_logs(inputs_data, error_log_lang='rus')
#     print(created_error_logs)
#
#
#
#     received_error_logs = operation.convert_txt_err_log_to_dict()


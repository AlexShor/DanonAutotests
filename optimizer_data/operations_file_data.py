import os
import re
from re import findall
from datetime import date, datetime
from typing import Type, Iterable

from optimizer_data.data.default_data import ErrorLogText, FileDirectory
from optimizer_data.data.input_speadsheets_data import ValidateRules, Spreadsheets
from custom_moduls.console_design.console_decorator import log_file_operation, log_api_status

import pandas as pd
import requests
from styleframe import StyleFrame, utils, Styler


class OperationsFileData:
    def __init__(self, destination: str = None, inputs_data: dict = None) -> None:

        if destination is not None:

            if not os.path.exists(destination):
                os.makedirs(destination)

            self._destination = destination

        else:
            self._destination = ''

        if inputs_data:
            self._inputs_data = inputs_data

        else:
            self._inputs_data = {}

    @staticmethod
    @log_file_operation(2)
    def _save_response_content(
        response: requests.Response,
        destination: str,
        file_name: str,
        chunk_size: int = 32768) -> None:

        with open(f'{destination}/{file_name}', "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    @log_api_status(1)
    def _get_data_from_google_drive(self, spreadsheet_link: str):

        url, spreadsheet_data = spreadsheet_link
        file_id = spreadsheet_data['id']

        response = requests.get(url, params={"id": file_id}, stream=True)

        return response

    def get_from_google_drive(self, spreadsheet_link: str, file_name: str) -> int:

        response = self._get_data_from_google_drive(spreadsheet_link)

        if 200 <= response.status_code < 300:
            self._save_response_content(response, self._destination, file_name)

        return response.status_code

    def delete(self, file_name: str) -> None:

        os.remove(self._destination + file_name)

    def read_xlsx(
        self,
        file_name: str,
        worksheet_name: str | int = 0,
        get_columns: int | Iterable[str] | None = None,
        skip_footer_rows: int = 0,
        style_conditions: dict = None) -> list[dict]:

        if style_conditions:

            sf = StyleFrame.read_excel(path=f'{self._destination}/{file_name}',
                                       usecols=get_columns,
                                       index_col=None,
                                       sheet_name=worksheet_name,
                                       dtype=str,
                                       keep_default_na=False,
                                       skipfooter=skip_footer_rows,
                                       read_style=True)

            columns = sf.columns

            checked_style_conditions = []
            for row in sf[columns[0]].style:
                check = all([row.__dict__.get(key) == style_conditions.get(key) for key in style_conditions])
                checked_style_conditions.append(check)

            rows_without_strikethrough = sf.loc[checked_style_conditions]

            result = []

            for i in range(len(rows_without_strikethrough)):
                result.append({str(column): str(rows_without_strikethrough[column][i]) for column in columns})

            return result

        else:

            df = pd.read_excel(io=f'{self._destination}/{file_name}',
                               usecols=get_columns,
                               index_col=None,
                               sheet_name=worksheet_name,
                               dtype=str,
                               keep_default_na=False,
                               skipfooter=skip_footer_rows)

            return df.to_dict('records')

    class __convert_rules:
        class base:
            @staticmethod
            def str_to_type(string: str, type_rule: dict) \
                -> (Type[int] | Type[float]
                    | Type[str] | Type[date]
                    | Type[datetime] | Type[bool]
                    | tuple | str | None):

                if type_rule is not None:

                    _type = type_rule.get(string, 'nan_check')

                    if _type != 'nan_check':
                        return _type

                    string, additional_value = findall(r'(\w+)\(([\w-]*)\)', string)[0]

                    return type_rule.get(string), additional_value

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

                negativity = re.search(r'[A-Za-z+]+', negativity).group()

                return negativity_rules[negativity]

        class preview:
            @staticmethod
            def decimal_places(string: str) -> int | None:
                if string.isdigit():
                    return int(string)
                return None

    def convert_validation_rules_data_to_dict(self, validation_rules_data: list[dict], valid_rules: dict) -> dict:

        if self._inputs_data:
            input_names = {value['system_file_name']: key for key, value in self._inputs_data.items()}
        else:
            input_names = {}

        converted_validation_rules_data = {}

        for row in validation_rules_data:

            file_name = row[valid_rules['col_names']['system_file_name']]
            system_file_name = input_names.get(file_name, file_name)

            col = row[valid_rules['col_names']['col']]

            data_type = self.__convert_rules.base.str_to_type(
                row[valid_rules['col_names']['data_type']],
                valid_rules['data_type'])

            negativity = self.__convert_rules.validate.negativity(
                row[valid_rules['col_names']['negativity']],
                valid_rules['negativity'],
                data_type
            )

            obligatory = self.__convert_rules.base.str_to_type(
                row[valid_rules['col_names']['obligatory']],
                valid_rules['obligatory']
            )

            if isinstance(obligatory, tuple):
                obligatory, default_if_obligatory_null = obligatory
            else:
                obligatory, default_if_obligatory_null = obligatory, None

            key = self.__convert_rules.base.str_to_type(
                row.get(
                    valid_rules['col_names'].get('key')
                ),
                valid_rules.get('key')
            )

            validation = self.__convert_rules.base.split_by(
                row.get(
                    valid_rules['col_names'].get('validation')
                )
            )

            only_for_download_and_preview = self.__convert_rules.base.str_to_type(
                row.get(
                    valid_rules['col_names'].get('only_for_download_and_preview')
                ),
                valid_rules.get('only_for_download_and_preview')
            )

            auto_mapping = self.__convert_rules.base.split_by(
                row.get(
                    valid_rules['col_names'].get('auto_mapping')
                )
            )

            converted_validation_rules_data.setdefault(system_file_name, {}).update(
                {col: {
                    'data_type': data_type,
                    'negativity': negativity,
                    'obligatory': obligatory,
                    'default_if_obligatory_null': default_if_obligatory_null,
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
    def errors_logs_comparison(created_error_logs: dict, received_error_logs: dict) -> dict:

        errors_logs_comparison_result = {}

        for input_name, received_error_log_data in received_error_logs.items():
            created_error_log_data = created_error_logs.get(input_name)

            errors = {}

            for error_type in ('obligation', 'type', 'negative'):

                received_errors = set(received_error_log_data.get(error_type, []))
                created_errors = set(created_error_log_data.get(error_type, []))

                created_not_have_errors = received_errors.difference(created_errors)
                received_not_have_errors = created_errors.difference(received_errors)

                if created_not_have_errors or received_not_have_errors:

                    errors[error_type] = {
                        'created_not_have_errors': created_not_have_errors,
                        'received_not_have_errors': received_not_have_errors
                    }

                else:
                    errors[error_type] = None

            errors_logs_comparison_result[input_name] = errors

        return errors_logs_comparison_result

    def split_file(self, file_name: str, size: int = 1_000_000, file_type: str = 'csv') -> None:

        readable_file_path = self._destination

        if readable_file_path != '':
            readable_file_path = readable_file_path + '/'

        creatable_file_path = f'{readable_file_path}{file_name}'

        if not os.path.exists(creatable_file_path):
            os.makedirs(creatable_file_path)

        with open(f'{readable_file_path}{file_name}.{file_type}', 'r', encoding='utf8') as csv_file:

            column_names = [csv_file.readline()]
            file_data = csv_file.readlines()

        file_number = 1

        for i in range(0, len(file_data), size):
            new_file_name = f'{file_name}_{file_number}.{file_type}'

            print(new_file_name)

            with open(f'{creatable_file_path}/{new_file_name}', 'w+', encoding='utf8') as new_file:
                new_file_data = column_names + file_data[i:i + size]
                new_file.writelines(new_file_data)

            file_number += 1

    def get_durectory_to_last_validation_ruls(self, optimizer_type: str) -> dict:

        files = [f'{self._destination}/{file}' for file in os.listdir(self._destination)]

        last_created_file = max(files, key=os.path.getctime).split('/')
        last_created_file = {'file_directory': '/'.join(last_created_file[:-1]), 'file_name': last_created_file[-1]}

        return last_created_file

    @staticmethod
    def determine_file_type(file_directory: str, file_name: str):

        files = [f'{file_directory}/{file}' for file in os.listdir(file_directory)]


        for file in files:
            if file_name == file.split('/')[-1].split('.')[0]:
                return file

    @log_file_operation(1)
    def extract_downloaded_file_from_zip_and_update_input_data(self):

        from zipfile import ZipFile

        zip_directory = self._destination
        inputs_data = self._inputs_data

        result = []

        try:

            with ZipFile(f'{zip_directory}.zip') as zip_file:
                zip_file.extractall(zip_directory)

            files = [f'{zip_directory}/{file}' for file in os.listdir(zip_directory)]
            for file in files:

                file_name_type = file.split('/')[-1].split('.')
                if file_name_type[0].lower().startswith('input'):
                    if file_name_type[1] == 'zip':

                        big_input = f'{zip_directory}/{file_name_type[0]}'

                        with ZipFile(f'{big_input}.zip') as zip_file:
                            zip_file.extractall(big_input)

                        big_input_files = [f'{big_input}/{file}' for file in os.listdir(big_input)]

                        big_input_file_name = big_input_files[0].split('/')[-1].split('.')[0]

                        for input_name, input_data in inputs_data.items():

                            download_file_name = input_data['download_file_name']
                            if download_file_name is not None and download_file_name in big_input_file_name:
                                inputs_data[input_name].update({'full_path': big_input_files})

                    else:

                        for input_name, input_data in inputs_data.items():
                            if input_data['download_file_name'] == file_name_type[0]:
                                inputs_data[input_name].update({'full_path': file})

        except Exception as exc:
            return exc

        return inputs_data

    @log_file_operation(1)
    def remove_data(self):

        try:
            os.remove(self._destination)
        except Exception as exc:
            return exc

if __name__ == '__main__':
    # dir = 'C:/Users/LexSh/YandexDisk-Alex.Shor/Spectr/Projects/Advanced/Danon/DanonAutotests/optimizer_data/files/input/promo/valid_input_files/files'
    # dir = 'C:/Users/LexSh/Downloads/25_Detailed_20240617_mb_Copy_1_20240626-09_24'
    # res = OperationsFileData.determine_file_type(dir, 'Input_FC')
    #
    # print(res)

    dir = 'C:/Users/LexSh/Downloads/test/25_Detailed_20240617_mb_Copy_1_20240626-10_39'
    OperationsFileData.extract_downloaded_file_from_zip_and_update_input_data(dir)

import os
from copy import deepcopy

from optimizer_data.data.input_speadsheets_data import ValidateRules
from optimizer_data.data.default_data import DefaultDataFill, ErrorLogText, FileDirectory
from optimizer_data.operations_file_data import OperationsFileData

import pandas as pd


class CreateFileData:
    @staticmethod
    def _save_file(
        file_name: str,
        file_data: dict,
        save_directory: str,
        file_type: str = 'xlsx',
        as_error_log=False) -> None:

        file_path = f'{save_directory}/{file_name}'

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        if as_error_log:
            error_log_data = [f'{_type} {repr(_data)}' for _type, _data in file_data.items()]

            with open(f'{file_path}.txt', 'w', encoding='utf8') as file:
                print(*error_log_data, sep='\n\n', file=file)

            return None

        df = pd.DataFrame(file_data)

        if file_type == 'xlsx':
            df.to_excel(f'{file_path}.{file_type}', index=False)
        elif file_type == 'csv':
            df.to_csv(f'{file_path}.{file_type}', index=False)
        else:
            raise TypeError(f'Wrong file type: "{file_type}"')

    @classmethod
    def invalid_files(
        cls,
        valid_rules_data: dict,
        save_directory: str | FileDirectory,
        file_type: str = 'xlsx',
        error_log_text_lang: str = 'eng') -> None:

        if isinstance(save_directory, str):
            invalid_files_directory = save_directory
            error_logs_directory = invalid_files_directory + '/errors_logs'
        else:
            invalid_files_directory = save_directory.invalid_input_files
            error_logs_directory = save_directory.input_files_error_logs

        for file_name, file_data in valid_rules_data.items():

            created_invalid_data, error_log_data = cls._creating_invalid_data(file_data, error_log_text_lang)

            cls._save_file(file_name, created_invalid_data, invalid_files_directory, file_type)
            cls._save_file(file_name, error_log_data, error_logs_directory, as_error_log=True)

    @classmethod
    def _creating_invalid_data(cls, file_data: dict, error_log_text_lang: str = 'eng') -> (dict, dict):

        invalid_data = {}
        error_log_data = {}
        error_log_text = ErrorLogText.get(error_log_text_lang)

        def __error_log_data(col_name: str, type_error: str, row: int) -> None:

            error_log_data.setdefault(error_log_text[type_error], []).append(
                f'{error_log_text["row"]} {row} - {error_log_text["col"]} {col_name.lower()}'
            )

        def __get_validity_data(col_name: str, data: dict, validity: bool, row: int) -> str:

            if not validity:
                __error_log_data(col_name, 'type', row)

            return DefaultDataFill.get(data['data_type'], validity)

        def __get_obligatory_data(col_name: str, data: dict, row: tuple, switch: bool) -> tuple:

            if data['obligatory']:
                __error_log_data(col_name, 'obligation', row[not switch])

            if switch:
                return '', __get_validity_data(col_name, data, True, row[switch])

            return __get_validity_data(col_name, data, True, row[switch]), ''

        def __get_negativity_data(col_name: str, data: dict, row: int) -> str:

            data_type = data['data_type']
            if data_type in (int, float):

                if data['negativity'] is False:
                    __error_log_data(col_name, 'negative', row)

                return '-' + DefaultDataFill.get(data_type, True)

            return __get_validity_data(col_name, data, True, row)

        def __get_integrity_data(col_name: str, data: dict, row: int, negativity: bool = False) -> str:

            types = [int, float]
            data = deepcopy(data)
            data_type = data['data_type']

            if data_type in types:
                types.remove(data_type)

                if data_type is int:
                    __error_log_data(col_name, 'type', row)
                    data['negativity'] = None

                if negativity:
                    data['data_type'] = types[0]
                    return __get_negativity_data(col_name, data, row)
                else:
                    return DefaultDataFill.get(types[0], True)

            return __get_validity_data(col_name, data, True, row)

        obligatory_switch = True

        for col_name, col_valid_data in file_data.items():
            new_col_data = [
                __get_validity_data(col_name=col_name, data=col_valid_data, validity=False, row=2),
                *__get_obligatory_data(col_name=col_name, data=col_valid_data, row=(3, 4), switch=obligatory_switch),
                __get_negativity_data(col_name=col_name, data=col_valid_data, row=5),
                __get_integrity_data(col_name=col_name, data=col_valid_data, row=6, negativity=False),
                __get_integrity_data(col_name=col_name, data=col_valid_data, row=7, negativity=True),
                __get_validity_data(col_name=col_name, data=col_valid_data, validity=True, row=8)
            ]

            invalid_data.update({col_name: new_col_data})

            obligatory_switch = not obligatory_switch

        return invalid_data, error_log_data


if __name__ == "__main__":

    file_name = "validation_rules_tetris.xlsx"
    validation_rules_path = FileDirectory().validation_rules
    # invalid_input_files_path = FileDirectory('tetris').validation_rules

    tetris_valid_rules = ValidateRules.get('tetris')
    columns = tetris_valid_rules['col_names'].values()

    xlsx_data = OperationsFileData(validation_rules_path).read_xlsx(file_name, 'Validation rules', get_columns=columns, skip_footer_rows=291)
    valid_rules_data = OperationsFileData.convert_validation_rules_data_to_dict(xlsx_data, tetris_valid_rules)
    print(valid_rules_data)
    # CreateFileData.invalid_files(valid_rules_data, save_directory=invalid_input_files_path, error_log_text_lang='rus')

    # res = CreateFileData._creating_invalid_data(valid_rules_data['Buyers contracts'], error_log_text_lang='rus')

    # print(res)


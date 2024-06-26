import json
from copy import deepcopy
from collections.abc import Mapping

from optimizer_data.data.default_data import FileDirectory
from optimizer_data.data.input_speadsheets_data import ValidateRules, PreviewRules, Spreadsheets
from optimizer_data.operations_file_data import OperationsFileData
from optimizer_data.data.input_type_name_matches import InputTypeNameMatch
from custom_moduls.console_design.console_decorator import log_validation_rules_comparison


class InputData:
    def __init__(self, optimizer_type: str, file_name: str = None) -> None:
        self._file_path = FileDirectory().input_data_json
        self._optimizer_type = optimizer_type

        if file_name is None:
            self._file_name = f'{optimizer_type}.json'
        else:
            self._file_name = file_name

    def _get_valid_rules_data(self, file_directory: str, file_name: str) -> dict:

        valid_rules = ValidateRules.get(self._optimizer_type)
        columns = valid_rules['col_names'].values()

        operation = OperationsFileData(file_directory)

        spreadsheet_params = Spreadsheets.get(self._optimizer_type, 'validation_rules')[1]['params']
        rules_data = operation.read_xlsx(file_name, get_columns=columns, **spreadsheet_params)

        converted_valid_rules = operation.convert_validation_rules_data_to_dict(rules_data, valid_rules)

        return converted_valid_rules

    def _get_preview_rules_data(self) -> dict:

        preview_rules = PreviewRules.get(self._optimizer_type)

        if preview_rules is None:
            return {}

        file_name = f'preview_rules_{self._optimizer_type}.xlsx'

        columns = preview_rules['col_names'].values()

        operation = OperationsFileData(FileDirectory().preview_rules)

        spreadsheet_params = Spreadsheets.get(self._optimizer_type, 'preview_rules')[1]['params']
        rules_data = operation.read_xlsx(file_name, get_columns=columns, **spreadsheet_params)

        converted_preview_rules = operation.convert_preview_rules_data_to_dict(rules_data, preview_rules)

        return converted_preview_rules

    def _write_json(self, write_data: dict):

        with open(f'{self._file_path}/{self._file_name}', 'w', encoding='utf8') as file:
            json.dump(write_data, file, indent=4, ensure_ascii=False)

    def create_json(self, input_type_name_match: dict) -> None:

        valid_rules_data = self._get_valid_rules_data()
        preview_rules_data = self._get_preview_rules_data()

        new_data = {}

        for in_name, in_data in input_type_name_match.items():
            new_in_data = {}
            for n_in_data, d_in_data in in_data.items():
                new_in_data['active'] = True
                new_in_data[n_in_data] = d_in_data

            system_file_name = in_data['system_file_name']
            valid_rule = valid_rules_data[system_file_name]
            new_valid_rule = {}
            for col_nam, col_data in valid_rule.items():
                col_data['active'] = True

                col_data['data_type'] = col_data['data_type'].__name__

                col_data['preview_rules'] = preview_rules_data.get(col_nam)

                new_valid_rule[col_nam] = col_data

            new_data[in_name] = new_in_data

            new_data[in_name]['columns'] = new_valid_rule

        file_name = f'{self._optimizer_type}.json'

        with open(f'{self._file_path}/{file_name}', 'w', encoding='utf8') as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)

    @classmethod
    def __deep_update(cls, source: dict, overrides: Mapping):
        for key, value in overrides.items():
            if isinstance(value, Mapping) and value:
                returned = cls.__deep_update(source.get(key, {}), value)
                source[key] = returned
            else:
                source[key] = overrides[key]
        return source

    def update_json(self, add_data: dict) -> None:

        input_data = self.get_from_json()

        result = self.__deep_update(input_data, add_data)

        self._write_json(result)

    def update_validation_rules(self) -> None:

        valid_rules_data = self._get_valid_rules_data()

        updated_data = {input_name: {'columns': valid_ruls} for input_name, valid_ruls in valid_rules_data.items()}

        self.update_json(updated_data)

    def get_from_json(self, only_active_inputs: bool = True) -> dict:

        with open(f'{self._file_path}/{self._file_name}', 'r', encoding='utf8') as file:
            data = json.load(file)

        if only_active_inputs:

            only_active_inputs_data = {}

            for data_name, data_values in data.items():

                if data_values['active']:
                    only_active_inputs_data[data_name] = data_values

            return only_active_inputs_data

        return data

    @log_validation_rules_comparison(1)
    def validation_rules_comparison(self, validation_rules_file_dir: dict):

        valid_rules_data = self._get_valid_rules_data(*validation_rules_file_dir.values())
        inputs_data = self.get_from_json(only_active_inputs=False)

        miss_data = {}
        extra_data = {}

        make_lower_input_name = lambda name: name.lower().replace(' ', '_').replace('-', '_')

        extra_inputs = set(inputs_data.keys()).difference(map(make_lower_input_name, valid_rules_data.keys()))
        extra_data.update({input: 'no data in file' for input in extra_inputs})

        for input_name, input_data in valid_rules_data.items():

            lower_input_name = make_lower_input_name(input_name)

            if lower_input_name in inputs_data.keys():

                columns = inputs_data[lower_input_name]['columns']

                extra_columns = set(columns.keys()).difference(valid_rules_data[input_name].keys())

                if extra_columns:
                    for col in extra_columns:
                        if columns[col]['active']:
                            extra_data[lower_input_name] = {col: 'no data in file'}

                for column_name, column_data in input_data.items():

                    if column_name in columns.keys():

                        for key, value in column_data.items():

                            saved_value = columns[column_name].get(key)

                            if value != saved_value:

                                option = {key: {'file_value': value, 'saved_value': saved_value}}
                                miss_data.setdefault(lower_input_name, {}).setdefault(column_name, {}).update(option)

                    else:
                        miss_data.setdefault(lower_input_name, {}).update({column_name: 'no data'})

            else:
                miss_data[lower_input_name] = 'no data'

        if miss_data or extra_data:
            return {'miss_data': miss_data, 'extra_data': extra_data}

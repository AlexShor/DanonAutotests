import json
from copy import deepcopy
from collections.abc import Mapping

from optimizer_data.data.default_data import FileDirectory
from optimizer_data.data.input_speadsheets_data import ValidateRules, PreviewRules, Spreadsheets
from optimizer_data.operations_file_data import OperationsFileData
from optimizer_data.data.input_type_name_matches import InputTypeNameMatch


class InputData:
    def __init__(self, optimizer_type: str, file_name: str = None) -> None:
        self._file_path = FileDirectory().input_data_json
        self._optimizer_type = optimizer_type

        if file_name is None:
            self._file_name = f'{optimizer_type}.json'
        else:
            self._file_name = file_name

    def _get_valid_rules_data(self) -> dict:

        file_name = f'validation_rules_{self._optimizer_type}.xlsx'
        valid_rules = ValidateRules.get(self._optimizer_type)
        columns = valid_rules['col_names'].values()

        operation = OperationsFileData(FileDirectory().validation_rules)

        spreadsheet_params = Spreadsheets.get('tetris', 'validation_rules')[1]['params']
        rules_data = operation.read_xlsx(file_name, get_columns=columns, **spreadsheet_params)

        converted_valid_rules = operation.convert_validation_rules_data_to_dict(rules_data, valid_rules)

        return converted_valid_rules

    def _get_preview_rules_data(self) -> dict:

        file_name = f'preview_rules_{self._optimizer_type}.xlsx'
        preview_rules = PreviewRules.get(self._optimizer_type)
        columns = preview_rules['col_names'].values()

        operation = OperationsFileData(FileDirectory().preview_rules)

        spreadsheet_params = Spreadsheets.get('tetris', 'preview_rules')[1]['params']
        rules_data = operation.read_xlsx(file_name, get_columns=columns, **spreadsheet_params)

        converted_preview_rules = operation.convert_preview_rules_data_to_dict(rules_data, preview_rules)
        print('converted_preview_rules')
        return converted_preview_rules

    def test(self):

        data = deepcopy(InputTypeNameMatch.Tetris.TYPES)
        valid_rules_data = self._get_valid_rules_data()
        preview_rules_data = self._get_preview_rules_data()
        # print(data)
        # print(valid_rules_data)
        # print(preview_rules_data)

        new_data = {}

        for in_name, in_data in data.items():
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

        # print(data)

        file_name = 'tetris.json'

        with open(f'{self._file_path}/{file_name}', 'w', encoding='utf8') as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)


    def _write_json(self, write_data: dict):

        with open(f'{self._file_path}/{self._file_name}', 'w', encoding='utf8') as file:
            json.dump(write_data, file, indent=4, ensure_ascii=False)

    def create_json(self) -> None:
        pass
        # data = InputTypeNameMatch.Tetris.TYPES
        # file_name = 'tetris.json'
        #
        # with open(f'{self._file_path}/{file_name}', 'w', encoding='utf8') as file:
        #     json.dump(data, file, indent=4, ensure_ascii=False)

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


if __name__ == "__main__":

    input_data = InputData('tetris')
    # input_data.test()
    data = input_data.get_from_json()

    # new_data = {}
    #
    # for i_name, i_data in data.items():
    #     if i_name in ['calendars', 'plants', 'products', 'innovations', 'warehouses', 'materials']:
    #         new_data[i_name] = {'upload_queue': 1}
    #     elif i_name in ['material_groups']:
    #         new_data[i_name] = {'upload_queue': 2}
    #     else:
    #         new_data[i_name] = {'upload_queue': 3}
    #
    # print(new_data)
    #
    # input_data.update_json(new_data)




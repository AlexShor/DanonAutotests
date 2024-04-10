import json
from copy import deepcopy

from optimizer_data.data.default_data import FileDirectory
from optimizer_data.data.input_speadsheets_data import ValidateRules
from optimizer_data.operations_file_data import OperationsFileData
from optimizer_data.data.input_type_name_matches import InputTypeNameMatch


class InputsData:
    def __init__(self, optimizer_type: str):
        self._file_path = FileDirectory().input_data_json
        self._optimizer_type = optimizer_type

    def _get_valid_rules_data(self) -> dict:
        file_name = f'validation_rules_{self._optimizer_type}.xlsx'
        validation_rules_path = FileDirectory().validation_rules
        valid_rules = ValidateRules.get(self._optimizer_type)
        columns = valid_rules['col_names'].values()
        file_params = valid_rules['file_params']

        xlsx_data = OperationsFileData(validation_rules_path).read_xlsx(file_name, get_columns=columns, **file_params)
        valid_rules_data = OperationsFileData.convert_validation_rules_data_to_dict(xlsx_data, valid_rules)

        return valid_rules_data

    def test(self):
        data = InputTypeNameMatch.Tetris.TYPES
        valid_rules_data = self._get_valid_rules_data()
        # print(data)
        # print(valid_rules_data)

        for in_name, in_data in deepcopy(data).items():
            system_file_name = in_data['system_file_name']
            valid_rule = valid_rules_data[system_file_name]
            new_valid_rule = {}
            for col_nam, col_data in valid_rule.items():
                col_data['data_type'] = col_data['data_type'].__name__
                new_valid_rule[col_nam] = col_data

            data[in_name]['columns'] = new_valid_rule

        print(data)

        file_name = 'tetris.json'

        with open(f'{self._file_path}/{file_name}', 'w', encoding='utf8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


    def create_json(self, optimizer_type: str):
        data = InputTypeNameMatch.Tetris.TYPES
        file_name = 'tetris.json'

        with open(f'{self._file_path}/{file_name}', 'w', encoding='utf8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def update_json(self):
        pass

    def get_from_json(self, file_name: str = None) -> dict:
        if file_name is None:
            file_name = f'{self._optimizer_type}.json'

        with open(f'{self._file_path}/{file_name}', 'r', encoding='utf8') as file:
            data = json.load(file)

        return data







if __name__ == "__main__":

    input_data = InputsData('tetris')
    input_data.test()




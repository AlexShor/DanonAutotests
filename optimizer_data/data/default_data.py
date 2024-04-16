from datetime import date, time
import os


class DefaultDataFill:
    @staticmethod
    def get(data_type, validity=True):
        types = {
            True: {
                str: 'string',
                float: '111.45',
                int: '222',
                bool: '1|TRUE:0|FALSE',
                date: '01-01-2024',
                time: '9:45:00 AM',
            },
            False: {
                str: '555',
                float: 'float',
                int: 'int',
                bool: '888',
                date: 'date',
                time: 'time',
            }
        }

        return types.get(validity).get(data_type)


class ErrorLogText:

    __log_text = {
        'rus': {
            'obligation': 'Ошибки касающийся обязательных полей:',
            'type': 'Ошибки по типам полей:',
            'negative': 'Ошибки по неотрицательным значениям:',
            'row': 'строка',
            'col': 'колонка'
        },
        'eng': {
            'obligation': 'Errors regarding obligatory fields:',
            'type': 'Type errors:',
            'negative': 'Errors with non-negative values:',
            'row': 'row',
            'col': 'column'
        }
    }

    def get(self, language: str):
        return self.__log_text[language]


class FileDirectory:

    __ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    __ROOT_DIRECTORY = '/'.join(__ABSOLUTE_PATH.split('\\')[:-2])

    def __init__(self, optimizer_type: str = None):
        if optimizer_type:
            self._optimizer_type = '/' + optimizer_type
        else:
            self._optimizer_type = ''

        self.input_data_json = f'{self.__ROOT_DIRECTORY}/optimizer_data/data/input_data_json'

        self.validation_rules = f'{self.__ROOT_DIRECTORY}/optimizer_data/files/rules/validation_rules'
        self.preview_rules = f'{self.__ROOT_DIRECTORY}/optimizer_data/files/rules/preview_rules'

        __input = f'{self.__ROOT_DIRECTORY}/optimizer_data/files/input/{self._optimizer_type}'

        self.downloaded_input_files = f'{__input}/downloaded_input_files'
        self.valid_input_files = f'{__input}/valid_input_files/files'
        self.invalid_input_files = f'{__input}/invalid_input_files/files'
        self.input_files_error_logs = f'{__input}/invalid_input_files/error_logs'

        __output = f'{self.__ROOT_DIRECTORY}/optimizer_data/files/output/{self._optimizer_type}'


if __name__ == "__main__":
    pass

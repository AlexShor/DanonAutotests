from datetime import date
import os


class DefaultDataFill:
    @staticmethod
    def get(data_type, validity=True):
        types = {
            True: {
                str: 'string',
                date: '01-01-2023',
                float: '111.45',
                int: '222',
                bool: '1|TRUE:0|FALSE'
            },
            False: {
                str: '555',
                date: 'date',
                float: 'float',
                int: 'int',
                bool: '888'
            }
        }

        return types.get(validity).get(data_type)


class ErrorLogText:
    @staticmethod
    def get(language: str = 'eng'):

        log_text = {
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

        return log_text[language]


class FileDirectory:
    __ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    __ROOT_DIRECTORY = '/'.join(__ABSOLUTE_PATH.split('\\')[:-2])

    def __init__(self, optimizer_type: str = None):
        if optimizer_type:
            self._optimizer_type = '/' + optimizer_type
        else:
            self._optimizer_type = ''

        self.input_data_json = f'{self.__ROOT_DIRECTORY}/optimizer_data/data/input_data_json'
        self.validation_rules = f'{self.__ROOT_DIRECTORY}/optimizer_data/files/validation_rules'
        self.input_files = f'{self.__ROOT_DIRECTORY}/optimizer_data/files{self._optimizer_type}/input_files'
        self.invalid_input_files = f'{self.__ROOT_DIRECTORY}/optimizer_data/files{self._optimizer_type}/invalid_input_files/files'
        self.input_files_error_logs = f'{self.__ROOT_DIRECTORY}/optimizer_data/files{self._optimizer_type}/invalid_input_files/error_logs'


if __name__ == "__main__":
    path = FileDirectory('tetris')


    print(path.validation_rules)
    print(path.input_files)
    print(path.invalid_input_files)
    print(path.input_files_error_logs)







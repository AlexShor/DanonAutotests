class ConsoleColors:
    @staticmethod
    def txt_red(text):
        return f'\033[31m{text}\033[0m'

    @staticmethod
    def txt_grn(text):
        return f'\033[32m{text}\033[0m'

    @staticmethod
    def txt_yel(text):
        return f'\033[33m{text}\033[0m'

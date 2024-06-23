class ConsoleColors:
    @staticmethod
    def txt_red(text: str) -> str:
        return f'\033[31m{text}\033[0m'

    @staticmethod
    def txt_grn(text: str) -> str:
        return f'\033[32m{text}\033[0m'

    @staticmethod
    def txt_yel(text: str) -> str:
        return f'\033[33m{text}\033[0m'

    @staticmethod
    def txt_blu(text: str) -> str:
        return f'\033[34m{text}\033[0m'

    @staticmethod
    def txt_vio(text: str) -> str:
        return f'\033[35m{text}\033[0m'

    @staticmethod
    def txt_cyn(text: str) -> str:
        return f'\033[36m{text}\033[0m'

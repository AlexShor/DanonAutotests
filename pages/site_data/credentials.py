import os

from dotenv import load_dotenv


class Credentials:
    @staticmethod
    def auth(env='DEV'):
        load_dotenv()
        email = os.getenv(f'{env}_EMAIL')
        password = os.getenv(f'{env}_PASSWORD')
        return {'email': email, 'password': password}

import os

from dotenv import load_dotenv


class Credentials:
    @staticmethod
    def auth():
        load_dotenv()
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')
        return {'email': email, 'password': password}

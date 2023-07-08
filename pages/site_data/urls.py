class BaseUrls:
    DEV = 'https://app.danon.digital-spectr.ru'


class Paths:
    CATALOGUE = 'catalogue'
    ACCOUNTS = 'accounts'


class Pages:
    LOGIN = 'login'


class Links(BaseUrls, Paths):
    LOGIN_PAGE = f'{BaseUrls.DEV}/{Pages.LOGIN}/'


class QueryParams:
    PROMO = 'promo'

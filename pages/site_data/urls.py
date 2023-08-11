from .default_params import ProjectType as Ptype


class BaseUrls:
    BASE_URLS = {'DEV': 'https://app.danon.digital-spectr.ru',
                 'STAGE': 'https://app.danon-stage.jumeforecast.com',
                 'PROD': 'https://danone.jumeplatform.com'}
    BASE_URLS_BACK = {'DEV': 'https://back.danon.digital-spectr.ru',
                      'STAGE': 'https://back.danon-stage.jumeforecast.com',
                      'PROD': 'https://back.danon.jumeforecast.com'}


class Paths:
    SCENARIO_PAGE = 'promo-optimizer/promo-scenario'


class Pages:
    LOGIN = 'login'
    SCENARIO_LIST = {Ptype.PROMO: 'promo-optimizer',
                     Ptype.RTM: 'rtm-optimizer',
                     Ptype.TETRIS: 'tetris-optimizer',
                     Ptype.CFR: 'cfr-optimizer'}

    CREATE_SCENARIO = {Ptype.PROMO: 'create-promo-scenario',
                       Ptype.RTM: 'create-rtm-scenario',
                       Ptype.TETRIS: 'create-tetris-scenario',
                       Ptype.CFR: 'create-cfr-scenario'}


class Links(BaseUrls, Paths):
    def __init__(self, environment):
        self.environment = environment

    def get(self, link, scenario_id=''):
        base_url = BaseUrls.BASE_URLS.get(self.environment)
        links = {'LOGIN_PAGE': f'{base_url}/{Pages.LOGIN}',
                 'SCENARIO_LIST_PAGE': f'{base_url}/{Pages.SCENARIO_LIST["promo"]}',
                 'CREATE_SCENARIO_PAGE': f'{base_url}/{Pages.CREATE_SCENARIO["promo"]}',
                 'SCENARIO_PAGE': f'{base_url}/{Paths.SCENARIO_PAGE}/{scenario_id}'}
        return links.get(link)


class QueryParams:
    PROMO = 'promo'

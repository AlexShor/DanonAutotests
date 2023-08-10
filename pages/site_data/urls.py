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
    PROMO_SCENARIO_LIST = 'promo-optimizer'
    RTM_SCENARIO_LIST = 'rtm-optimizer'
    TETRIS_SCENARIO_LIST = 'tetris-optimizer'
    CFR_SCENARIO_LIST = 'cfr-optimizer'

    PROMO_CREATE_SCENARIO = 'create-promo-scenario'
    RTM_CREATE_SCENARIO = 'create-rtm-scenario'
    TETRIS_CREATE_SCENARIO = 'create-tetris-scenario'
    CFR_CREATE_SCENARIO = 'create-cfr-scenario'


class Links(BaseUrls, Paths):
    def __init__(self, environment):
        self.environment = environment

    def get(self, link, scenario_id=''):
        base_url = BaseUrls.BASE_URLS.get(self.environment)
        links = {'LOGIN_PAGE': f'{base_url}/{Pages.LOGIN}',
                 'SCENARIO_LIST_PAGE': f'{base_url}/{Pages.PROMO_SCENARIO_LIST}',
                 'CREATE_SCENARIO_PAGE': f'{base_url}/{Pages.PROMO_CREATE_SCENARIO}',
                 'SCENARIO_PAGE': f'{base_url}/{Paths.SCENARIO_PAGE}/{scenario_id}'}
        return links.get(link)


class QueryParams:
    PROMO = 'promo'

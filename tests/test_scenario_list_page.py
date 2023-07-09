from ..pages.scenario_list_page import ScenarioListPage
from ..pages.site_data.urls import Links


def test_user_authorization(env, browser, authoriz_creds):

    link = Links(env).get('SCENARIO_LIST_PAGE')
    scenario_list_page = ScenarioListPage(browser, env, link)
    scenario_list_page.should_be_scenario_list_page()

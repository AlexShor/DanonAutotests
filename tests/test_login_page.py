import time

from ..pages.login_page import LoginPage
from ..pages.site_data.urls import Links


def test_user_authorization(browser, authoriz_creds):
    link = Links.LOGIN_PAGE
    page = LoginPage(browser, link)
    page.open()
    page.authorize_user(*authoriz_creds.values())


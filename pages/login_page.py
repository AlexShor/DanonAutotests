from .base_page import BasePage
from .site_data.locators import LoginPageLocators as LPLocator
from .site_data.locators import BasePageLocators as BPLocator


class LoginPage(BasePage):
    def authorize_user(self, email, password):
        self.find_elem(*BPLocator.JB_BUTTON).click()
        self.find_elem(*LPLocator.INPUT_EMAIL).send_keys(email)
        self.find_elem(*LPLocator.INPUT_PASSWORD).send_keys(password)
        self.find_elem(*BPLocator.JB_SMALL).click()

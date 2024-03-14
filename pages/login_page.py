from pages.base_page import BasePage
from pages.site_data.locators import LoginPageLocators as LPLocator
from pages.site_data.locators import BasePageLocators as BPLocator


class LoginPage(BasePage):
    def authorize_user(self, email, password):
        self.find_elem(*BPLocator.JB_BUTTON).click()
        # self.find_elem(*LPLocator.INPUT_EMAIL).send_keys(email)
        self.is_clickable(*LPLocator.INPUT_EMAIL).send_keys(email)
        self.find_elem(*LPLocator.INPUT_PASSWORD).send_keys(password)
        self.find_elem(*BPLocator.JB_SMALL).click()

from .base_page import BasePage
from .site_data.locators import LoginPageLocators as LPLocator


class LoginPage(BasePage):
    def authorize_user(self, email, password):
        self.browser.find_element(*LPLocator.JB_BUTTON).find_element(*LPLocator.JENIUS_BUTTON).click()
        self.browser.find_element(*LPLocator.INPUT_EMAIL).send_keys(email)
        self.browser.find_element(*LPLocator.INPUT_PASSWORD).send_keys(password)
        self.browser.find_element(*LPLocator.JB_SMALL).find_element(*LPLocator.JENIUS_BUTTON).click()

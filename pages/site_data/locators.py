from selenium.webdriver.common.by import By


class BasePageLocators:
    HTML = (By.TAG_NAME, 'html')
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")
    VIEW_BASKET_BUTTON = (By.CSS_SELECTOR, ".basket-mini a.btn")
    ACTIVE_BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb .active")
    USER_ICON = (By.CSS_SELECTOR, ".icon-user")


class LoginPageLocators:
    JENIUS_BUTTON = (By.XPATH, '//button[contains(@class, "_circleCont_")]')
    JB_BUTTON = (By.XPATH, '//div[contains(@class, "_button_")]')
    JB_SMALL = (By.XPATH, '//div[contains(@class, "_small_")]')
    JB_LEFT = (By.XPATH, '//div[contains(@class, "_bottomLeft_") and contains(@class, "_scaleInMax_")]')
    JB_BOTTOM = (By.XPATH, '//div[contains(@class, "_bottom_")]')
    POPOVER = (By.XPATH, '//div[contains(@class, "_popover_")]')
    INPUT_EMAIL = (By.XPATH, '//input[@type="email"]')
    INPUT_PASSWORD = (By.XPATH, '//input[@type="password"]')
    CHECKBOX_REMEMBER_ME = (By.XPATH, '//div[contains(@class, "_rememberMe_")]')
    FORGOT_PASS_BUTTON = (By.XPATH, '//div[contains(@class, "_forgot_")]/span')
    PASSWORD_EYE = (By.XPATH, '//div[contains(@class, "_noMultiline_")]/..//div[contains(@class, "_icon_")]')

# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Сторінка авторизації"""
    
    # Локатори
    EMAIL_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'Login')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.css-1iyoj2o .error, [data-testid="error-message"]')
    
    def enter_email(self, email):
        """Ввести email"""
        self.input_text(*self.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        """Ввести пароль"""
        self.input_text(*self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """Клікнути кнопку входу"""
        self.click_element(*self.LOGIN_BUTTON)
    
    def has_error(self):
        """Перевірити наявність помилки"""
        return self.element_exists(*self.ERROR_MESSAGE, timeout=2)
    
    def login(self, email, password):
        """Виконати повну авторизацію"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from .base_page import BasePage


class MainPage(BasePage):
    """Головна сторінка OLX"""
    
    # Локатори
    PROFILE_BUTTON_SELECTORS = [
        (By.CSS_SELECTOR, 'a[data-cy="myolx-link"]'),
        (By.CSS_SELECTOR, 'a[data-testid="myolx-link"]'),
        (By.XPATH, '//a[contains(@href, "account") and contains(., "профіль")]'),
        (By.XPATH, '//a[contains(text(), "Ваш профіль")]')
    ]
    SEARCH_INPUT = (By.ID, 'search')
    LOCATION_INPUT = (By.ID, 'location-input')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'button[name="searchBtn"]')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = 'https://www.olx.ua/uk'
    
    def open(self):
        """Відкрити головну сторінку"""
        self.driver.get(self.url)
        time.sleep(1.5)
    
    def click_profile_button(self):
        """Клікнути на кнопку профілю"""
        for selector in self.PROFILE_BUTTON_SELECTORS:
            try:
                self.click_element(*selector)
                return
            except (TimeoutException, NoSuchElementException):
                continue
        raise Exception("Не вдалося знайти кнопку 'Ваш профіль'")
    
    def enter_search_query(self, query):
        """Ввести пошуковий запит"""
        self.input_text(*self.SEARCH_INPUT, query)
    
    def enter_location(self, location):
        """Ввести локацію"""
        location_input = self.find_element(*self.LOCATION_INPUT)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_input)
        time.sleep(0.2)
        location_input.clear()
        location_input.send_keys(location)
        time.sleep(1)
    
    def click_search(self):
        """Клікнути кнопку пошуку"""
        self.click_element(*self.SEARCH_BUTTON)

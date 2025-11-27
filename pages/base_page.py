# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time


class BasePage:
    """Базовий клас для всіх сторінок з загальними методами"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, by, value, timeout=10):
        """Знайти елемент на сторінці з очікуванням"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def find_clickable_element(self, by, value, timeout=10):
        """Знайти клікабельний елемент"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def click_element(self, by, value, timeout=10):
        """Клікнути на елемент з обробкою помилок"""
        try:
            element = self.find_clickable_element(by, value, timeout)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            element.click()
            time.sleep(0.5)
        except ElementClickInterceptedException:
            element = self.find_element(by, value, timeout)
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.5)
    
    def input_text(self, by, value, text, timeout=10):
        """Ввести текст в поле"""
        element = self.find_element(by, value, timeout)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)
        element.clear()
        element.send_keys(text)
        time.sleep(0.3)
    
    def wait_for_url_contains(self, url_part, timeout=10):
        """Очікувати поки URL міститиме певну частину"""
        WebDriverWait(self.driver, timeout).until(EC.url_contains(url_part))
        time.sleep(0.5)
    
    def element_exists(self, by, value, timeout=3):
        """Перевірити чи елемент існує на сторінці"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False
    
    def get_current_url(self):
        """Отримати поточний URL"""
        return self.driver.current_url

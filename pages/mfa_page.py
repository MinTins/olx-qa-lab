# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from .base_page import BasePage


class MFAPage(BasePage):
    """Сторінка двофакторної автентифікації"""
    
    # Локатори
    EMAIL_OPTION_SELECTORS = [
        (By.XPATH, '//div[@role="radio" and contains(@aria-label, "Email")]'),
        (By.XPATH, '//div[@role="radio" and contains(., "Email")]'),
        (By.XPATH, '//div[contains(@class, "css-v4f662") and contains(., "Email")]')
    ]
    CONFIRM_BUTTON_SELECTORS = [
        (By.XPATH, '//button[@type="submit" and contains(., "Підтвердити")]'),
        (By.XPATH, '//button[contains(text(), "Підтвердити")]'),
        (By.CSS_SELECTOR, 'button[type="submit"]')
    ]
    
    def is_mfa_page(self):
        """Перевірити чи це сторінка 2FA"""
        for selector in self.EMAIL_OPTION_SELECTORS:
            if self.element_exists(*selector, timeout=2):
                return True
        return False
    
    def select_email_option(self):
        """Вибрати опцію Email для 2FA"""
        for selector in self.EMAIL_OPTION_SELECTORS:
            try:
                email_option = self.find_element(*selector, timeout=3)
                if email_option.get_attribute('aria-checked') != 'true':
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_option)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", email_option)
                    time.sleep(0.3)
                return True
            except (TimeoutException, NoSuchElementException):
                continue
        return False
    
    def click_confirm(self):
        """Клікнути кнопку підтвердження"""
        for selector in self.CONFIRM_BUTTON_SELECTORS:
            try:
                self.click_element(*selector, timeout=3)
                return True
            except (TimeoutException, NoSuchElementException):
                continue
        return False
    
    def wait_for_user_mfa_input(self):
        """Очікувати введення коду користувачем"""
        print("\n" + "="*60)
        print("ОЧІКУВАННЯ: Введіть код з пошти на сайті та натисніть 'Увійти'")
        print("="*60)
        input("Натисніть Enter після введення коду...")
        time.sleep(1)

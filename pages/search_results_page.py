# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from .base_page import BasePage


class SearchResultsPage(BasePage):
    """Сторінка результатів пошуку"""
    
    # Локатори
    FIRST_AD_LINK = (By.CSS_SELECTOR, 'div[data-cy="l-card"]:first-child a.css-1tqlkj0')
    AD_CARD_BY_INDEX = '//div[@data-cy="l-card"][{}]//a[contains(@class, "css-")]'
    TOTAL_COUNT = (By.CSS_SELECTOR, 'span[data-testid="total-count"]')
    TOTAL_COUNT_ALT = (By.XPATH, "//span[contains(text(), 'знайшли') or contains(text(), 'оголошень')]")
    AD_CARDS = (By.CSS_SELECTOR, 'div[data-cy="l-card"]')
    CATEGORY_DROPDOWN = (By.CSS_SELECTOR, 'button[data-testid="category-dropdown"]')
    ELECTRONICS_BUTTON = (By.XPATH, '//button[@data-categoryid="37" and @role="menuitem"]')
    PHONES_BUTTON = (By.XPATH, '//button[@data-categoryid="44" and @role="menuitem"]')
    COOKIES_OVERLAY = (By.CSS_SELECTOR, '[data-testid="cookies-overlay__container"]')
    ACCEPT_COOKIES = (By.CSS_SELECTOR, '[data-testid="accept-consent"]')
    
    def click_ad_by_index(self, index=1):
        """Клікнути на оголошення за індексом"""
        xpath = self.AD_CARD_BY_INDEX.format(index)
        self.click_element(By.XPATH, xpath)
    
    def get_total_count(self):
        """Отримати загальну кількість результатів"""
        total_count_text = "Не вдалося отримати кількість"
        
        try:
            wait = WebDriverWait(self.driver, 10)
            total_count_element = wait.until(
                EC.presence_of_element_located(self.TOTAL_COUNT)
            )
            total_count_text = total_count_element.text
        except TimeoutException:
            try:
                total_count_element = self.driver.find_element(*self.TOTAL_COUNT_ALT)
                total_count_text = total_count_element.text
            except:
                ad_cards = self.driver.find_elements(*self.AD_CARDS)
                if len(ad_cards) > 0:
                    total_count_text = f"Знайдено {len(ad_cards)}+ оголошень на сторінці"
        
        return total_count_text
    
    def close_cookies_popup(self):
        """Закрити спливаюче вікно про cookies"""
        try:
            cookies_overlay = self.driver.find_elements(*self.COOKIES_OVERLAY)
            if cookies_overlay:
                accept_button = self.driver.find_element(*self.ACCEPT_COOKIES)
                accept_button.click()
                time.sleep(0.5)
        except:
            pass
    
    def apply_phone_category(self):
        """Застосувати категорію Телефони"""
        try:
            category_dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CATEGORY_DROPDOWN)
            )
            
            current_category_text = category_dropdown.text.strip()
            
            # Перевірка чи категорія вже застосована
            if 'Телефони' in current_category_text or 'телефони' in current_category_text.lower():
                print(f"ℹ Категорія вже застосована: {current_category_text}")
                return True
            
            # Відкрити випадаюче меню
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_dropdown)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", category_dropdown)
            time.sleep(1.2)
            
            # Вибрати Електроніка
            electronics_button = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(self.ELECTRONICS_BUTTON)
            )
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", electronics_button)
            time.sleep(1)
            
            # Вибрати Телефони
            phones_button = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(self.PHONES_BUTTON)
            )
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", phones_button)
            time.sleep(2)
            
            return True
            
        except TimeoutException:
            return False
    
    def has_category_in_url(self):
        """Перевірити наявність категорії в URL"""
        current_url = self.get_current_url()
        return 'telefony' in current_url.lower() or 'elektronika' in current_url.lower()

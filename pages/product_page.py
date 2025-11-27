# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    """Сторінка товару"""
    
    # Локатори
    SELLER_NAME = (By.CSS_SELECTOR, 'h4[data-testid="user-profile-user-name"]')
    SELLER_RATING = (By.CSS_SELECTOR, 'div[data-testid="score-widget-empty"] p, div[data-testid="user-score-widget"]')
    MEMBER_SINCE = (By.CSS_SELECTOR, 'p[data-testid="member-since"]')
    LAST_SEEN = (By.CSS_SELECTOR, 'p[data-testid="lastSeenBox"]')
    
    def get_seller_info(self):
        """Отримати інформацію про продавця"""
        try:
            seller_info = {}
            
            # Отримати ім'я продавця
            try:
                seller_info['name'] = self.find_element(*self.SELLER_NAME, timeout=5).text
            except:
                seller_info['name'] = "Не знайдено"
            
            # Отримати рейтинг
            try:
                rating_element = self.find_element(*self.SELLER_RATING, timeout=3)
                seller_info['rating'] = rating_element.text
            except:
                seller_info['rating'] = "Не знайдено"
            
            # Отримати дату реєстрації
            try:
                member_since = self.find_element(*self.MEMBER_SINCE, timeout=3).text
                seller_info['member_since'] = member_since
            except:
                seller_info['member_since'] = "Не знайдено"
            
            # Отримати останній візит
            try:
                last_seen = self.find_element(*self.LAST_SEEN, timeout=3).text
                seller_info['last_seen'] = last_seen
            except:
                seller_info['last_seen'] = "Не знайдено"
            
            return seller_info
        except Exception as e:
            return {'error': str(e)}
    
    def print_seller_info(self, seller_info):
        """Вивести інформацію про продавця"""
        if 'error' not in seller_info:
            print("\n" + "─"*60)
            print("ІНФОРМАЦІЯ ПРО ПРОДАВЦЯ:")
            print("─"*60)
            print(f"Ім'я: {seller_info.get('name', 'Н/Д')}")
            print(f"Рейтинг: {seller_info.get('rating', 'Н/Д')}")
            print(f"На OLX з: {seller_info.get('member_since', 'Н/Д')}")
            print(f"Останній візит: {seller_info.get('last_seen', 'Н/Д')}")
            print("─"*60 + "\n")
    
    def is_product_page(self):
        """Перевірити чи це сторінка товару"""
        return '/d/uk/obyavlenie/' in self.get_current_url()

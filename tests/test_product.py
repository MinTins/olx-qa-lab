# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

import time
from pages import SearchResultsPage, ProductPage
from .base_test import BaseTest


class ProductTests(BaseTest):
    """Тести для роботи з товарами"""
    
    def test_product_card_and_seller_info(self):
        """Тест-кейс 5: Відкриття картки товару та отримання даних продавця"""
        self.print_test_header(5, "Відкриття картки товару та отримання даних продавця")
        
        search_results = SearchResultsPage(self.driver)
        product_page = ProductPage(self.driver)
        
        try:
            # Клікнути на оголошення
            search_results.click_ad_by_index(6)
            time.sleep(1.5)
            
            # Перевірка що відкрилась сторінка товару
            if product_page.is_product_page():
                # Отримати дані продавця
                seller_info = product_page.get_seller_info()
                
                if 'error' not in seller_info:
                    # Вивести інформацію
                    product_page.print_seller_info(seller_info)
                    
                    self.logger.log_test_result(
                        "Відкриття картки товару та отримання даних", 
                        True, 
                        f"Продавець: {seller_info.get('name')}"
                    )
                else:
                    self.logger.log_test_result(
                        "Відкриття картки товару та отримання даних", 
                        False, 
                        f"Помилка отримання даних: {seller_info['error']}"
                    )
            else:
                self.logger.log_test_result(
                    "Відкриття картки товару та отримання даних", 
                    False, 
                    f"Не вдалося відкрити картку товару: {self.driver.current_url}"
                )
            
        except Exception as e:
            self.logger.log_test_result(
                "Відкриття картки товару та отримання даних", 
                False, 
                str(e)
            )

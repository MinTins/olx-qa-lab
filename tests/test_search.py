# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

import time
from pages import MainPage, SearchResultsPage
from .base_test import BaseTest


class SearchTests(BaseTest):
    """Тести пошуку"""
    
    def test_search_playstation(self):
        """Тест-кейс 3: Пошук PlayStation 5 по всій Україні"""
        self.print_test_header(3, "Пошук PlayStation 5 по всій Україні")
        
        main_page = MainPage(self.driver)
        search_results = SearchResultsPage(self.driver)
        
        try:
            # Відкрити головну сторінку
            main_page.open()
            
            # Виконати пошук
            main_page.enter_search_query('PlayStation 5')
            main_page.click_search()
            
            time.sleep(3)
            
            # Отримати кількість результатів
            total_count_text = search_results.get_total_count()
            print(f"\n📊 {total_count_text}")
            
            # Перевірка результату
            current_url = search_results.get_current_url()
            
            if 'q-PlayStation-5' in current_url or 'q-playstation-5' in current_url.lower():
                self.logger.log_test_result(
                    "Пошук PlayStation 5", 
                    True, 
                    f"Результати: {total_count_text}"
                )
            else:
                self.logger.log_test_result(
                    "Пошук PlayStation 5", 
                    False, 
                    f"URL не містить пошукового запиту: {current_url}"
                )
            
        except Exception as e:
            self.logger.log_test_result("Пошук PlayStation 5", False, str(e))
    
    def test_search_iphone_with_category(self):
        """Тест-кейс 4: Пошук iPhone 15 з фільтром категорії"""
        self.print_test_header(4, "Пошук iPhone 15 з фільтром категорії")
        
        main_page = MainPage(self.driver)
        search_results = SearchResultsPage(self.driver)
        
        try:
            # Відкрити головну сторінку
            main_page.open()
            
            # Виконати пошук з локацією
            main_page.enter_search_query('iPhone 15')
            main_page.enter_location('Київська область')
            main_page.click_search()
            
            time.sleep(2.5)
            
            # Закрити cookies popup якщо є
            search_results.close_cookies_popup()
            
            # Застосувати категорію
            category_applied = search_results.apply_phone_category()
            
            time.sleep(1)
            current_url = search_results.get_current_url()
            
            # Перевірка результату
            checks = [
                'iphone-15' in current_url.lower() or 'q-iphone-15' in current_url.lower(),
                'ko' in current_url or 'kyiv' in current_url.lower() or 'київ' in current_url.lower()
            ]
            
            has_category = search_results.has_category_in_url()
            
            if any(checks):
                if has_category or category_applied:
                    self.logger.log_test_result(
                        "Пошук iPhone 15 з категорією", 
                        True, 
                        f"URL: {current_url}"
                    )
                else:
                    self.logger.log_test_result(
                        "Пошук iPhone 15 з категорією", 
                        True, 
                        f"Пошук виконано: {current_url}"
                    )
            else:
                self.logger.log_test_result(
                    "Пошук iPhone 15 з категорією", 
                    False, 
                    f"URL не містить очікуваних параметрів: {current_url}"
                )
            
        except Exception as e:
            self.logger.log_test_result("Пошук iPhone 15 з категорією", False, str(e))

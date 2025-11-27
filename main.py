# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

import time
from tests import LoginTests, SearchTests, ProductTests


class OLXTestRunner:
    """Клас для запуску всіх тестів OLX"""
    
    def __init__(self):
        self.login_tests = None
        self.search_tests = None
        self.product_tests = None
    
    def run_login_tests(self):
        """Запустити тести авторизації"""
        print("\n" + "="*60)
        print("РОЗДІЛ: ТЕСТИ АВТОРИЗАЦІЇ")
        print("="*60)
        
        self.login_tests = LoginTests()
        
        try:
            self.login_tests.test_invalid_login()
            time.sleep(1)
            
            self.login_tests.test_valid_login()
            time.sleep(1)
        finally:
            self.login_tests.teardown()
    
    def run_search_tests(self):
        """Запустити тести пошуку"""
        print("\n" + "="*60)
        print("РОЗДІЛ: ТЕСТИ ПОШУКУ")
        print("="*60)
        
        self.search_tests = SearchTests()
        
        try:
            self.search_tests.test_search_playstation()
            time.sleep(1)
            
            self.search_tests.test_search_iphone_with_category()
            time.sleep(1)
        finally:
            # Не закриваємо драйвер, бо потрібен для тестів товарів
            pass
    
    def run_product_tests(self):
        """Запустити тести товарів (використовує драйвер після пошуку)"""
        print("\n" + "="*60)
        print("РОЗДІЛ: ТЕСТИ ТОВАРІВ")
        print("="*60)
        
        if self.search_tests:
            # Використовуємо існуючий драйвер з тестів пошуку
            self.product_tests = ProductTests()
            self.product_tests.driver = self.search_tests.driver
            self.product_tests.logger = self.search_tests.logger
            
            try:
                self.product_tests.test_product_card_and_seller_info()
            finally:
                self.product_tests.teardown()
    
    def print_final_summary(self):
        """Вивести фінальний підсумок всіх тестів"""
        all_results = []
        
        if self.login_tests:
            all_results.extend(self.login_tests.logger.get_test_results())
        
        if self.search_tests:
            all_results.extend(self.search_tests.logger.get_test_results())
        
        print("\n" + "="*60)
        print("ФІНАЛЬНИЙ ПІДСУМОК ТЕСТУВАННЯ")
        print("="*60)
        
        total = len(all_results)
        passed = sum(1 for r in all_results if r['passed'])
        failed = total - passed
        
        print(f"Всього тестів: {total}")
        print(f"✓ Пройдено: {passed}")
        print(f"✗ Не пройдено: {failed}")
        print(f"Успішність: {(passed/total*100):.1f}%")
        print("="*60 + "\n")
        
        if failed > 0:
            print("Деталі непройдених тестів:")
            for result in all_results:
                if not result['passed']:
                    print(f"  • {result['test']}: {result['message']}")
            print()
    
    def run_all_tests(self):
        """Запустити всі тести"""
        try:
            print("\n" + "🚀 " + "="*56)
            print("ЗАПУСК АВТОМАТИЗОВАНОГО ТЕСТУВАННЯ OLX")
            print("="*60 + "\n")
            
            # Запуск тестів авторизації
            self.run_login_tests()
            
            # Запуск тестів пошуку
            self.run_search_tests()
            
            # Запуск тестів товарів
            self.run_product_tests()
            
            # Вивести фінальний підсумок
            self.print_final_summary()
            
        except Exception as e:
            print(f"\n❌ Критична помилка: {str(e)}")
        
        print("\n✅ Тестування завершено!")


if __name__ == '__main__':
    runner = OLXTestRunner()
    runner.run_all_tests()

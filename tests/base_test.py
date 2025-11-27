# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

import time
from utils import DriverFactory, TestLogger


class BaseTest:
    """Базовий клас для всіх тестів"""
    
    def __init__(self):
        self.driver = None
        self.logger = TestLogger()
        self.setup()
    
    def setup(self):
        """Налаштування перед тестами"""
        self.driver = DriverFactory.create_chrome_driver()
    
    def teardown(self):
        """Очищення після тестів"""
        if self.driver:
            print("\nЗакриття браузера через 3 секунди...")
            time.sleep(3)
            self.driver.quit()
    
    def print_test_header(self, test_case_number, test_name):
        """Вивести заголовок тесту"""
        print("\n" + "="*60)
        print(f"ТЕСТ-КЕЙС {test_case_number}: {test_name}")
        print("="*60)

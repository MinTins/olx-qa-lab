# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

"""
Файл для запуску окремих тестів або групи тестів
"""

import sys
import time
from tests import LoginTests, SearchTests, ProductTests


def print_menu():
    """Вивести меню вибору тестів"""
    print("\n" + "="*60)
    print("OLX TEST AUTOMATION - ВИБІР ТЕСТІВ")
    print("="*60)
    print("1. Всі тести")
    print("2. Тільки тести авторизації")
    print("3. Тільки тести пошуку")
    print("4. Тести пошуку + тест товару")
    print("5. Тест: Невалідна авторизація")
    print("6. Тест: Валідна авторизація")
    print("7. Тест: Пошук PlayStation 5")
    print("8. Тест: Пошук iPhone 15 з категорією")
    print("0. Вихід")
    print("="*60)


def run_all_tests():
    """Запустити всі тести"""
    print("\n🚀 Запуск всіх тестів...\n")
    from main import OLXTestRunner
    runner = OLXTestRunner()
    runner.run_all_tests()


def run_login_tests():
    """Запустити тести авторизації"""
    print("\n🔐 Запуск тестів авторизації...\n")
    tests = LoginTests()
    try:
        tests.test_invalid_login()
        time.sleep(1)
        tests.test_valid_login()
        tests.logger.print_test_summary()
    finally:
        tests.teardown()


def run_search_tests():
    """Запустити тести пошуку"""
    print("\n🔍 Запуск тестів пошуку...\n")
    tests = SearchTests()
    try:
        tests.test_search_playstation()
        time.sleep(1)
        tests.test_search_iphone_with_category()
        tests.logger.print_test_summary()
    finally:
        tests.teardown()


def run_search_and_product_tests():
    """Запустити тести пошуку та товарів"""
    print("\n🔍 Запуск тестів пошуку та товарів...\n")
    search_tests = SearchTests()
    try:
        search_tests.test_search_playstation()
        time.sleep(1)
        search_tests.test_search_iphone_with_category()
        time.sleep(1)
        
        # Запуск тесту товару на тому ж драйвері
        product_tests = ProductTests()
        product_tests.driver = search_tests.driver
        product_tests.logger = search_tests.logger
        
        product_tests.test_product_card_and_seller_info()
        search_tests.logger.print_test_summary()
    finally:
        search_tests.teardown()


def run_invalid_login_test():
    """Запустити тест невалідної авторизації"""
    print("\n❌ Запуск тесту невалідної авторизації...\n")
    tests = LoginTests()
    try:
        tests.test_invalid_login()
        tests.logger.print_test_summary()
    finally:
        tests.teardown()


def run_valid_login_test():
    """Запустити тест валідної авторизації"""
    print("\n✅ Запуск тесту валідної авторизації...\n")
    tests = LoginTests()
    try:
        tests.test_valid_login()
        tests.logger.print_test_summary()
    finally:
        tests.teardown()


def run_playstation_search_test():
    """Запустити тест пошуку PlayStation"""
    print("\n🎮 Запуск тесту пошуку PlayStation 5...\n")
    tests = SearchTests()
    try:
        tests.test_search_playstation()
        tests.logger.print_test_summary()
    finally:
        tests.teardown()


def run_iphone_search_test():
    """Запустити тест пошуку iPhone"""
    print("\n📱 Запуск тесту пошуку iPhone 15...\n")
    tests = SearchTests()
    try:
        tests.test_search_iphone_with_category()
        tests.logger.print_test_summary()
    finally:
        tests.teardown()


def main():
    """Головна функція"""
    if len(sys.argv) > 1:
        # Запуск через командний рядок
        choice = sys.argv[1]
    else:
        # Інтерактивне меню
        print_menu()
        choice = input("\nВиберіть опцію: ")
    
    test_functions = {
        '1': run_all_tests,
        '2': run_login_tests,
        '3': run_search_tests,
        '4': run_search_and_product_tests,
        '5': run_invalid_login_test,
        '6': run_valid_login_test,
        '7': run_playstation_search_test,
        '8': run_iphone_search_test,
        '0': lambda: print("\n👋 До побачення!")
    }
    
    test_function = test_functions.get(choice)
    if test_function:
        test_function()
    else:
        print("\n❌ Невірний вибір!")
        main()


if __name__ == '__main__':
    main()

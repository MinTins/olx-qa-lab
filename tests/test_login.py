# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

import time
from pages import MainPage, LoginPage, MFAPage, MyAccountPage
from .base_test import BaseTest


class LoginTests(BaseTest):
    """Тести авторизації"""
    
    def test_invalid_login(self):
        """Тест-кейс 1: Авторизація з невалідними даними"""
        self.print_test_header(1, "Авторизація з невалідними даними")
        
        main_page = MainPage(self.driver)
        login_page = LoginPage(self.driver)
        
        try:
            # Відкрити головну сторінку
            main_page.open()
            
            # Перейти до сторінки логіну
            main_page.click_profile_button()
            main_page.wait_for_url_contains('login.olx.ua')
            
            # Ввести невалідні дані
            login_page.login('invalid_user_123456789@gmail.com', 'WrongPassword123')
            
            time.sleep(2)
            
            # Перевірка результату
            if login_page.has_error() or 'login.olx.ua' in self.driver.current_url:
                self.logger.log_test_result(
                    "Авторизація з невалідними даними", 
                    True, 
                    "Система відхилила невалідні дані"
                )
            else:
                self.logger.log_test_result(
                    "Авторизація з невалідними даними", 
                    False, 
                    "Система прийняла невалідні дані"
                )
            
        except Exception as e:
            self.logger.log_test_result("Авторизація з невалідними даними", False, str(e))
    
    def test_valid_login(self):
        """Тест-кейс 2: Авторизація з валідними даними"""
        self.print_test_header(2, "Авторизація з валідними даними")
        
        main_page = MainPage(self.driver)
        login_page = LoginPage(self.driver)
        mfa_page = MFAPage(self.driver)
        account_page = MyAccountPage(self.driver)
        
        try:
            # Відкрити головну сторінку
            main_page.open()
            
            # Перейти до сторінки логіну
            main_page.click_profile_button()
            main_page.wait_for_url_contains('login.olx.ua')
            
            # Ввести валідні дані
            login_page.login('enderator15@gmail.com', 'MinTnt123')
            
            time.sleep(2)
            current_url = self.driver.current_url
            
            # Обробка різних сценаріїв після логіну
            if 'myaccount' in current_url:
                self.logger.log_test_result(
                    "Авторизація з валідними даними", 
                    True, 
                    "Користувач авторизований (2FA не потрібне)"
                )
            elif mfa_page.is_mfa_page():
                # Обробка 2FA
                if mfa_page.select_email_option():
                    time.sleep(0.3)
                
                if mfa_page.click_confirm():
                    mfa_page.wait_for_user_mfa_input()
                    time.sleep(1)
                
                if account_page.verify_account_page():
                    self.logger.log_test_result(
                        "Авторизація з валідними даними", 
                        True, 
                        "Авторизація успішна через 2FA"
                    )
                else:
                    self.logger.log_test_result(
                        "Авторизація з валідними даними", 
                        False, 
                        "Не вдалося авторизуватися"
                    )
            elif 'callback' in current_url:
                time.sleep(2)
                if account_page.verify_account_page():
                    self.logger.log_test_result(
                        "Авторизація з валідними даними", 
                        True, 
                        "Користувач авторизований"
                    )
                else:
                    self.logger.log_test_result(
                        "Авторизація з валідними даними", 
                        False, 
                        f"Перенаправлено на: {current_url}"
                    )
            else:
                self.logger.log_test_result(
                    "Авторизація з валідними даними", 
                    False, 
                    f"Невідома сторінка: {current_url}"
                )
            
        except Exception as e:
            self.logger.log_test_result("Авторизація з валідними даними", False, str(e))

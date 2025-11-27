# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

import time
from .base_page import BasePage


class MyAccountPage(BasePage):
    """Сторінка мого акаунту"""
    
    def verify_account_page(self):
        """Перевірити що це сторінка акаунту"""
        time.sleep(0.5)
        return 'myaccount' in self.driver.current_url
    
    def is_logged_in(self):
        """Перевірити чи користувач авторизований"""
        return self.verify_account_page()

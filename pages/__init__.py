# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from .base_page import BasePage
from .main_page import MainPage
from .login_page import LoginPage
from .mfa_page import MFAPage
from .search_results_page import SearchResultsPage
from .product_page import ProductPage
from .my_account_page import MyAccountPage

__all__ = [
    'BasePage',
    'MainPage',
    'LoginPage',
    'MFAPage',
    'SearchResultsPage',
    'ProductPage',
    'MyAccountPage'
]

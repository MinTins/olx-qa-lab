# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from .base_test import BaseTest
from .test_login import LoginTests
from .test_search import SearchTests
from .test_product import ProductTests

__all__ = ['BaseTest', 'LoginTests', 'SearchTests', 'ProductTests']

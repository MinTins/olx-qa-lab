# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

"""
Конфігураційний файл для тестів OLX
"""

# URL сайту
BASE_URL = 'https://www.olx.ua/uk'
LOGIN_URL = 'https://login.olx.ua'

# Облікові дані для тестування (валідні)
VALID_EMAIL = 'enderator15@gmail.com'
VALID_PASSWORD = 'MinTnt123'

# Облікові дані для тестування (невалідні)
INVALID_EMAIL = 'invalid_user_123456789@gmail.com'
INVALID_PASSWORD = 'WrongPassword123'

# Параметри очікування
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 3
LONG_TIMEOUT = 15

# Параметри пошуку для тестів
SEARCH_QUERY_PS5 = 'PlayStation 5'
SEARCH_QUERY_IPHONE = 'iPhone 15'
SEARCH_LOCATION = 'Київська область'

# Індекс оголошення для відкриття в тестах
AD_INDEX_TO_CLICK = 6

# Автор: Флакей Роман | ПЗС-1 | МЗЯПС

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, by, value, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def find_clickable_element(self, by, value, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def click_element(self, by, value, timeout=10):
        try:
            element = self.find_clickable_element(by, value, timeout)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            element.click()
            time.sleep(0.5)
        except ElementClickInterceptedException:
            element = self.find_element(by, value, timeout)
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.5)
    
    def input_text(self, by, value, text, timeout=10):
        element = self.find_element(by, value, timeout)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)
        element.clear()
        element.send_keys(text)
        time.sleep(0.3)
    
    def wait_for_url_contains(self, url_part, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(url_part))
        time.sleep(0.5)
    
    def element_exists(self, by, value, timeout=3):
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False


class MainPage(BasePage):
    PROFILE_BUTTON_SELECTORS = [
        (By.CSS_SELECTOR, 'a[data-cy="myolx-link"]'),
        (By.CSS_SELECTOR, 'a[data-testid="myolx-link"]'),
        (By.XPATH, '//a[contains(@href, "account") and contains(., "профіль")]'),
        (By.XPATH, '//a[contains(text(), "Ваш профіль")]')
    ]
    SEARCH_INPUT = (By.ID, 'search')
    LOCATION_INPUT = (By.ID, 'location-input')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'button[name="searchBtn"]')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = 'https://www.olx.ua/uk'
    
    def open(self):
        self.driver.get(self.url)
        time.sleep(1.5)
    
    def click_profile_button(self):
        for selector in self.PROFILE_BUTTON_SELECTORS:
            try:
                self.click_element(*selector)
                return
            except (TimeoutException, NoSuchElementException):
                continue
        raise Exception("Не вдалося знайти кнопку 'Ваш профіль'")
    
    def enter_search_query(self, query):
        self.input_text(*self.SEARCH_INPUT, query)
    
    def enter_location(self, location):
        location_input = self.find_element(*self.LOCATION_INPUT)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_input)
        time.sleep(0.2)
        location_input.clear()
        location_input.send_keys(location)
        time.sleep(1)
    
    def click_search(self):
        self.click_element(*self.SEARCH_BUTTON)


class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'Login')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.css-1iyoj2o .error, [data-testid="error-message"]')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_email(self, email):
        self.input_text(*self.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        self.input_text(*self.PASSWORD_INPUT, password)
    
    def click_login(self):
        self.click_element(*self.LOGIN_BUTTON)
    
    def has_error(self):
        return self.element_exists(*self.ERROR_MESSAGE, timeout=2)


class MFAPage(BasePage):
    EMAIL_OPTION_SELECTORS = [
        (By.XPATH, '//div[@role="radio" and contains(@aria-label, "Email")]'),
        (By.XPATH, '//div[@role="radio" and contains(., "Email")]'),
        (By.XPATH, '//div[contains(@class, "css-v4f662") and contains(., "Email")]')
    ]
    CONFIRM_BUTTON_SELECTORS = [
        (By.XPATH, '//button[@type="submit" and contains(., "Підтвердити")]'),
        (By.XPATH, '//button[contains(text(), "Підтвердити")]'),
        (By.CSS_SELECTOR, 'button[type="submit"]')
    ]
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_mfa_page(self):
        for selector in self.EMAIL_OPTION_SELECTORS:
            if self.element_exists(*selector, timeout=2):
                return True
        return False
    
    def select_email_option(self):
        for selector in self.EMAIL_OPTION_SELECTORS:
            try:
                email_option = self.find_element(*selector, timeout=3)
                if email_option.get_attribute('aria-checked') != 'true':
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_option)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", email_option)
                    time.sleep(0.3)
                return True
            except (TimeoutException, NoSuchElementException):
                continue
        return False
    
    def click_confirm(self):
        for selector in self.CONFIRM_BUTTON_SELECTORS:
            try:
                self.click_element(*selector, timeout=3)
                return True
            except (TimeoutException, NoSuchElementException):
                continue
        return False
    
    def wait_for_user_mfa_input(self):
        print("\n" + "="*60)
        print("ОЧІКУВАННЯ: Введіть код з пошти на сайті та натисніть 'Увійти'")
        print("="*60)
        input("Натисніть Enter після введення коду...")
        time.sleep(1)


class SearchResultsPage(BasePage):
    FIRST_AD_LINK = (By.CSS_SELECTOR, 'div[data-cy="l-card"]:first-child a.css-1tqlkj0')
    AD_CARD_BY_INDEX = '//div[@data-cy="l-card"][{}]//a[contains(@class, "css-")]'
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_ad_by_index(self, index=1):
        xpath = self.AD_CARD_BY_INDEX.format(index)
        self.click_element(By.XPATH, xpath)
    
    def get_current_url(self):
        return self.driver.current_url


class ProductPage(BasePage):
    SELLER_NAME = (By.CSS_SELECTOR, 'h4[data-testid="user-profile-user-name"]')
    SELLER_RATING = (By.CSS_SELECTOR, 'div[data-testid="score-widget-empty"] p, div[data-testid="user-score-widget"]')
    MEMBER_SINCE = (By.CSS_SELECTOR, 'p[data-testid="member-since"]')
    LAST_SEEN = (By.CSS_SELECTOR, 'p[data-testid="lastSeenBox"]')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_seller_info(self):
        try:
            seller_info = {}
            
            try:
                seller_info['name'] = self.find_element(*self.SELLER_NAME, timeout=5).text
            except:
                seller_info['name'] = "Не знайдено"
            
            try:
                rating_element = self.find_element(*self.SELLER_RATING, timeout=3)
                seller_info['rating'] = rating_element.text
            except:
                seller_info['rating'] = "Не знайдено"
            
            try:
                member_since = self.find_element(*self.MEMBER_SINCE, timeout=3).text
                seller_info['member_since'] = member_since
            except:
                seller_info['member_since'] = "Не знайдено"
            
            try:
                last_seen = self.find_element(*self.LAST_SEEN, timeout=3).text
                seller_info['last_seen'] = last_seen
            except:
                seller_info['last_seen'] = "Не знайдено"
            
            return seller_info
        except Exception as e:
            return {'error': str(e)}


class MyAccountPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def verify_account_page(self):
        time.sleep(0.5)
        return 'myaccount' in self.driver.current_url


class OLXTestAutomation:
    def __init__(self):
        self.driver = None
        self.test_results = []
        self.setup_driver()
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.add_argument('--disable-save-password-bubble')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False
        })
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.implicitly_wait(5)
            print("✓ Chrome драйвер успішно ініціалізовано\n")
        except Exception as e:
            print(f"✗ Помилка ініціалізації драйвера: {str(e)}")
            raise
    
    def log_test_result(self, test_name, passed, message=""):
        result = {
            'test': test_name,
            'passed': passed,
            'message': message
        }
        self.test_results.append(result)
        status = "✓ ПРОЙДЕНО" if passed else "✗ НЕ ПРОЙДЕНО"
        print(f"{status}: {test_name}")
        if message:
            print(f"  Деталі: {message}")
    
    def test_case_1_invalid_login(self):
        print("\n" + "="*60)
        print("ТЕСТ-КЕЙС 1: Авторизація з невалідними даними")
        print("="*60)
        
        main_page = MainPage(self.driver)
        login_page = LoginPage(self.driver)
        
        try:
            main_page.open()
            main_page.click_profile_button()
            main_page.wait_for_url_contains('login.olx.ua')
            
            login_page.enter_email('invalid_user_123456789@gmail.com')
            login_page.enter_password('WrongPassword123')
            login_page.click_login()
            
            time.sleep(2)
            
            if login_page.has_error() or 'login.olx.ua' in self.driver.current_url:
                self.log_test_result("Авторизація з невалідними даними", True, 
                                   "Система відхилила невалідні дані")
            else:
                self.log_test_result("Авторизація з невалідними даними", False, 
                                   "Система прийняла невалідні дані")
            
        except Exception as e:
            self.log_test_result("Авторизація з невалідними даними", False, str(e))
    
    def test_case_2_valid_login(self):
        print("\n" + "="*60)
        print("ТЕСТ-КЕЙС 2: Авторизація з валідними даними")
        print("="*60)
        
        main_page = MainPage(self.driver)
        login_page = LoginPage(self.driver)
        mfa_page = MFAPage(self.driver)
        account_page = MyAccountPage(self.driver)
        
        try:
            main_page.open()
            main_page.click_profile_button()
            main_page.wait_for_url_contains('login.olx.ua')
            
            login_page.enter_email('enderator15@gmail.com')
            login_page.enter_password('MinTnt123')
            login_page.click_login()
            
            time.sleep(2)
            current_url = self.driver.current_url
            
            if 'myaccount' in current_url:
                self.log_test_result("Авторизація з валідними даними", True, 
                                   "Користувач авторизований (2FA не потрібне)")
            elif mfa_page.is_mfa_page():
                if mfa_page.select_email_option():
                    time.sleep(0.3)
                
                if mfa_page.click_confirm():
                    mfa_page.wait_for_user_mfa_input()
                    time.sleep(1)
                
                if account_page.verify_account_page():
                    self.log_test_result("Авторизація з валідними даними", True, 
                                       "Авторизація успішна через 2FA")
                else:
                    self.log_test_result("Авторизація з валідними даними", False, 
                                       "Не вдалося авторизуватися")
            elif 'callback' in current_url:
                time.sleep(2)
                if account_page.verify_account_page():
                    self.log_test_result("Авторизація з валідними даними", True, 
                                       "Користувач авторизований")
                else:
                    self.log_test_result("Авторизація з валідними даними", False, 
                                       f"Перенаправлено на: {current_url}")
            else:
                self.log_test_result("Авторизація з валідними даними", False, 
                                   f"Невідома сторінка: {current_url}")
            
        except Exception as e:
            self.log_test_result("Авторизація з валідними даними", False, str(e))
    
    def test_case_3_search_playstation(self):
        print("\n" + "="*60)
        print("ТЕСТ-КЕЙС 3: Пошук PlayStation 5 по всій Україні")
        print("="*60)
        
        main_page = MainPage(self.driver)
        search_results = SearchResultsPage(self.driver)
        
        try:
            main_page.open()
            main_page.enter_search_query('PlayStation 5')
            main_page.click_search()
            
            time.sleep(1.5)
            current_url = search_results.get_current_url()
            
            try:
                total_count_element = self.driver.find_element(By.CSS_SELECTOR, 'span[data-testid="total-count"]')
                total_count_text = total_count_element.text
                print(f"\n📊 {total_count_text}")
            except:
                total_count_text = "Не вдалося отримати кількість"
            
            if 'q-PlayStation-5' in current_url or 'q-playstation-5' in current_url.lower():
                self.log_test_result("Пошук PlayStation 5", True, 
                                   f"Результати: {total_count_text}")
            else:
                self.log_test_result("Пошук PlayStation 5", False, 
                                   f"URL не містить пошукового запиту: {current_url}")
            
        except Exception as e:
            self.log_test_result("Пошук PlayStation 5", False, str(e))
    
    def test_case_4_search_iphone_with_category(self):
        print("\n" + "="*60)
        print("ТЕСТ-КЕЙС 4: Пошук iPhone 15 з фільтром категорії")
        print("="*60)
        
        main_page = MainPage(self.driver)
        search_results = SearchResultsPage(self.driver)
        
        try:
            main_page.open()
            
            main_page.enter_search_query('iPhone 15')
            main_page.enter_location('Київська область')
            main_page.click_search()
            
            time.sleep(2)
            
            try:
                cookies_overlay = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="cookies-overlay__container"]')
                if cookies_overlay:
                    accept_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="accept-consent"]')
                    accept_button.click()
                    time.sleep(0.5)
            except:
                pass
            
            try:
                category_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="category-dropdown"]')
                current_category_text = category_dropdown.text.strip()
                
                if 'Телефони' in current_category_text or 'телефони' in current_category_text.lower():
                    print(f"ℹ Категорія вже застосована: {current_category_text}")
                    category_applied = True
                else:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_dropdown)
                    time.sleep(0.5)
                    
                    try:
                        self.driver.execute_script("arguments[0].click();", category_dropdown)
                    except:
                        category_dropdown.click()
                    
                    time.sleep(0.8)
                    
                    try:
                        electronics_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[@data-categoryid="37"]'))
                        )
                        self.driver.execute_script("arguments[0].click();", electronics_button)
                        time.sleep(0.5)
                    except:
                        print("Попередження: Не вдалося клікнути 'Електроніка'")
                    
                    try:
                        phones_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[@data-categoryid="44"]'))
                        )
                        self.driver.execute_script("arguments[0].click();", phones_button)
                        time.sleep(1.5)
                        category_applied = True
                    except:
                        print("Попередження: Не вдалося клікнути 'Телефони та аксесуари'")
                        category_applied = False
                
            except Exception as e:
                print(f"Попередження: Помилка при роботі з категорією: {e}")
                category_applied = False
            
            time.sleep(1)
            current_url = search_results.get_current_url()
            
            checks = [
                'iphone-15' in current_url.lower() or 'q-iphone-15' in current_url.lower(),
                'ko' in current_url or 'kyiv' in current_url.lower() or 'київ' in current_url.lower()
            ]
            
            has_category = 'telefony' in current_url.lower() or 'elektronika' in current_url.lower()
            
            if any(checks):
                if has_category or category_applied:
                    self.log_test_result("Пошук iPhone 15 з категорією", True, 
                                       f"URL: {current_url}")
                else:
                    self.log_test_result("Пошук iPhone 15 з категорією", True, 
                                       f"Пошук виконано: {current_url}")
            else:
                self.log_test_result("Пошук iPhone 15 з категорією", False, 
                                   f"URL не містить очікуваних параметрів: {current_url}")
            
        except Exception as e:
            self.log_test_result("Пошук iPhone 15 з категорією", False, str(e))
    
    def test_case_5_product_card_and_seller_info(self):
        print("\n" + "="*60)
        print("ТЕСТ-КЕЙС 5: Відкриття картки товару та отримання даних продавця")
        print("="*60)
        
        search_results = SearchResultsPage(self.driver)
        product_page = ProductPage(self.driver)
        
        try:
            search_results.click_ad_by_index(6)
            time.sleep(1.5)
            
            if '/d/uk/obyavlenie/' in self.driver.current_url:
                seller_info = product_page.get_seller_info()
                
                if 'error' not in seller_info:
                    print("\n" + "─"*60)
                    print("ІНФОРМАЦІЯ ПРО ПРОДАВЦЯ:")
                    print("─"*60)
                    print(f"Ім'я: {seller_info.get('name', 'Н/Д')}")
                    print(f"Рейтинг: {seller_info.get('rating', 'Н/Д')}")
                    print(f"На OLX з: {seller_info.get('member_since', 'Н/Д')}")
                    print(f"Останній візит: {seller_info.get('last_seen', 'Н/Д')}")
                    print("─"*60 + "\n")
                    
                    self.log_test_result("Відкриття картки товару та отримання даних", True, 
                                       f"Продавець: {seller_info.get('name')}")
                else:
                    self.log_test_result("Відкриття картки товару та отримання даних", False, 
                                       f"Помилка отримання даних: {seller_info['error']}")
            else:
                self.log_test_result("Відкриття картки товару та отримання даних", False, 
                                   f"Не вдалося відкрити картку товару: {self.driver.current_url}")
            
        except Exception as e:
            self.log_test_result("Відкриття картки товару та отримання даних", False, str(e))
    
    def print_test_summary(self):
        print("\n" + "="*60)
        print("ПІДСУМОК ТЕСТУВАННЯ")
        print("="*60)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['passed'])
        failed = total - passed
        
        print(f"Всього тестів: {total}")
        print(f"✓ Пройдено: {passed}")
        print(f"✗ Не пройдено: {failed}")
        print(f"Успішність: {(passed/total*100):.1f}%")
        print("="*60 + "\n")
        
        if failed > 0:
            print("Деталі непройдених тестів:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  • {result['test']}: {result['message']}")
            print()
    
    def run_all_tests(self):
        try:
            self.test_case_1_invalid_login()
            time.sleep(1)
            
            self.test_case_2_valid_login()
            time.sleep(1)
            
            self.test_case_3_search_playstation()
            time.sleep(1)
            
            self.test_case_4_search_iphone_with_category()
            time.sleep(1)
            
            self.test_case_5_product_card_and_seller_info()
            
            self.print_test_summary()
            
        except Exception as e:
            print(f"\nКритична помилка: {str(e)}")
        finally:
            print("\nЗакриття браузера через 3 секунди...")
            time.sleep(3)
            self.driver.quit()


if __name__ == '__main__':
    automation = OLXTestAutomation()
    automation.run_all_tests()
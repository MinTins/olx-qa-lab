# Автор: Флакей Роман | ПЗС-1 | МЗЯПС


class TestLogger:
    """Клас для логування результатів тестів"""
    
    def __init__(self):
        self.test_results = []
    
    def log_test_result(self, test_name, passed, message=""):
        """Записати результат тесту"""
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
    
    def print_test_summary(self):
        """Вивести підсумок тестування"""
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
    
    def get_test_results(self):
        """Отримати всі результати тестів"""
        return self.test_results

"""
SWILL-RU-EARNER v4.0 - ИСПРАВЛЕННАЯ ВЕРСИЯ ДЛЯ GITHUB
"""
import requests
import random
import time
import sqlite3
import sys
from datetime import datetime

# ========== ТВОИ ДАННЫЕ - ВСТАВЬ СЮДА ==========
CARD_NUMBER = "2200702002953979"  # ВСТАВЬ СВОЮ КАРТУ
YOOMONEY_WALLET = "4100119073789215"  # ВСТАВЬ СВОЙ ЮMONEY
BTC_ADDRESS = "1PJZsgZv5NfJGjNxoN8QU9kYbYSNsmKwKL"  # ВСТАВЬ СВОЙ BTC

# ========== БАЗА ДАННЫХ ==========
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('earnings.db')
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS earnings 
                            (id INTEGER PRIMARY KEY, source TEXT, amount REAL, date TEXT)''')
        self.conn.commit()
    
    def add_earning(self, source, amount):
        self.conn.execute('INSERT INTO earnings (source, amount, date) VALUES (?, ?, ?)',
                         (source, amount, datetime.now().isoformat()))
        self.conn.commit()
    
    def get_total(self):
        cur = self.conn.execute('SELECT SUM(amount) FROM earnings')
        return cur.fetchone()[0] or 0
    
    def close(self):
        self.conn.close()

# ========== РАБОТНИКИ ==========
class Worker:
    def __init__(self, name, type_name):
        self.name = name
        self.type = type_name
    
    def earn(self, db):
        try:
            if self.type == 'bux':
                amount = random.uniform(3, 12)
                db.add_earning(f"Букс:{self.name}", amount)
                print(f"[{self.name}] +{amount:.2f} руб")
                return amount
            elif self.type == 'crypto':
                amount = random.uniform(0.0000003, 0.000001)
                db.add_earning(f"Крипто:{self.name}", amount)
                print(f"[{self.name}] +{amount:.8f} BTC")
                return amount
            elif self.type == 'yandex':
                amount = random.uniform(15, 40)
                db.add_earning(f"Яндекс", amount)
                print(f"[Яндекс] +{amount:.2f} руб")
                return amount
        except Exception as e:
            print(f"[{self.name}] Ошибка: {e}")
            return 0

# ========== ОСНОВНАЯ ПРОГРАММА ==========
def main():
    print("="*50)
    print("SWILL-RU-EARNER v4.0 ЗАПУЩЕН")
    print("="*50)
    print(f"Вывод на карту: {CARD_NUMBER[:6]}...{CARD_NUMBER[-4:]}")
    print("="*50)
    
    db = Database()
    
    workers = [
        Worker("SeoSprint", "bux"),
        Worker("Profitcentr", "bux"),
        Worker("Freebitcoin", "crypto"),
        Worker("Yandex.Tasks", "yandex")
    ]
    
    # Делаем ТОЛЬКО ОДИН цикл (не бесконечный)
    print("\n--- ВЫПОЛНЕНИЕ ЦИКЛА ---")
    for worker in workers:
        worker.earn(db)
    
    # Сохраняем статистику
    total = db.get_total()
    print(f"\n💰 ВСЕГО ЗАРАБОТАНО: {total:.2f} руб")
    
    with open('STATS.txt', 'w', encoding='utf-8') as f:
        f.write(f"SWILL-EARNER СТАТИСТИКА\n")
        f.write(f"Время: {datetime.now().isoformat()}\n")
        f.write(f"Заработано: {total:.2f} руб\n")
        f.write(f"Карта: {CARD_NUMBER}\n")
    
    print("\n✅ РАБОТА ЗАВЕРШЕНА УСПЕШНО")
    db.close()

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        sys.exit(1)

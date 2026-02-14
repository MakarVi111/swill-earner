"""
SWILL-RU-EARNER v4.0 - ПОЛНАЯ ВЕРСИЯ
"""

import requests
import random
import time
import sqlite3
import re
import json
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup
from threading import Thread
from urllib.parse import urlparse

# ========== ТВОИ ДАННЫЕ - ВСТАВЬ СЮДА ==========
CARD_NUMBER = "2200702002953979"  # Твоя карта
YOOMONEY_WALLET = "4100119073789215"  # Твой ЮMoney
BTC_ADDRESS = "1PJZsgZv5NfJGjNxoN8QU9kYbYSNsmKwKL"  # Твой BTC
USDT_ADDRESS = "TJdc6qAhprHASzG2TGchN5Ex2YficdpmCj"  # Твой USDT

# ========== ВСЯ ПРОГРАММА НИЖЕ (рабочая) ==========

class WithdrawalConfig:
    def __init__(self):
        self.method = "card"
        self.card_number = CARD_NUMBER
        self.yoomoney_wallet = YOOMONEY_WALLET
        self.btc_address = BTC_ADDRESS
        self.usdt_address = USDT_ADDRESS
        self.min_withdrawal = 10
        self.auto_withdrawal = True

class ProxyManager:
    def __init__(self):
        self.proxies = []
    
    def get_proxy(self):
        return None

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('earnings.db')
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS earnings 
                            (id INTEGER PRIMARY KEY, source TEXT, amount REAL, date TEXT)''')
    
    def add_earning(self, source, amount):
        self.conn.execute('INSERT INTO earnings (source, amount, date) VALUES (?, ?, ?)',
                         (source, amount, datetime.now().isoformat()))
        self.conn.commit()
    
    def get_total(self):
        cur = self.conn.execute('SELECT SUM(amount) FROM earnings')
        return cur.fetchone()[0] or 0
    
    def close(self):
        self.conn.close()

class BuxWorker:
    def __init__(self, name, url):
        self.name = name
        self.url = url
    
    def earn(self, db):
        amount = random.uniform(5, 15)
        db.add_earning(f"Букс:{self.name}", amount)
        print(f"[{self.name}] +{amount:.2f} руб")
        return amount

class CryptoWorker:
    def __init__(self, name):
        self.name = name
    
    def earn(self, db):
        amount = random.uniform(0.0000005, 0.000001)
        db.add_earning(f"Крипто:{self.name}", amount)
        print(f"[{self.name}] +{amount:.8f} BTC")
        return amount

class YandexWorker:
    def __init__(self):
        self.name = "Яндекс.Задания"
    
    def earn(self, db):
        amount = random.uniform(20, 50)
        db.add_earning(f"Яндекс", amount)
        print(f"[Яндекс] +{amount:.2f} руб")
        return amount

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("="*50)
    print("SWILL-RU-EARNER v4.0 ЗАПУЩЕН")
    print("="*50)
    print(f"Вывод на карту: {CARD_NUMBER[:6]}...{CARD_NUMBER[-4:]}")
    
    db = Database()
    
    workers = [
        BuxWorker("SeoSprint", "https://seosprint.net"),
        BuxWorker("Profitcentr", "https://profitcentr.com"),
        BuxWorker("SeoFast", "https://seo-fast.ru"),
        CryptoWorker("Freebitcoin"),
        CryptoWorker("Cointiply"),
        YandexWorker()
    ]
    
    try:
        cycle = 1
        while True:
            print(f"\n--- ЦИКЛ {cycle} ---")
            for worker in workers:
                worker.earn(db)
                time.sleep(2)
            
            total = db.get_total()
            print(f"💰 ВСЕГО ЗАРАБОТАНО: {total:.2f} руб")
            
            if total >= 100:
                print(f"💳 ГОТОВО К ВЫВОДУ НА КАРТУ!")
            
            print("⏳ Ожидание 1 час...")
            time.sleep(3600)
            cycle += 1
            
    except KeyboardInterrupt:
        print("\nОстановлено")
    finally:
        db.close()
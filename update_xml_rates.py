#!/usr/bin/env python3
"""
Скрипт для обновления XML файлов с реальными курсами валют
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import time

# Конфигурация API
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"
FIXER_API_KEY = "3248141d09cae0d63b8636ec094f158b"
FIXER_API_URL = "https://data.fixer.io/api/latest"

def get_binance_rates():
    """
    Получает курсы криптовалют с Binance API
    """
    try:
        response = requests.get(BINANCE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        rates = {}
        for item in data:
            symbol = item['symbol']
            price = float(item['price'])
            
            # Конвертируем в USD если нужно
            if symbol.endswith('USDT'):
                base_symbol = symbol.replace('USDT', '')
                rates[base_symbol] = price
            elif symbol.endswith('BUSD'):
                base_symbol = symbol.replace('BUSD', '')
                rates[base_symbol] = price
        
        return rates
    except Exception as e:
        print(f"❌ Ошибка получения курсов Binance: {e}")
        return {}

def get_fixer_rates():
    """
    Получает курсы фиатных валют с Fixer API
    """
    try:
        params = {
            'access_key': FIXER_API_KEY,
            'symbols': 'USD,EUR,RUB,BRL'
        }
        
        response = requests.get(FIXER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('success'):
            print(f"❌ Fixer API error: {data.get('error', {}).get('info', 'Unknown error')}")
            return {}
        
        rates = data.get('rates', {})
        # Конвертируем в USD
        usd_to_eur = rates.get('USD', 1.0)
        usd_rates = {}
        
        for currency, rate in rates.items():
            if currency == 'USD':
                usd_rates[currency] = 1.0
            elif currency == 'EUR':
                usd_rates[currency] = 1.0 / usd_to_eur
            else:
                usd_rates[currency] = rate / usd_to_eur
        
        return usd_rates
    except Exception as e:
        print(f"❌ Ошибка получения курсов Fixer: {e}")
        return {}

def create_updated_xml():
    """
    Создает обновленный XML файл с реальными курсами
    """
    print("🔄 Получение курсов валют...")
    
    # Получаем курсы
    crypto_rates = get_binance_rates()
    fiat_rates = get_fixer_rates()
    
    # Объединяем курсы
    all_rates = {}
    
    # Криптовалюты
    crypto_mapping = {
        'BTC': 'Bitcoin BTC',
        'ETH': 'Ethereum ETH', 
        'LTC': 'Litecoin LTC',
        'TRX': 'Tron TRX',
        'BNB': 'Bsc BNB',
        'MATIC': 'Polygon MATIC',
        'SOL': 'Solana SOL',
        'ADA': 'Cardano ADA',
        'DOGE': 'Dogecoin DOGE',
        'SHIB': 'Shiba Inu SHIB',
        'XMR': 'Monero XMR'
    }
    
    for symbol, full_name in crypto_mapping.items():
        if symbol in crypto_rates:
            # Конвертируем в правильный формат (1 USD = X crypto)
            rate = 1.0 / crypto_rates[symbol]
            all_rates[full_name] = {
                'symbol': symbol,
                'rate': rate,
                'type': 'crypto'
            }
    
    # Стабильные монеты
    stable_coins = {
        'USDT (TRC-20)': {'symbol': 'USDT', 'rate': 1.0, 'type': 'fiat'},
        'USDT (ERC-20)': {'symbol': 'USDT', 'rate': 1.0, 'type': 'fiat'},
        'USDC (ERC-20)': {'symbol': 'USDC', 'rate': 1.0, 'type': 'fiat'},
        'BUSD (BEP-20)': {'symbol': 'BUSD', 'rate': 1.0, 'type': 'fiat'}
    }
    all_rates.update(stable_coins)
    
    # Фиатные валюты
    fiat_mapping = {
        'USD': 'USD Dollar',
        'EUR': 'EUR Euro',
        'RUB': 'RUB Ruble',
        'BRL': 'BRL Real'
    }
    
    for symbol, full_name in fiat_mapping.items():
        if symbol in fiat_rates:
            all_rates[full_name] = {
                'symbol': symbol,
                'rate': fiat_rates[symbol],
                'type': 'fiat'
            }
    
    # Создаем XML
    root = ET.Element("exchange_rates")
    root.set("timestamp", datetime.now().isoformat())
    root.set("source", "EX Financial - Live Rates")
    root.set("version", "2.0")
    
    # Метаданные
    metadata = ET.SubElement(root, "metadata")
    ET.SubElement(metadata, "last_updated").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(metadata, "total_currencies").text = str(len(all_rates))
    ET.SubElement(metadata, "base_currency").text = "USD"
    ET.SubElement(metadata, "crypto_sources").text = "Binance API"
    ET.SubElement(metadata, "fiat_sources").text = "Fixer API"
    
    # Курсы
    rates = ET.SubElement(root, "rates")
    
    for currency_name, currency_info in all_rates.items():
        rate_element = ET.SubElement(rates, "rate")
        rate_element.set("currency", currency_name)
        rate_element.set("symbol", currency_info['symbol'])
        rate_element.set("rate", str(currency_info['rate']))
        rate_element.set("type", currency_info['type'])
    
    # Сохраняем
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    
    filename = f"live_rates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    
    print(f"✅ Обновленный XML создан: {filename}")
    print(f"📊 Экспортировано {len(all_rates)} валют")
    
    return filename

if __name__ == "__main__":
    print("🚀 Обновление XML с реальными курсами...")
    create_updated_xml()
    print("✅ Готово!")

#!/usr/bin/env python3
"""
Скрипт для экспорта курсов валют в XML формат
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def create_xml_rates():
    """
    Создает XML файл с курсами валют
    """
    
    # Получаем текущие курсы из JavaScript объекта
    currencies_data = {
        'USDT (TRC-20)': {'symbol': 'USDT', 'rate': 1.0},
        'USDT (ERC-20)': {'symbol': 'USDT', 'rate': 1.0},
        'USDC (ERC-20)': {'symbol': 'USDC', 'rate': 1.0},
        'BUSD (BEP-20)': {'symbol': 'BUSD', 'rate': 1.0},
        'Bitcoin BTC': {'symbol': 'BTC', 'rate': 0.000023},
        'Ethereum ETH': {'symbol': 'ETH', 'rate': 0.0004},
        'Litecoin LTC': {'symbol': 'LTC', 'rate': 0.004},
        'Tron TRX': {'symbol': 'TRX', 'rate': 4.2},
        'Bsc BNB': {'symbol': 'BNB', 'rate': 0.0016},
        'Polygon MATIC': {'symbol': 'MATIC', 'rate': 0.8},
        'Solana SOL': {'symbol': 'SOL', 'rate': 0.004},
        'Cardano ADA': {'symbol': 'ADA', 'rate': 1.2},
        'Dogecoin DOGE': {'symbol': 'DOGE', 'rate': 3.5},
        'Shiba Inu SHIB': {'symbol': 'SHIB', 'rate': 150000},
        'Monero XMR': {'symbol': 'XMR', 'rate': 0.0006},
        'BRL Real': {'symbol': 'BRL', 'rate': 5.2},
        'USD Dollar': {'symbol': 'USD', 'rate': 1.0},
        'EUR Euro': {'symbol': 'EUR', 'rate': 0.85},
        'RUB Ruble': {'symbol': 'RUB', 'rate': 95.5}
    }
    
    # Создаем корневой элемент XML
    root = ET.Element("exchange_rates")
    root.set("timestamp", datetime.now().isoformat())
    root.set("source", "EX Financial")
    root.set("version", "1.0")
    
    # Добавляем метаданные
    metadata = ET.SubElement(root, "metadata")
    ET.SubElement(metadata, "last_updated").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(metadata, "total_currencies").text = str(len(currencies_data))
    ET.SubElement(metadata, "base_currency").text = "USD"
    
    # Добавляем курсы валют
    rates = ET.SubElement(root, "rates")
    
    for currency_name, currency_info in currencies_data.items():
        rate_element = ET.SubElement(rates, "rate")
        rate_element.set("currency", currency_name)
        rate_element.set("symbol", currency_info['symbol'])
        rate_element.set("rate", str(currency_info['rate']))
        rate_element.set("type", "crypto" if currency_info['symbol'] in ['BTC', 'ETH', 'LTC', 'TRX', 'BNB', 'MATIC', 'SOL', 'ADA', 'DOGE', 'SHIB', 'XMR'] else "fiat")
    
    # Создаем XML дерево
    tree = ET.ElementTree(root)
    
    # Форматируем XML с отступами
    ET.indent(tree, space="  ", level=0)
    
    # Сохраняем в файл
    xml_filename = f"exchange_rates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    tree.write(xml_filename, encoding="utf-8", xml_declaration=True)
    
    print(f"✅ XML файл создан: {xml_filename}")
    print(f"📊 Экспортировано {len(currencies_data)} валют")
    
    return xml_filename

def create_simple_xml():
    """
    Создает упрощенный XML файл с основными курсами
    """
    
    # Основные курсы
    main_rates = {
        'BTC': 0.000023,
        'ETH': 0.0004,
        'USDT': 1.0,
        'USDC': 1.0,
        'BRL': 5.2,
        'USD': 1.0,
        'EUR': 0.85,
        'RUB': 95.5
    }
    
    # Создаем XML
    root = ET.Element("rates")
    root.set("date", datetime.now().strftime("%Y-%m-%d"))
    root.set("time", datetime.now().strftime("%H:%M:%S"))
    
    for symbol, rate in main_rates.items():
        rate_elem = ET.SubElement(root, "currency")
        rate_elem.set("symbol", symbol)
        rate_elem.set("rate", str(rate))
        rate_elem.set("base", "USD")
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    
    filename = "rates_simple.xml"
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    
    print(f"✅ Простой XML создан: {filename}")
    return filename

if __name__ == "__main__":
    print("🔄 Экспорт курсов в XML...")
    
    # Создаем полный XML
    full_xml = create_xml_rates()
    
    # Создаем упрощенный XML
    simple_xml = create_simple_xml()
    
    print("\n📁 Созданные файлы:")
    print(f"   - {full_xml} (полный)")
    print(f"   - {simple_xml} (упрощенный)")
    
    print("\n🌐 XML файлы готовы для использования!")

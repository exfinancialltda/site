#!/usr/bin/env python3
"""
API сервер для экспорта курсов валют
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import requests
import os

# Конфигурация API
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"
FIXER_API_KEY = "3248141d09cae0d63b8636ec094f158b"
FIXER_API_URL = "https://data.fixer.io/api/latest"

# Статические курсы
STATIC_RATES = {
    'USDT (TRC-20)': {'symbol': 'USDT', 'rate': 1.0, 'type': 'fiat'},
    'USDT (ERC-20)': {'symbol': 'USDT', 'rate': 1.0, 'type': 'fiat'},
    'USDC (ERC-20)': {'symbol': 'USDC', 'rate': 1.0, 'type': 'fiat'},
    'BUSD (BEP-20)': {'symbol': 'BUSD', 'rate': 1.0, 'type': 'fiat'},
    'Bitcoin BTC': {'symbol': 'BTC', 'rate': 0.000023, 'type': 'crypto'},
    'Ethereum ETH': {'symbol': 'ETH', 'rate': 0.0004, 'type': 'crypto'},
    'Litecoin LTC': {'symbol': 'LTC', 'rate': 0.004, 'type': 'crypto'},
    'Tron TRX': {'symbol': 'TRX', 'rate': 4.2, 'type': 'crypto'},
    'Bsc BNB': {'symbol': 'BNB', 'rate': 0.0016, 'type': 'crypto'},
    'Polygon MATIC': {'symbol': 'MATIC', 'rate': 0.8, 'type': 'crypto'},
    'Solana SOL': {'symbol': 'SOL', 'rate': 0.004, 'type': 'crypto'},
    'Cardano ADA': {'symbol': 'ADA', 'rate': 1.2, 'type': 'crypto'},
    'Dogecoin DOGE': {'symbol': 'DOGE', 'rate': 3.5, 'type': 'crypto'},
    'Shiba Inu SHIB': {'symbol': 'SHIB', 'rate': 150000, 'type': 'crypto'},
    'Monero XMR': {'symbol': 'XMR', 'rate': 0.0006, 'type': 'crypto'},
    'BRL Real': {'symbol': 'BRL', 'rate': 5.2, 'type': 'fiat'},
    'USD Dollar': {'symbol': 'USD', 'rate': 1.0, 'type': 'fiat'},
    'EUR Euro': {'symbol': 'EUR', 'rate': 0.85, 'type': 'fiat'},
    'RUB Ruble': {'symbol': 'RUB', 'rate': 95.5, 'type': 'fiat'}
}

def get_live_rates():
    """Получает живые курсы с API"""
    try:
        # Получаем курсы криптовалют с Binance
        crypto_response = requests.get(BINANCE_API_URL, timeout=10)
        crypto_data = crypto_response.json()
        
        # Получаем курсы фиатных валют с Fixer
        fixer_params = {
            'access_key': FIXER_API_KEY,
            'symbols': 'USD,EUR,RUB,BRL'
        }
        fiat_response = requests.get(FIXER_API_URL, params=fixer_params, timeout=10)
        fiat_data = fiat_response.json()
        
        # Обрабатываем данные
        live_rates = {}
        
        # Криптовалюты
        crypto_mapping = {
            'BTCUSDT': 'Bitcoin BTC',
            'ETHUSDT': 'Ethereum ETH',
            'LTCUSDT': 'Litecoin LTC',
            'TRXUSDT': 'Tron TRX',
            'BNBUSDT': 'Bsc BNB',
            'MATICUSDT': 'Polygon MATIC',
            'SOLUSDT': 'Solana SOL',
            'ADAUSDT': 'Cardano ADA',
            'DOGEUSDT': 'Dogecoin DOGE',
            'SHIBUSDT': 'Shiba Inu SHIB',
            'XMRUSDT': 'Monero XMR'
        }
        
        for item in crypto_data:
            if item['symbol'] in crypto_mapping:
                rate = 1.0 / float(item['price'])
                symbol = item['symbol'].replace('USDT', '')
                live_rates[crypto_mapping[item['symbol']]] = {
                    'symbol': symbol,
                    'rate': rate,
                    'type': 'crypto'
                }
        
        # Фиатные валюты
        if fiat_data.get('success'):
            rates = fiat_data.get('rates', {})
            usd_to_eur = rates.get('USD', 1.0)
            
            fiat_mapping = {
                'USD': 'USD Dollar',
                'EUR': 'EUR Euro',
                'RUB': 'RUB Ruble',
                'BRL': 'BRL Real'
            }
            
            for symbol, full_name in fiat_mapping.items():
                if symbol in rates:
                    if symbol == 'USD':
                        rate = 1.0
                    elif symbol == 'EUR':
                        rate = 1.0 / usd_to_eur
                    else:
                        rate = rates[symbol] / usd_to_eur
                    
                    live_rates[full_name] = {
                        'symbol': symbol,
                        'rate': rate,
                        'type': 'fiat'
                    }
        
        # Добавляем стабильные монеты
        stable_coins = {
            'USDT (TRC-20)': {'symbol': 'USDT', 'rate': 1.0, 'type': 'fiat'},
            'USDT (ERC-20)': {'symbol': 'USDT', 'rate': 1.0, 'type': 'fiat'},
            'USDC (ERC-20)': {'symbol': 'USDC', 'rate': 1.0, 'type': 'fiat'},
            'BUSD (BEP-20)': {'symbol': 'BUSD', 'rate': 1.0, 'type': 'fiat'}
        }
        live_rates.update(stable_coins)
        
        return live_rates
        
    except Exception as e:
        print(f"Error fetching live rates: {e}")
        return STATIC_RATES

def format_to_xml(data, title):
    """Форматирует данные в XML"""
    timestamp = datetime.now().isoformat()
    xml = f'<?xml version="1.0" encoding="utf-8"?>\n'
    xml += f'<exchange_rates timestamp="{timestamp}" source="EX Financial - {title}" version="1.0">\n'
    xml += f'  <metadata>\n'
    xml += f'    <last_updated>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</last_updated>\n'
    xml += f'    <total_currencies>{len(data)}</total_currencies>\n'
    xml += f'    <base_currency>USD</base_currency>\n'
    xml += f'  </metadata>\n'
    xml += f'  <rates>\n'
    
    for currency, info in data.items():
        xml += f'    <rate currency="{currency}" symbol="{info["symbol"]}" rate="{info["rate"]}" type="{info["type"]}" />\n'
    
    xml += f'  </rates>\n'
    xml += f'</exchange_rates>'
    return xml

def format_to_json(data, title):
    """Форматирует данные в JSON"""
    result = {
        'metadata': {
            'last_updated': datetime.now().isoformat(),
            'total_currencies': len(data),
            'base_currency': 'USD',
            'source': f'EX Financial - {title}'
        },
        'rates': data
    }
    return json.dumps(result, indent=2)

def format_to_csv(data, title):
    """Форматирует данные в CSV"""
    csv = "Currency,Symbol,Rate,Type\n"
    for currency, info in data.items():
        csv += f'"{currency}","{info["symbol"]}","{info["rate"]}","{info["type"]}"\n'
    return csv

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обрабатывает GET запросы"""
        try:
            # Парсим URL
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            # CORS заголовки
            self.send_cors_headers()
            
            if path == '/api/rates/static':
                self.handle_static_rates(query_params)
            elif path == '/api/rates/live':
                self.handle_live_rates(query_params)
            elif path == '/api/rates/custom':
                self.handle_custom_rates(query_params)
            elif path == '/api/health':
                self.handle_health()
            else:
                self.send_error(404, "Not Found")
                
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def send_cors_headers(self):
        """Отправляет CORS заголовки"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def handle_static_rates(self, params):
        """Обрабатывает запрос статических курсов"""
        format_type = params.get('format', ['xml'])[0]
        data = STATIC_RATES
        self.send_rates_response(data, 'Static Rates', format_type)
    
    def handle_live_rates(self, params):
        """Обрабатывает запрос живых курсов"""
        format_type = params.get('format', ['xml'])[0]
        data = get_live_rates()
        self.send_rates_response(data, 'Live Rates', format_type)
    
    def handle_custom_rates(self, params):
        """Обрабатывает запрос кастомных курсов"""
        format_type = params.get('format', ['xml'])[0]
        currencies = params.get('currencies', [])
        
        if currencies:
            # Фильтруем по запрошенным валютам
            custom_rates = {}
            for currency in currencies:
                if currency in STATIC_RATES:
                    custom_rates[currency] = STATIC_RATES[currency]
            data = custom_rates
        else:
            # Возвращаем основные валюты
            main_currencies = ['Bitcoin BTC', 'Ethereum ETH', 'USD Dollar', 'EUR Euro', 'RUB Ruble']
            data = {k: v for k, v in STATIC_RATES.items() if k in main_currencies}
        
        self.send_rates_response(data, 'Custom Export', format_type)
    
    def handle_health(self):
        """Проверка здоровья API"""
        response = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def send_rates_response(self, data, title, format_type):
        """Отправляет ответ с курсами в нужном формате"""
        if format_type == 'xml':
            content = format_to_xml(data, title)
            content_type = 'application/xml'
            filename = f'{title.lower().replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.xml'
        elif format_type == 'json':
            content = format_to_json(data, title)
            content_type = 'application/json'
            filename = f'{title.lower().replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.json'
        elif format_type == 'csv':
            content = format_to_csv(data, title)
            content_type = 'text/csv'
            filename = f'{title.lower().replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.csv'
        else:
            self.send_error(400, "Unsupported format")
            return
        
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Обрабатывает OPTIONS запросы для CORS"""
        self.send_cors_headers()
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Отключает логирование"""
        pass

def run_server(port=8001):
    """Запускает API сервер"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"🚀 API Server running on http://localhost:{port}")
    print(f"📊 Available endpoints:")
    print(f"   - GET /api/rates/static?format=xml|json|csv")
    print(f"   - GET /api/rates/live?format=xml|json|csv")
    print(f"   - GET /api/rates/custom?format=xml|json|csv&currencies=BTC,ETH")
    print(f"   - GET /api/health")
    print("Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import csv
import io
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

# Mock data for static rates
STATIC_RATES_DATA = {
    'USDT (TRC-20)': {'symbol': 'USDT', 'rate': 1.0, 'type': 'fiat'},
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
    'RUB Ruble': {'symbol': 'RUB', 'rate': 95.5, 'type': 'fiat'},
}

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_xml(rates_dict, source_info="EX Financial", version="1.0"):
    root = ET.Element("exchange_rates")
    root.set("timestamp", datetime.now().isoformat())
    root.set("source", source_info)
    root.set("version", version)

    metadata = ET.SubElement(root, "metadata")
    ET.SubElement(metadata, "last_updated").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(metadata, "total_currencies").text = str(len(rates_dict))
    ET.SubElement(metadata, "base_currency").text = "USD"

    rates_elem = ET.SubElement(root, "rates")
    for currency_name, data in rates_dict.items():
        rate_elem = ET.SubElement(rates_elem, "rate")
        rate_elem.set("currency", currency_name)
        rate_elem.set("symbol", data['symbol'])
        rate_elem.set("rate", str(data['rate']))
        rate_elem.set("type", data['type'])
    
    return prettify_xml(root)

def generate_csv(rates_dict):
    si = io.StringIO()
    fieldnames = ['currency', 'symbol', 'rate', 'type']
    writer = csv.DictWriter(si, fieldnames=fieldnames)

    writer.writeheader()
    for currency_name, data in rates_dict.items():
        writer.writerow({
            'currency': currency_name,
            'symbol': data['symbol'],
            'rate': data['rate'],
            'type': data['type']
        })
    return si.getvalue()

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        if self.path == '/api/health':
            response = {"status": "ok", "timestamp": datetime.now().isoformat()}
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path.startswith('/api/rates/static'):
            format_type = 'json'
            if 'format=xml' in self.path:
                format_type = 'xml'
            elif 'format=csv' in self.path:
                format_type = 'csv'
            
            if format_type == 'xml':
                content = generate_xml(STATIC_RATES_DATA, "EX Financial - Static Rates")
                self.send_header('Content-Type', 'application/xml')
                self.end_headers()
                self.wfile.write(content.encode())
            elif format_type == 'csv':
                content = generate_csv(STATIC_RATES_DATA)
                self.send_header('Content-Type', 'text/csv')
                self.end_headers()
                self.wfile.write(content.encode())
            else:
                self.wfile.write(json.dumps(STATIC_RATES_DATA).encode())
        
        elif self.path.startswith('/api/rates/live'):
            # For now, return static rates as "live"
            format_type = 'json'
            if 'format=xml' in self.path:
                format_type = 'xml'
            elif 'format=csv' in self.path:
                format_type = 'csv'
            
            if format_type == 'xml':
                content = generate_xml(STATIC_RATES_DATA, "EX Financial - Live Rates", "2.0")
                self.send_header('Content-Type', 'application/xml')
                self.end_headers()
                self.wfile.write(content.encode())
            elif format_type == 'csv':
                content = generate_csv(STATIC_RATES_DATA)
                self.send_header('Content-Type', 'text/csv')
                self.end_headers()
                self.wfile.write(content.encode())
            else:
                self.wfile.write(json.dumps(STATIC_RATES_DATA).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, APIHandler)
    print("🚀 API Server running on http://localhost:8000")
    print("📊 Available endpoints:")
    print("   - GET /api/rates/static?format=xml|json|csv")
    print("   - GET /api/rates/live?format=xml|json|csv")
    print("   - GET /api/health")
    print("Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

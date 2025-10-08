# EX Financial - Cryptocurrency Exchange Platform

A modern, multilingual cryptocurrency exchange platform with real-time rates and export functionality.

## 🌐 Live Demo

- **Main Site**: https://exfinancialltda.github.io/site/
- **Export Page**: https://exfinancialltda.github.io/site/export.html

## ✨ Features

### 🌍 Multilingual Support
- English (default)
- Russian (Русский)
- Portuguese (Português)
- Spanish (Español)

### 💱 Exchange Features
- Real-time cryptocurrency rates
- Multiple currency support (19 currencies)
- Live rate updates from Binance API
- RUB rates from Fixer API
- Commission system (6% for RUB, 2% for others)

### 📊 Export Functionality
- **Static Rates**: Predefined exchange rates
- **Live Rates**: Real-time rates from APIs
- **Custom Export**: Selected currencies
- **Formats**: XML, JSON, CSV
- **API Endpoints**: REST API for programmatic access

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/exfinancialltda/site.git
cd site

# Start the web server
python3 start_server.py

# Start the API server (optional)
python3 api_server.py
```

### API Usage
```bash
# Static rates in XML
curl "http://localhost:8001/api/rates/static?format=xml"

# Live rates in JSON
curl "http://localhost:8001/api/rates/live?format=json"

# Custom rates in CSV
curl "http://localhost:8001/api/rates/custom?format=csv&currencies=BTC,ETH,USD"
```

## 📁 Project Structure

```
site/
├── index.html              # Main exchange interface
├── export.html             # Export functionality page
├── api_server.py           # REST API server
├── start_server.py         # Web server
├── export_rates_xml.py     # XML export script
├── update_xml_rates.py     # Live rates updater
├── rates_simple.xml        # Simple XML rates
├── live_rates_*.xml        # Live rates XML files
└── .nojekyll              # GitHub Pages configuration
```

## 🔧 Configuration

### API Keys
- **Fixer API**: `3248141d09cae0d63b8636ec094f158b`
- **Binance API**: Public endpoints (no key required)

### Supported Currencies
- **Cryptocurrencies**: BTC, ETH, LTC, TRX, BNB, MATIC, SOL, ADA, DOGE, SHIB, XMR
- **Stablecoins**: USDT, USDC, BUSD
- **Fiat**: USD, EUR, RUB, BRL

## 🌐 GitHub Pages Setup

1. Go to repository Settings
2. Navigate to Pages section
3. Set Source to "Deploy from a branch"
4. Select "main" branch
5. Set folder to "/ (root)"
6. Save settings

The site will be available at: `https://exfinancialltda.github.io/site/`

## 📊 Export Formats

### XML Format
```xml
<?xml version="1.0" encoding="utf-8"?>
<exchange_rates timestamp="2025-10-08T14:12:32" source="EX Financial">
  <metadata>
    <last_updated>2025-10-08 14:12:32</last_updated>
    <total_currencies>19</total_currencies>
    <base_currency>USD</base_currency>
  </metadata>
  <rates>
    <rate currency="Bitcoin BTC" symbol="BTC" rate="0.000023" type="crypto" />
  </rates>
</exchange_rates>
```

### JSON Format
```json
{
  "metadata": {
    "last_updated": "2025-10-08T14:12:32",
    "total_currencies": 19,
    "base_currency": "USD"
  },
  "rates": {
    "Bitcoin BTC": {
      "symbol": "BTC",
      "rate": 0.000023,
      "type": "crypto"
    }
  }
}
```

### CSV Format
```csv
Currency,Symbol,Rate,Type
"Bitcoin BTC","BTC","0.000023","crypto"
"USD Dollar","USD","1.0","fiat"
```

## 🔄 Rate Updates

- **Crypto rates**: Updated every 30 seconds from Binance
- **RUB rates**: Updated every 8 hours from Fixer API
- **Other fiat**: Static rates

## 🛠️ Development

### Adding New Languages
1. Add translations to the `translations` object in `index.html`
2. Add language option to the selector
3. Test language switching

### Adding New Currencies
1. Update `CURRENCY_MAPPING` in `index.html`
2. Add currency to `staticRates` in `export.html`
3. Update API server currency lists

## 📝 License

This project is proprietary software of EX Financial Ltd.

## 📞 Support

- **Email**: support@ex.financial
- **Website**: https://exfinancialltda.github.io/site/

---

**EX Financial** - Professional cryptocurrency exchange platform

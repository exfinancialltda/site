// Многоязычная поддержка для сайта обмена валют
const translations = {
    'pt-BR': {
        // Португальский (Бразилия)
        'title': 'Ex.financial | Câmbio de Criptomoedas',
        'hero_title': 'Câmbio de Criptomoedas',
        'hero_subtitle': 'Taxas premium com liquidação instantânea',
        'exchange_title': 'Câmbio Premium',
        'exchange_subtitle': 'Acesse taxas institucionais sem taxas ocultas',
        'convert_from': 'Você envia',
        'convert_to': 'Você recebe',
        'amount_placeholder': '0.00',
        'execute_exchange': 'Executar Câmbio',
        'live_rates': 'Taxas em Tempo Real',
        'currency_converter': 'Conversor de Moedas',
        'crypto_exchange': 'Câmbio de Criptomoedas',
        'fiat_exchange': 'Câmbio de Moedas Fiat',
        'premium_rates': 'Taxas Premium',
        'instant_settlement': 'Liquidação Instantânea',
        'secure_transaction': 'Transação Segura',
        'how_it_works': 'Como Funciona',
        'step1': 'Verificação Premium',
        'step2': 'Câmbio Executivo',
        'step3': 'Liquidação Instantânea',
        'security_title': 'Segurança de Nível Bancário',
        'start_exchange': 'Iniciar Câmbio',
        'contact_us': 'Entre em Contato',
        'language': 'Idioma'
    },
    'ru': {
        // Русский
        'title': 'Ex.financial | Обмен Криптовалют',
        'hero_title': 'Обмен Криптовалют',
        'hero_subtitle': 'Премиум курсы с мгновенным расчетом',
        'exchange_title': 'Премиум Обмен',
        'exchange_subtitle': 'Получите институциональные курсы без скрытых комиссий',
        'convert_from': 'Вы отправляете',
        'convert_to': 'Вы получаете',
        'amount_placeholder': '0.00',
        'execute_exchange': 'Выполнить Обмен',
        'live_rates': 'Курсы в Реальном Времени',
        'currency_converter': 'Конвертер Валют',
        'crypto_exchange': 'Обмен Криптовалют',
        'fiat_exchange': 'Обмен Фиатных Валют',
        'premium_rates': 'Премиум Курсы',
        'instant_settlement': 'Мгновенный Расчет',
        'secure_transaction': 'Безопасная Сделка',
        'how_it_works': 'Как Это Работает',
        'step1': 'Премиум Верификация',
        'step2': 'Исполнительный Обмен',
        'step3': 'Мгновенный Расчет',
        'security_title': 'Банковский Уровень Безопасности',
        'start_exchange': 'Начать Обмен',
        'contact_us': 'Связаться с Нами',
        'language': 'Язык'
    },
    'en': {
        // Английский
        'title': 'Ex.financial | Cryptocurrency Exchange',
        'hero_title': 'Cryptocurrency Exchange',
        'hero_subtitle': 'Premium rates with instant settlement',
        'exchange_title': 'Premium Exchange',
        'exchange_subtitle': 'Access institutional rates with zero hidden fees',
        'convert_from': 'You Send',
        'convert_to': 'You Receive',
        'amount_placeholder': '0.00',
        'execute_exchange': 'Execute Exchange',
        'live_rates': 'Live Rates',
        'currency_converter': 'Currency Converter',
        'crypto_exchange': 'Cryptocurrency Exchange',
        'fiat_exchange': 'Fiat Currency Exchange',
        'premium_rates': 'Premium Rates',
        'instant_settlement': 'Instant Settlement',
        'secure_transaction': 'Secure Transaction',
        'how_it_works': 'How It Works',
        'step1': 'Premium Verification',
        'step2': 'Executive Exchange',
        'step3': 'Instant Settlement',
        'security_title': 'Bank-Level Security',
        'start_exchange': 'Start Exchange',
        'contact_us': 'Contact Us',
        'language': 'Language'
    },
    'es': {
        // Испанский
        'title': 'Ex.financial | Intercambio de Criptomonedas',
        'hero_title': 'Intercambio de Criptomonedas',
        'hero_subtitle': 'Tarifas premium con liquidación instantánea',
        'exchange_title': 'Intercambio Premium',
        'exchange_subtitle': 'Accede a tarifas institucionales sin cargos ocultos',
        'convert_from': 'Tú envías',
        'convert_to': 'Tú recibes',
        'amount_placeholder': '0.00',
        'execute_exchange': 'Ejecutar Intercambio',
        'live_rates': 'Tarifas en Tiempo Real',
        'currency_converter': 'Convertidor de Monedas',
        'crypto_exchange': 'Intercambio de Criptomonedas',
        'fiat_exchange': 'Intercambio de Monedas Fiat',
        'premium_rates': 'Tarifas Premium',
        'instant_settlement': 'Liquidación Instantánea',
        'secure_transaction': 'Transacción Segura',
        'how_it_works': 'Cómo Funciona',
        'step1': 'Verificación Premium',
        'step2': 'Intercambio Ejecutivo',
        'step3': 'Liquidación Instantánea',
        'security_title': 'Seguridad de Nivel Bancario',
        'start_exchange': 'Iniciar Intercambio',
        'contact_us': 'Contáctanos',
        'language': 'Idioma'
    }
};

// Функция для изменения языка
function changeLanguage(lang) {
    if (translations[lang]) {
        document.documentElement.lang = lang;
        document.documentElement.setAttribute('data-lang', lang);
        
        // Обновляем все элементы с переводом
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (translations[lang][key]) {
                element.textContent = translations[lang][key];
            }
        });
        
        // Обновляем заголовок страницы
        if (translations[lang]['title']) {
            document.title = translations[lang]['title'];
        }
        
        // Сохраняем выбранный язык
        localStorage.setItem('selectedLanguage', lang);
        
        // Обновляем активный класс в селекторе языка
        document.querySelectorAll('.lang-selector').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-lang="${lang}"]`).classList.add('active');
    }
}

// Инициализация языка при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const savedLang = localStorage.getItem('selectedLanguage') || 'pt-BR';
    changeLanguage(savedLang);
});

#!/usr/bin/env python3
import subprocess
import time
import os
import signal
import sys

def start_api_server():
    """Запускает API сервер"""
    try:
        api_process = subprocess.Popen(['python3', 'simple_api.py'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
        time.sleep(2)  # Даем время API серверу запуститься
        return api_process
    except Exception as e:
        print(f"❌ Ошибка запуска API сервера: {e}")
        return None

def start_web_server():
    """Запускает веб сервер"""
    try:
        web_process = subprocess.Popen(['python3', 'start_server.py'],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        return web_process
    except Exception as e:
        print(f"❌ Ошибка запуска веб сервера: {e}")
        return None

def signal_handler(sig, frame):
    """Обработчик сигнала для корректного завершения"""
    print("\n🛑 Остановка серверов...")
    if 'api_process' in globals() and api_process:
        api_process.terminate()
    if 'web_process' in globals() and web_process:
        web_process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚀 Запуск серверов...")
    
    # Запускаем API сервер
    api_process = start_api_server()
    if not api_process:
        print("❌ Не удалось запустить API сервер")
        sys.exit(1)
    
    # Запускаем веб сервер
    web_process = start_web_server()
    if not web_process:
        print("❌ Не удалось запустить веб сервер")
        api_process.terminate()
        sys.exit(1)
    
    print("✅ Серверы запущены:")
    print("   🌐 Веб сервер: http://localhost:8000")
    print("   📊 API сервер: http://localhost:8001")
    print("   📄 Экспорт: http://localhost:8000/export.html")
    print("\nНажмите Ctrl+C для остановки")
    
    try:
        # Ждем завершения процессов
        web_process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

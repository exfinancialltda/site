#!/usr/bin/env python3
import http.server
import socketserver
import os

# Переходим в директорию скрипта
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Сервер запущен на http://localhost:{PORT}")
    print(f"Текущая директория: {os.getcwd()}")
    print("Нажмите Ctrl+C для остановки")
    httpd.serve_forever()

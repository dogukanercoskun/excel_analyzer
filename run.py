#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Excel Veri Analiz Aracı

Bu betik, Excel Veri Analiz Web Uygulamasını başlatır.
Kullanıcıların Excel dosyalarını yükleyip analiz etmelerine,
veri görselleştirme yapmalarına ve sonuçları dışa aktarmalarına olanak tanır.
"""

import os
import webbrowser
from threading import Timer
from app import app

def open_browser():
    """
    Varsayılan web tarayıcısında uygulamayı açar.
    """
    webbrowser.open_new('http://127.0.0.1:5000/')

def main():
    """
    Ana uygulama başlatma fonksiyonu.
    """
    # uploads klasörünün var olduğundan emin ol
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print(f"'uploads' klasörü oluşturuldu: {os.path.abspath('uploads')}")
    else:
        print(f"'uploads' klasörü mevcut: {os.path.abspath('uploads')}")
        print(f"Yazma izni: {os.access('uploads', os.W_OK)}")
    
    # flask_session klasörünün var olduğundan emin ol
    if not os.path.exists('flask_session'):
        os.makedirs('flask_session')
        print(f"'flask_session' klasörü oluşturuldu: {os.path.abspath('flask_session')}")
    else:
        print(f"'flask_session' klasörü mevcut: {os.path.abspath('flask_session')}")
    
    # Kütüphane kontrolü
    try:
        import flask_wtf
        print("Flask-WTF başarıyla yüklendi!")
    except ImportError:
        print("\n⚠️  UYARI: Flask-WTF kütüphanesi yüklenemedi!")
        print("Lütfen 'pip install flask-wtf' komutunu çalıştırın.\n")
    
    try:
        from flask_session import Session
        print("Flask-Session başarıyla yüklendi!")
    except ImportError:
        print("\n⚠️  UYARI: Flask-Session kütüphanesi yüklenemedi!")
        print("Lütfen 'pip install flask-session' komutunu çalıştırın.\n")
    
    print("\n" + "-"*50)
    print("Excel Veri Analiz Uygulaması başlatılıyor...")
    print("Uygulama adresini tarayıcınızda açmak için: http://127.0.0.1:5000")
    print("-"*50 + "\n")
    
    # Tarayıcıyı aç
    Timer(1, open_browser).start()
    
    # Flask uygulamasını başlat
    # Debug modu açık ve threaded mod açık
    app.run(debug=True, threaded=True, host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()

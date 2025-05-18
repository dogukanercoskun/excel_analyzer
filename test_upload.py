# test_upload.py - Excel Analyzer için basit bir test scripti

import os
import requests
from bs4 import BeautifulSoup
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_file_upload():
    """
    Dosya yükleme işlevini test eder.
    """
    # Flask uygulamasının çalıştığını varsayalım
    base_url = "http://127.0.0.1:5000"
    
    # Örnek Excel dosyasının yolunu belirle
    sample_file_path = "Scale.xlsx"  # Bu dosyanın var olduğundan emin olun
    
    if not os.path.exists(sample_file_path):
        logging.error(f"Test dosyası bulunamadı: {sample_file_path}")
        return False
    
    # Ana sayfayı yükle ve CSRF token al
    try:
        session = requests.Session()
        logging.info(f"Ana sayfaya istek gönderiliyor: {base_url}")
        response = session.get(base_url)
        
        if response.status_code != 200:
            logging.error(f"Ana sayfa yüklenemedi. Durum Kodu: {response.status_code}")
            return False
        
        # CSRF token'ı çıkart (eğer varsa)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        
        csrf_token = None
        if csrf_input:
            csrf_token = csrf_input.get('value')
            logging.info(f"CSRF token bulundu: {csrf_token}")
        else:
            logging.warning("CSRF token bulunamadı. Flask-WTF muhtemelen yapılandırılmamış.")
        
        # Dosyayı yükle
        upload_url = f"{base_url}/upload"
        logging.info(f"Dosya yükleniyor: {sample_file_path} -> {upload_url}")
        
        with open(sample_file_path, 'rb') as f:
            files = {'file': (os.path.basename(sample_file_path), f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            
            data = {}
            if csrf_token:
                data['csrf_token'] = csrf_token
            
            response = session.post(upload_url, files=files, data=data, allow_redirects=False)
        
        if response.status_code == 302:  # Redirect
            logging.info(f"Dosya başarıyla yüklendi! Yönlendirme: {response.headers.get('Location')}")
            # Yönlendirme sayfasını kontrol et
            redirect_url = response.headers.get('Location')
            if redirect_url.startswith('/'):
                redirect_url = base_url + redirect_url
            
            logging.info(f"Yönlendirme sayfasına erişiliyor: {redirect_url}")
            redirect_response = session.get(redirect_url)
            
            if redirect_response.status_code == 200:
                logging.info("Yönlendirme sayfası başarıyla yüklendi.")
                return True
            else:
                logging.error(f"Yönlendirme sayfası yüklenemedi. Durum Kodu: {redirect_response.status_code}")
                return False
        else:
            logging.error(f"Dosya yükleme başarısız. Durum Kodu: {response.status_code}")
            logging.error(f"Yanıt: {response.text}")
            return False
            
    except Exception as e:
        logging.error(f"Test sırasında hata oluştu: {str(e)}")
        return False

if __name__ == "__main__":
    logging.info("Excel Analyzer Dosya Yükleme Testi başlatılıyor...")
    success = test_file_upload()
    
    if success:
        logging.info("✅ TEST BAŞARILI: Dosya yükleme işlemi çalışıyor!")
    else:
        logging.error("❌ TEST BAŞARISIZ: Dosya yükleme işleminde sorun var.")

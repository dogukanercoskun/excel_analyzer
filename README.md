# Excel Veri Analiz Aracı
Excel dosyalarını yükleyip analiz eden, veri görselleştirme yapan ve sonuçları tablolar ve grafikler şeklinde sunan web tabanlı bir analiz uygulaması.

Özellikler
Excel Dosyası Yükleme: Kullanıcılar .xlsx, .xls ve .csv formatındaki dosyaları sürükle-bırak veya dosya seçici ile yükleyebilir.

Veri Doğrulama: Yüklenen dosyalar otomatik olarak işlenir ve veri hakkında temel bilgiler (satır sayısı, sütun sayısı, eksik değerler vb.) gösterilir.

Veri Anlamlandırma: Kullanıcılar sütunları tanımlayabilir, açıklamalar ekleyebilir ve veri türleri hakkında bilgi sağlayabilir.

Çeşitli Analiz Seçenekleri:

Özet İstatistikler (Ortalama, medyan, standart sapma vb.)
Korelasyon Analizi
Zaman Serisi Analizi
Kategorik Veri Analizi
Dağılım Analizi
Dağılım Grafiği
Görselleştirme: Veriler çeşitli grafik türleriyle görselleştirilir (çubuk, pasta, çizgi, ısı haritası, histogram, kutu grafiği, dağılım grafiği).

Rapor Oluşturma: Tüm analiz sonuçları PDF, Excel veya CSV formatlarında dışa aktarılabilir.

Kurulum
Gereksinimler
Python 3.9+
Pip (Python paket yöneticisi)
Adımlar
Projeyi klonlayın veya dosyaları indirin:
git clone https://github.com/kullanici/excel_analyzer.git
cd excel_analyzer
Sanal ortam oluşturun (opsiyonel ama önerilir):
python -m venv venv
Sanal ortamı etkinleştirin:
Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate
Gerekli paketleri yükleyin:
pip install -r requirements.txt
Uygulamayı başlatın:
python app.py
Tarayıcınızda uygulama adresine gidin:
http://127.0.0.1:5000
=======
# Excel Veri Analiz Web Uygulaması

Bu web uygulaması, Excel dosyalarını yükleyip analiz etmenizi, veri görselleştirme yapmanızı ve sonuçları tablolar ve grafikler şeklinde sunmanızı sağlar.

## Özellikler

- Excel dosyalarını sürükle-bırak veya dosya seçici ile yükleme (.xlsx, .xls, .csv)
- Veri doğrulama ve ön işleme
- Veri anlamlandırma ve açıklama ekleme
- Çeşitli analiz seçenekleri:
  - Temel istatistikler (ortalama, medyan, mod, standart sapma, vb.)
  - Korelasyon analizi
  - Zaman serisi analizi
  - Kategorik veri analizi
  - Dağılım analizi
- İnteraktif grafikler ve görselleştirmeler
- Analiz sonuçlarını dışa aktarma

## Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/KULLANICIADI/excel-analyzer.git
cd excel-analyzer

# Sanal ortam oluşturun ve etkinleştirin
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python run.py
Not: NumPy uyumsuzluk hatasıyla karşılaşırsanız, şu komutu çalıştırın:

pip install "numpy<2.0.0"
>>>>>>> a1ef2a0 (ikinci commit: Excel veri analiz web uygulaması)
Kullanım
<<<<<<< HEAD

Ana sayfada "Dosya Seçin" butonuna tıklayın veya dosyanızı sürükleyip bırakın.
Yüklenen dosyanın bilgilerini kontrol edin ve devam etmek için "İleri" butonuna tıklayın.
Verilerinizin sütunları hakkında ek bilgiler girin ve "Bilgileri Kaydet" butonuna tıklayın.
İstediğiniz analiz türlerini seçin ve parametreleri belirleyin.
"Tüm Analiz Sonuçlarını Görüntüle" butonuna tıklayarak sonuçları görüntüleyin.
Sonuçları PDF, Excel veya CSV formatında indirmek için "Raporu İndir" butonunu kullanın.
Desteklenen Dosya Formatları
Excel (.xlsx, .xls)
CSV (.csv) - Çeşitli ayraç türleri desteklenir (virgül, noktalı virgül)
Veri Limitleri
Maksimum dosya boyutu: 16 MB
Desteklenen maksimum satır sayısı: Sınırsız (sistem belleği ile sınırlıdır)
Katkıda Bulunma
Katkıda bulunmak için:

Bu depoyu forklayın
Yeni bir dal oluşturun (git checkout -b yeni-ozellik)
Değişikliklerinizi commit edin (git commit -am 'Yeni özellik: açıklama')
Dalınızı push edin (git push origin yeni-ozellik)
Bir Pull Request açın
Lisans
Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakın.

İletişim
Sorularınız için: ornek@email.com
Ana sayfada "Dosya Seç" düğmesine tıklayın veya bir Excel dosyasını sürükleyip bırakın
Verileriniz yüklendikten sonra, önce veriyi doğrulayın
Sütunlar hakkında açıklamalar ve anlamlandırmalar ekleyin
Yapmak istediğiniz analiz türlerini seçin
Sonuçlarınızı görüntüleyin ve dışa aktarın
Katkıda Bulunma
Katkıda bulunmak istiyorsanız, lütfen bir "pull request" açın veya önerileriniz için bir "issue" oluşturun.

Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.

a1ef2a0 (ikinci commit: Excel veri analiz web uygulaması)
# Excel Veri Analiz Aracı

Excel dosyalarını yükleyip analiz eden, veri görselleştirme yapan ve sonuçları tablolar ve grafikler şeklinde sunan web tabanlı bir analiz uygulaması.

## Özellikler

- **Excel Dosyası Yükleme**: Kullanıcılar .xlsx, .xls ve .csv formatındaki dosyaları sürükle-bırak veya dosya seçici ile yükleyebilir.

- **Veri Doğrulama**: Yüklenen dosyalar otomatik olarak işlenir ve veri hakkında temel bilgiler (satır sayısı, sütun sayısı, eksik değerler vb.) gösterilir.

- **Veri Anlamlandırma**: Kullanıcılar sütunları tanımlayabilir, açıklamalar ekleyebilir ve veri türleri hakkında bilgi sağlayabilir.

- **Çeşitli Analiz Seçenekleri**:
  - Özet İstatistikler (Ortalama, medyan, standart sapma vb.)
  - Korelasyon Analizi
  - Zaman Serisi Analizi
  - Kategorik Veri Analizi
  - Dağılım Analizi
  - Dağılım Grafiği

- **Görselleştirme**: Veriler çeşitli grafik türleriyle görselleştirilir (çubuk, pasta, çizgi, ısı haritası, histogram, kutu grafiği, dağılım grafiği).

- **Rapor Oluşturma**: Tüm analiz sonuçları PDF, Excel veya CSV formatlarında dışa aktarılabilir.

## Kurulum

### Gereksinimler

- Python 3.9+
- Pip (Python paket yöneticisi)

### Adımlar

1. Projeyi klonlayın veya dosyaları indirin:

```bash
git clone https://github.com/kullanici/excel_analyzer.git
cd excel_analyzer
```

2. Sanal ortam oluşturun (opsiyonel ama önerilir):

```bash
python -m venv venv
```

3. Sanal ortamı etkinleştirin:

- Windows:
```bash
venv\Scripts\activate
```

- macOS/Linux:
```bash
source venv/bin/activate
```

4. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

5. Uygulamayı başlatın:

```bash
python app.py
```

6. Tarayıcınızda uygulama adresine gidin:

```
http://127.0.0.1:5000
```

## Kullanım

1. Ana sayfada "Dosya Seçin" butonuna tıklayın veya dosyanızı sürükleyip bırakın.
2. Yüklenen dosyanın bilgilerini kontrol edin ve devam etmek için "İleri" butonuna tıklayın.
3. Verilerinizin sütunları hakkında ek bilgiler girin ve "Bilgileri Kaydet" butonuna tıklayın.
4. İstediğiniz analiz türlerini seçin ve parametreleri belirleyin.
5. "Tüm Analiz Sonuçlarını Görüntüle" butonuna tıklayarak sonuçları görüntüleyin.
6. Sonuçları PDF, Excel veya CSV formatında indirmek için "Raporu İndir" butonunu kullanın.

## Desteklenen Dosya Formatları

- Excel (.xlsx, .xls)
- CSV (.csv) - Çeşitli ayraç türleri desteklenir (virgül, noktalı virgül)

## Veri Limitleri

- Maksimum dosya boyutu: 16 MB
- Desteklenen maksimum satır sayısı: Sınırsız (sistem belleği ile sınırlıdır)

## Katkıda Bulunma

Katkıda bulunmak için:

1. Bu depoyu forklayın
2. Yeni bir dal oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: açıklama'`)
4. Dalınızı push edin (`git push origin yeni-ozellik`)
5. Bir Pull Request açın

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

Sorularınız için: [ornek@email.com](mailto:ornek@email.com)

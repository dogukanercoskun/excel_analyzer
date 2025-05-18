import os
import uuid
import logging
import io
import base64
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_file
from werkzeug.utils import secure_filename
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

# Loglama ayarı
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Uygulama oluşturma
app = Flask(__name__)
app.secret_key = 'EXCEL_ANALYZER_SECRET_KEY_2024'  # Sabit bir secret key kullanalim

# CSRF korumasını etkinleştir - bazı route'lar için devre dışı bırakılacak
csrf = CSRFProtect()
csrf.init_app(app)

# CSRF korumasını bazı rotalar için devre dışı bırakalım
@csrf.exempt
def csrf_exempt(view):
    """View decorator that exempts a view from CSRF protection."""
    view.csrf_exempt = True
    return view

# Flask session ayarları
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 dakika
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 saat

# Session cookie adını açıkça tanımla (Flask 2.3+ için gerekli)
app.config['SESSION_COOKIE_NAME'] = 'excel_analyzer_session'

# Session uygulamasini başlat
sess = Session(app)

# Yükleme dizini için yapılandırma
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB max

# Debug bilgileri
logging.info(f"Upload folder: {UPLOAD_FOLDER}")
logging.info(f"Upload folder exists: {os.path.exists(UPLOAD_FOLDER)}")
logging.info(f"Upload folder is absolute: {os.path.isabs(UPLOAD_FOLDER)}")
logging.info(f"Allowed extensions: {ALLOWED_EXTENSIONS}")
logging.info(f"Max content length: {app.config['MAX_CONTENT_LENGTH']/1024/1024} MB")

# Uploads klasörünü oluştur
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# Dosya uzantısı kontrolü
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ana sayfa
@app.route('/')
def index():
    # Kütüphane kontrolü
    try:
        import flask_wtf
        logging.info("Flask-WTF başarıyla yüklendi.")
    except ImportError:
        logging.error("Flask-WTF yüklenmemiş! Formlar düzgün çalışmayabilir.")
    
    # Session çalışıyor mu kontrol et
    session['test'] = 'test_value'
    logging.info(f"Session test: {session.get('test')}")
    
    # Uploads klasörü kontrolü
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        logging.info(f"Uploads klasörü oluşturuldu: {app.config['UPLOAD_FOLDER']}")
    else:
        logging.info(f"Uploads klasörü mevcut: {app.config['UPLOAD_FOLDER']}")
        logging.info(f"Uploads klasörü yazma izni: {os.access(app.config['UPLOAD_FOLDER'], os.W_OK)}")
    
    return render_template('index.html')

# Dosya yükleme
@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info("Upload route çağrıldı")
    logging.info(f"Request method: {request.method}")
    
    # Form bilgilerini görüntüle
    logging.info(f"Form keys: {request.form.keys()}")
    
    # Dosya bilgilerini görüntüle 
    logging.info(f"Files keys: {request.files.keys()}")
    
    # CSRF kontrolü
    csrf_token = request.form.get('csrf_token')
    logging.info(f"CSRF token present: {csrf_token is not None}")
    
    if 'file' not in request.files:
        logging.error("'file' anahtarı request.files içinde bulunamadı")
        flash('Dosya bulunamadı', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    logging.info(f"Yüklenen dosya adı: {file.filename}")
    
    if file.filename == '':
        logging.error("Dosya adı boş")
        flash('Dosya seçilmedi', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        logging.error(f"Desteklenmeyen dosya formatı: {file.filename}")
        flash('İzin verilen dosya formatları: xlsx, xls, csv', 'error')
        return redirect(url_for('index'))
    
    try:
        # Güvenli dosya adı oluştur
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        unique_filename = f"{unique_id}_{filename}"
        
        # Uploads klasörünün var olduğundan emin ol
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Tam dosya yolu
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        logging.info(f"Dosya yolu: {filepath}")
        
        # Dosyayı kaydet
        file.save(filepath)
        logging.info(f"Dosya başarıyla kaydedildi: {filepath}")
        
        # Dosyanın var olduğunu kontrol et
        if not os.path.exists(filepath):
            logging.error(f"Dosya kaydedilmedi: {filepath}")
            flash('Dosya kaydedilemedi', 'error')
            return redirect(url_for('index'))
        
        logging.info(f"Dosya boyutu: {os.path.getsize(filepath)} bytes")
        
        # Dosyayı işle ve istatistikleri al
        try:
            file_stats = process_file(filepath)
            logging.info("Dosya başarıyla işlendi")
            
            # Session'a bilgileri kaydet
            session['filepath'] = filepath
            session['file_stats'] = file_stats
            logging.info("Session bilgileri kaydedildi")
            
            return redirect(url_for('validate_data'))
        except Exception as e:
            logging.exception(f"Dosya işleme hatası: {str(e)}")
            flash(f'Dosya işlenirken hata oluştu: {str(e)}', 'error')
            return redirect(url_for('index'))
        
    except Exception as e:
        logging.exception(f"Dosya yükleme hatası: {str(e)}")
        flash(f'Dosya yükleme hatası: {str(e)}', 'error')
        return redirect(url_for('index'))

# Dosya işleme fonksiyonu
def process_file(filepath):
    # Gerekli kütüphaneleri burada import et
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as e:
        logging.error(f"Kütüphane import edilemedi: {str(e)}")
        raise Exception(f"Gerekli kütüphaneler yüklenemedi: {str(e)}")

    file_extension = filepath.rsplit('.', 1)[1].lower()
    
    try:
        if file_extension == 'csv':
            # CSV dosyası için farklı ayraçları dene
            try:
                df = pd.read_csv(filepath, encoding='utf-8')
            except Exception:
                try:
                    df = pd.read_csv(filepath, encoding='latin1')
                except Exception:
                    try:
                        df = pd.read_csv(filepath, sep=';', encoding='utf-8')
                    except Exception:
                        df = pd.read_csv(filepath, sep=';', encoding='latin1')
        else:
            # Excel dosyası
            df = pd.read_excel(filepath, engine='openpyxl')
        
        # Temel istatistikleri hesapla
        stats = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': list(df.columns),
            'column_types': {col: str(df[col].dtype) for col in df.columns},
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percent': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            'sample_data': df.head(5).to_dict(orient='records')
        }
        
        # Veri türlerine göre ek istatistikler
        numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        date_columns = []
        
        # Tarih sütunlarını tespit et
        for col in df.columns:
            try:
                if df[col].dtype == 'object':
                    pd.to_datetime(df[col])
                    date_columns.append(col)
            except Exception:
                pass
        
        stats['numerical_columns'] = numerical_columns
        stats['categorical_columns'] = categorical_columns
        stats['date_columns'] = date_columns
        
        # Sayısal sütunlar için istatistikler
        if numerical_columns:
            stats['numerical_stats'] = df[numerical_columns].describe().to_dict()
        
        # Kategorik sütunlar için istatistikler
        if categorical_columns:
            cat_stats = {}
            for col in categorical_columns:
                value_counts = df[col].value_counts().head(10).to_dict()
                cat_stats[col] = {
                    'unique_count': df[col].nunique(),
                    'top_values': value_counts
                }
            stats['categorical_stats'] = cat_stats
        
        return stats
    except Exception as e:
        logging.exception(f"Dosya işleme hatası: {str(e)}")
        raise Exception(f"Dosya işlenirken hata oluştu: {str(e)}")

# Veri doğrulama sayfası
@app.route('/validate_data')
def validate_data():
    if 'file_stats' not in session:
        flash('Önce bir dosya yükleyin', 'error')
        return redirect(url_for('index'))
    
    return render_template('validate_data.html', stats=session['file_stats'])

# Veri anlamlandırma sayfası
@app.route('/understand_data', methods=['POST'])
def understand_data():
    if 'filepath' not in session:
        flash('Dosya bilgisi bulunamadı', 'error')
        return redirect(url_for('index'))
    
    # Doğrulama işlemi başarılı, veri anlamlandırma sayfasına yönlendir
    return render_template('understand_data.html', stats=session['file_stats'])

# Sütun bilgileri güncelleme
@app.route('/update_column_info', methods=['POST'])
@csrf_exempt
def update_column_info():
    if 'file_stats' not in session:
        return jsonify({"error": "Oturum bilgisi bulunamadı"}), 400
    
    data = request.json
    column_info = data.get('column_info', {})
    
    # Sütun bilgilerini session'da güncelle
    if 'column_metadata' not in session:
        session['column_metadata'] = {}
    
    session['column_metadata'].update(column_info)
    
    return jsonify({"status": "success"}), 200

# Analiz seçenekleri sayfası
@app.route('/select_analysis', methods=['POST'])
def select_analysis():
    if 'file_stats' not in session:
        flash('Veri bilgisi bulunamadı', 'error')
        return redirect(url_for('index'))
    
    # Veri anlamlandırma işlemi başarılı, analiz seçenekleri sayfasına yönlendir
    return render_template('select_analysis.html', 
                          stats=session['file_stats'],
                          metadata=session.get('column_metadata', {}))

# Analiz yapma
@app.route('/perform_analysis', methods=['POST'])
@csrf_exempt
def perform_analysis():
    if 'filepath' not in session:
        return jsonify({"error": "Dosya bilgisi bulunamadı"}), 400
    
    # Gerekli kütüphaneleri burada import et
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as e:
        logging.error(f"Kütüphane import edilemedi: {str(e)}")
        return jsonify({"error": f"Gerekli kütüphaneler yüklenemedi: {str(e)}"}), 500
    
    data = request.json
    analysis_type = data.get('analysis_type')
    columns = data.get('columns', [])
    
    # Dosyayı yeniden yükle
    filepath = session['filepath']
    file_extension = filepath.rsplit('.', 1)[1].lower()
    
    try:
        if file_extension == 'csv':
            try:
                df = pd.read_csv(filepath, encoding='utf-8')
            except:
                try:
                    df = pd.read_csv(filepath, encoding='latin1')
                except:
                    try:
                        df = pd.read_csv(filepath, sep=';', encoding='utf-8')
                    except:
                        df = pd.read_csv(filepath, sep=';', encoding='latin1')
        else:
            df = pd.read_excel(filepath)
    except Exception as e:
        logging.error(f"Dosya okuma hatası: {str(e)}")
        return jsonify({"error": f"Dosya okunamadı: {str(e)}"}), 500
    
    # Analiz türüne göre işlem yap
    result = {}
    
    if analysis_type == 'summary_stats':
        if columns:
            result = df[columns].describe().to_dict()
        else:
            result = {"error": "Sütun seçilmedi"}
    
    elif analysis_type == 'correlation':
        if len(columns) >= 2:
            corr = df[columns].corr().to_dict()
            result = corr
            
            # Korelasyon grafiği
            plt.figure(figsize=(10, 8))
            import seaborn as sns
            corr_matrix = df[columns].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
            
            # Base64 ile grafik encode et
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            
            result['heatmap'] = img_str
        else:
            result = {"error": "Korelasyon için en az 2 sütun seçilmelidir"}
    
    elif analysis_type == 'time_series':
        if len(columns) >= 2 and columns[0] in session['file_stats']['date_columns']:
            # Tarih sütunu ve diğer sütunlar
            date_col = columns[0]
            value_cols = columns[1:]
            
            # Tarihe göre sırala
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.sort_values(by=date_col)
            
            # Her değer sütunu için çizgi grafik
            plt.figure(figsize=(12, 6))
            
            for col in value_cols:
                plt.plot(df[date_col], df[col], marker='o', linestyle='-', label=col)
            
            plt.title(f'{", ".join(value_cols)} değerlerinin zaman içindeki değişimi')
            plt.xlabel(date_col)
            plt.ylabel('Değer')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Base64 ile grafik encode et
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            
            result['time_series_plot'] = img_str
            
            # Özet istatistikler
            result['summary'] = df[value_cols].describe().to_dict()
        else:
            result = {"error": "Zaman serisi analizi için bir tarih sütunu ve en az bir değer sütunu seçilmelidir"}
    
    elif analysis_type == 'categorical':
        if len(columns) >= 1:
            cat_col = columns[0]
            cat_counts = df[cat_col].value_counts().head(10)
            
            # Pasta grafik
            plt.figure(figsize=(10, 8))
            plt.pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', shadow=True)
            plt.title(f'{cat_col} için Kategori Dağılımı')
            plt.axis('equal')  # Daire şeklinde olmasını sağlar
            
            # Base64 ile grafik encode et
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.read()).decode('utf-8')
            
            result['pie_chart'] = img_str
            result['value_counts'] = cat_counts.to_dict()
            
            # İkinci sütun seçilmişse çapraz tablo oluştur
            if len(columns) >= 2:
                cat_col2 = columns[1]
                cross_tab = pd.crosstab(df[cat_col], df[cat_col2])
                result['cross_tab'] = cross_tab.to_dict()
                
                # Çubuk grafik
                plt.figure(figsize=(12, 8))
                cross_tab.plot(kind='bar', stacked=True)
                plt.title(f'{cat_col} ve {cat_col2} arasındaki ilişki')
                plt.xlabel(cat_col)
                plt.ylabel('Sayı')
                plt.xticks(rotation=45)
                plt.legend(title=cat_col2)
                plt.tight_layout()
                
                # Base64 ile grafik encode et
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                img_str = base64.b64encode(buffer.read()).decode('utf-8')
                
                result['bar_chart'] = img_str
        else:
            result = {"error": "Kategorik analiz için en az bir sütun seçilmelidir"}
    
    elif analysis_type == 'distribution':
        if len(columns) >= 1:
            # Her sayısal sütun için histogram
            for col in columns:
                if col in session['file_stats']['numerical_columns']:
                    plt.figure(figsize=(10, 6))
                    plt.hist(df[col].dropna(), bins=30, alpha=0.7, color='blue', edgecolor='black')
                    plt.title(f'{col} için Dağılım Histogramı')
                    plt.xlabel(col)
                    plt.ylabel('Frekans')
                    plt.grid(True, alpha=0.3)
                    
                    # Ortalama ve medyan çizgileri
                    plt.axvline(df[col].mean(), color='red', linestyle='dashed', linewidth=2, label=f'Ortalama: {df[col].mean():.2f}')
                    plt.axvline(df[col].median(), color='green', linestyle='dashed', linewidth=2, label=f'Medyan: {df[col].median():.2f}')
                    plt.legend()
                    
                    # Base64 ile grafik encode et
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    
                    if 'histograms' not in result:
                        result['histograms'] = {}
                    
                    result['histograms'][col] = img_str
                    
                    # Kutu grafiği
                    plt.figure(figsize=(10, 6))
                    plt.boxplot(df[col].dropna(), vert=False)
                    plt.title(f'{col} için Kutu Grafiği')
                    plt.xlabel(col)
                    plt.grid(True, alpha=0.3)
                    
                    # Base64 ile grafik encode et
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    img_str = base64.b64encode(buffer.read()).decode('utf-8')
                    
                    if 'boxplots' not in result:
                        result['boxplots'] = {}
                    
                    result['boxplots'][col] = img_str
        else:
            result = {"error": "Dağılım analizi için en az bir sayısal sütun seçilmelidir"}
    
    elif analysis_type == 'scatter':
        if len(columns) >= 2:
            x_col = columns[0]
            y_col = columns[1]
            
            if x_col in session['file_stats']['numerical_columns'] and y_col in session['file_stats']['numerical_columns']:
                plt.figure(figsize=(10, 8))
                plt.scatter(df[x_col], df[y_col], alpha=0.5)
                plt.title(f'{x_col} ve {y_col} arasındaki ilişki')
                plt.xlabel(x_col)
                plt.ylabel(y_col)
                plt.grid(True, alpha=0.3)
                
                # Eğilim çizgisi
                z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
                p = np.poly1d(z)
                plt.plot(df[x_col].dropna(), p(df[x_col].dropna()), "r--", alpha=0.8)
                
                # Base64 ile grafik encode et
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                img_str = base64.b64encode(buffer.read()).decode('utf-8')
                
                result['scatter_plot'] = img_str
                
                # Korelasyon değeri
                result['correlation'] = df[[x_col, y_col]].corr().iloc[0, 1]
            else:
                result = {"error": "Dağılım grafiği için sayısal sütunlar seçilmelidir"}
        else:
            result = {"error": "Dağılım grafiği için en az iki sütun seçilmelidir"}
    
    # Analiz sonuçlarını sesssion'a kaydet
    if 'analysis_results' not in session:
        session['analysis_results'] = {}
    
    session['analysis_results'][analysis_type] = result
    
    return jsonify(result)

# Analiz sonuçları sayfası
@app.route('/analysis_results')
def analysis_results():
    if 'analysis_results' not in session:
        flash('Henüz analiz yapılmadı', 'error')
        return redirect(url_for('index'))
    
    return render_template('analysis_results.html', 
                          results=session['analysis_results'],
                          stats=session['file_stats'])

# Raporu dışa aktar
@app.route('/export_report', methods=['POST'])
def export_report():
    if 'analysis_results' not in session:
        flash('Dışa aktarılacak analiz sonucu bulunamadı', 'error')
        return redirect(url_for('index'))
    
    export_type = request.form.get('export_type', 'pdf')
    
    # Burada dışa aktarma işlemi yapılacak
    # Şimdilik bir örnek olarak dosya indirme
    if export_type == 'pdf':
        # PDF oluşturma kodları buraya eklenecek
        # Şimdilik örnek bir PDF dosyası
        return send_file(session['filepath'], as_attachment=True, download_name='analysis_report.pdf')
    elif export_type == 'excel':
        # Excel oluşturma kodları buraya eklenecek
        return send_file(session['filepath'], as_attachment=True, download_name='analysis_report.xlsx')
    elif export_type == 'csv':
        # CSV oluşturma kodları buraya eklenecek
        return send_file(session['filepath'], as_attachment=True, download_name='analysis_report.csv')
    else:
        flash('Desteklenmeyen dışa aktarma formatı', 'error')
        return redirect(url_for('analysis_results'))

# Yeni analiz başlat
@app.route('/new_analysis')
def new_analysis():
    # Oturum verilerini temizle
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # uploads klasörünün var olduğundan emin ol
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    app.run(debug=True)
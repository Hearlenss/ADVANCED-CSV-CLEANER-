#  ANKA TEAM – Advanced CSV Cleaner v2.3

Schema-Agnostic • Automatic • Secure Data Cleaning Tool

ANKA CSV Cleaner; farklı kaynaklardan gelen, başlıkları ve yapısı uyuşmayan
CSV dosyalarını **otomatik algılayıp temizleyen** gelişmiş bir Python aracıdır.

---

## Özellikler

- **Schema-Agnostic Engine**
  - CSV başlıkları farklı olsa bile otomatik kolon algılama
- **Akıllı Alan Eşleştirme**
  - name, email, phone, cnic, qualification, fathername, address, center vb.
- **Normalize Alanlar**
  - `normalized_name`
  - `normalized_email`
  - `normalized_phone`
  - `normalized_title`
  - `normalized_date`
- **Multi-CSV Desteği**
  - Birden fazla CSV dosyasını **ayrı ayrı** işler (birleştirme yok)
- **Duplicate Temizleme**
  - İsim + email / telefon bazlı tekrar kontrolü
- **URL & Veri Sanitization**
  - Bozuk linkler otomatik temizlenir
- **Otomatik Çıktı İsimlendirme**
  - `example.csv` →
    - `example_clean.csv`
    - `example_clean.json`
    - `example_clean.xlsx`
    - `example_clean.log`
- **CSV + JSON + Excel Çıktısı**

---

## 📂 Otomatik Algılanan Alanlar

- name
- email
- cell / phone / mobile
- cnic
- id
- fathername
- address
- location
- center
- domicile
- qualification
- title
- date / year

> CSV dosyasının **ilk satırı ne olursa olsun**, sistem otomatik algılar.

---

##  Nasıl Çalışır?

1. CSV başlıklarını analiz eder  
2. Alias mantığıyla kolonları eşleştirir  
3. Email / telefon / tarih doğrulaması yapar  
4. Duplicate kayıtları ayıklar  
5. Normalize alanları ekler  
6. Temiz veriyi ayrı dosyalara yazar  

---

##  Kurulum

Python 3.8+


pip install openpyxl
Diğer tüm kütüphaneler Python ile birlikte gelir.

 Kullanım
bash
Kodu kopyala
python anka_csv_cleaner.py
Birden fazla dosya için:

text
Kodu kopyala
file1.csv, file2.csv, file3.csv
Neden ANKA CSV Cleaner?
Manuel Excel temizleme yok

Kolon uyumsuzluğu derdi yok

Veri kaybı riski yok

OSINT & Pentest uyumlu

Büyük ve kirli dataset’ler için ideal

Yol Haritası
Büyük dosyalar için stream processing

Config tabanlı alias yönetimi

GUI sürüm (opsiyonel)

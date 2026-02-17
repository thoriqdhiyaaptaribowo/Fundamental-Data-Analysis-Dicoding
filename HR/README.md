# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Maju merupakan salah satu perusahaan multinasional yang telah berdiri sejak tahun 2000. Ia memiliki lebih dari 1000 karyawan yang tersebar di seluruh penjuru negeri. 

Walaupun telah menjadi menjadi perusahaan yang cukup besar, Jaya Jaya Maju masih cukup kesulitan dalam mengelola karyawan. Hal ini berimbas tingginya attrition rate (rasio jumlah karyawan yang keluar dengan total karyawan keseluruhan) hingga lebih dari 10%.

Untuk mencegah hal ini semakin parah, manajer departemen HR ingin meminta bantuan Anda mengidentifikasi berbagai faktor yang mempengaruhi tingginya attrition rate tersebut. Selain itu, ia juga meminta Anda untuk membuat business dashboard untuk membantunya memonitori berbagai faktor tersebut. Selain itu, mereka juga telah menyediakan dataset yang dapat Anda unduh melalui tautan berikut: Jaya Jaya Maju.

### Permasalahan Bisnis

1. Faktor-faktor apa sajakah yang paling signifikan mempengaruhi keputusan pekerja untuk meninggalkan perusahaan?
2. Strategi retensi karyawan apa saja yang dapat diimplementasikan perusahaan untuk mengurangi tingkat atrisi dan meningkatkan durabilitas tenaga kerja?

### Cakupan Proyek

Cakupan dari proyek ini adalah untuk mencari informasi terkait faktor-faktor yang mempengaruhi atrisi pekerja dengan melakukan serta mengetahui tindakan apa yang dapat dilakukan untuk mempertahankan karyawannya dengan melakukan analisis korelasi dan membuat model machine learning

### Persiapan

Sumber data: 'employee_data.csv'

Setup environment:

Disarankan menggunakan Python 3.10 atau lebih baru. Ikuti langkah berikut untuk menyiapkan lingkungan pengembangan:

1. Buat dan aktifkan virtual environment (menggunakan venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Atau jika menggunakan conda:

```bash
conda create -n hr-env python=3.10 -y
conda activate hr-env
```

2. Perbarui pip dan instal dependensi:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. (Opsional) Untuk membuka notebook interaktif:

```bash
pip install jupyterlab   # atau pip install notebook
jupyter lab             # atau jupyter notebook
```

4. Menjalankan skrip inference atau analisis:

```bash
python inference.py
# atau buka `notebook.ipynb` di Jupyter untuk eksplorasi interaktif
```

Catatan:
- Pastikan file dataset (`employee_data.csv`) berada pada direktori yang sesuai (sama dengan repository), atau sesuaikan path di dalam skrip/notebook.
- Jika mengalami masalah versi paket, cek `requirements.txt` dan gunakan Python versi yang kompatibel.


## Business Dashboards

Jelaskan tentang business dashboard yang telah dibuat. Jika ada, sertakan juga link untuk mengakses dashboard tersebut.
Business dashboard memberi gambaran terkait faktor faktor yang memppengaruhi atrisi pekerja perusahaan. Faktor faktor tersebut teridi dari pendapatan per bulan, departemen, kepuasan terhadap lingkungan, kepuasan terhadap pekerjaan, pengalaman kerja/banyak perusahaan yang pernah memperkerjakan karyawan, level opsi stok karyawan, lama karyawan di posisi kerja-nya, persen peningkatan gaji, kepuasan terhadap work-life balance, dan lama bekerja dengan manajer yang sama.

Berikut merupakan link untuk mengakses dashboard:
https://lookerstudio.google.com/reporting/d03aaa2d-02ac-4d48-9a65-4bd2ecf38875

## Conclusion

1. **Kinerja Model**: Model yang dikembangkan mencapai akurasi 88.44% pada data pengujian, menunjukkan kemampuan yang baik dalam memprediksi kemungkinan seorang karyawan akan meninggalkan perusahaan. Namun, perlu diperhatikan bahwa model menunjukkan tingkat recall yang rendah untuk kelas "Attrition" (3.13%), yang berarti model kesulitan mengidentifikasi karyawan yang benar-benar akan resign.

2. **Faktor Paling Berpengaruh**:
   - **Pendapatan Bulanan (Monthly Income)** adalah faktor dominan yang mempengaruhi keputusan karyawan tetap atau keluar, dengan skor kepentingan 0.25
   - **Persentase Kenaikan Gaji (Percent Salary Hike)** menjadi faktor kedua terpenting (0.093)
   - **Jumlah Perusahaan Sebelumnya (Num Companies Worked)** menunjukkan bahwa pengalaman kerja di perusahaan lain mempengaruhi loyalitas (0.089)

3. **Faktor Kepuasan dan Keseimbangan**:
   - Environment Satisfaction dan Job Satisfaction menunjukkan pengaruh yang signifikan terhadap attrition
   - Work-Life Balance juga berkontribusi pada retensi karyawan
   - Stock Option Level memiliki pengaruh positif dalam mempertahankan karyawan

4. **Faktor Manajemen dan Pengalaman**:
   - Durasi bekerja dengan manajer saat ini (Years With Current Manager) 
   - Durasi waktu di posisi saat ini (Years In Current Role)
   - Kedua faktor ini menunjukkan pentingnya hubungan dan stabilitas dalam pekerjaan

5. **Faktor Organisasional**:
   - Departemen memiliki pengaruh yang lebih kecil dibandingkan faktor-faktor individual, namun tetap relevan

### Rekomendasi Action Items

#### 1. **Optimalisasi Struktur Kompensasi (Prioritas Tinggi)**
   - Lakukan review menyeluruh terhadap sistem gaji agar kompetitif dengan standar industri
   - Implementasikan mekanisme kenaikan gaji yang transparan dan adil untuk semua level karyawan
   - Pertimbangkan untuk meningkatkan margin kenaikan gaji tahunan (Salary Hike) yang saat ini menjadi faktor kedua paling penting
   - Pertahankan dan tingkatkan benefit stock option untuk karyawan jangka panjang

#### 2. **Program Peningkatan Kepuasan Kerja (Prioritas Tinggi)**
   - Tingkatkan fasilitas dan kualitas lingkungan kerja (kantor, furniture, teknologi)
   - Lakukan survei berkala untuk mengukur job satisfaction dan environment satisfaction
   - Buat program pengembangan karir yang jelas untuk meningkatkan kepuasan kerja
   - Implementasikan flexible working arrangement untuk meningkatkan work-life balance

#### 3. **Penguatan Hubungan Manajemen (Prioritas Sedang)**
   - Berikan training kepada manajer tentang people management dan leadership skills
   - Ciptakan sistem mentoring formal antara manajer dan karyawan untuk membangun hubungan yang kuat
   - Dorong one-on-one meetings reguler antara manager dan subordinat
   - Evaluasi kualitas kepemimpinan manajer dengan metrik yang jelas

#### 4. **Strategi Retensi Berbasis Pengalaman (Prioritas Sedang)**
   - Identifikasi dan berikan perhatian khusus kepada karyawan dengan pengalaman kerja ekstensif (banyak perusahaan sebelumnya)
   - Ciptakan special programs untuk karyawan senior yang mungkin mencari tantangan baru
   - Tawarkan project rotasi atau role variety untuk mencegah monotonitas
   - Implementasikan succession planning untuk memastikan pertumbuhan karir jelas

#### 5. **Analisis Departemen Spesifik (Prioritas Sedang)**
   - Lakukan deep dive analysis pada departemen dengan tingkat attrition tertinggi
   - Terapkan tailored retention strategies untuk setiap departemen
   - Identifikasi best practices dari departemen dengan attrition rendah
   - Alokasikan budget pengembangan berdasarkan risiko attrition per departemen

#### 6. **Program Retensi Khusus (Prioritas Sedang)**
   - Rancanng program loyalty untuk karyawan dengan tenure panjang
   - Berikan recognition dan reward untuk karyawan yang stay loyal
   - Implementasikan referral program untuk meningkatkan engagement
   - Buat employee engagement initiatives yang regular dan meaningful

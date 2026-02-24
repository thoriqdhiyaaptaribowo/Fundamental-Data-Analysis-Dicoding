# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Hingga saat ini ia telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias dropout.

Jumlah dropout yang tinggi ini tentunya menjadi salah satu masalah yang besar untuk sebuah institusi pendidikan. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang mungkin akan melakukan dropout sehingga dapat diberi bimbingan khusus.

### Permasalahan Bisnis

1. Faktor-faktor apa sajakah yang paling signifikan mempengaruhi tingkat dropout siswa?
2. Strategi apa saja yang dapat diimplementasikan perusahaan untuk mengurangi tingkat dropout siswa?

### Cakupan Proyek

Cakupan dari proyek ini adalah untuk mencari informasi terkait faktor-faktor yang mempengaruhi tingkat dropout siswa dengan serta mengetahui tindakan apa yang dapat dilakukan untuk mengurangi tingkat dropout dengan melakukan analisis korelasi dan membuat model machine learning

### Persiapan

Sumber data: 'data.csv'

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

4. Menjalankan skrip prediction atau analisis:

```bash
python prediction.py
# atau buka `notebook.ipynb` di Jupyter untuk eksplorasi interaktif
```

Catatan:
- Pastikan file dataset (`data.csv`) berada pada direktori yang sesuai (sama dengan repository), atau sesuaikan path di dalam skrip/notebook.
- Jika mengalami masalah versi paket, cek `requirements.txt` dan gunakan Python versi yang kompatibel.


## Business Dashboards

Business dashboard memberi gambaran terkait faktor faktor yang memppengaruhi tingkat dropout siswa. Faktor faktor tersebut teridi dari Course yang diambil, status nikah, jadwal pagi atau sore, status displaced, kebutuhan akademik khusus, status hutang, status keterlambatan SPP, dan status kebeasiswaan. Berikut merupakan link untuk mengakses dashboard:
https://lookerstudio.google.com/reporting/17130a83-9567-49b7-bc65-8bf7b604ff0a

## Menjalankan Sistem Machine Learning
Untuk menggunakan Sistem machine learning secara lokal, install streamlit dan jalankan app dengan program berikut
```
pip install streamlit
streamlit run "Education Problem/app.py"
```
kemudian akses http://localhost:8501 untuk membuka app di browser

Atau jalankan sistem dengan menggunakan streamlit cloud melalui link berikut:
https://thoriqdhiyaaptaribowo-fundamental-da-educationproblemapp-jseegt.streamlit.app/


Cara penggunakan app:
- Gunakan tombol “Upload CSV” untuk mengunggah file CSV berisi kolom-kolom fitur.
- Centang “Use sample CSV” jika file sample.csv ada di folder Education Problem.
- Tekan “Run predictions” untuk memproses dan menampilkan hasil.
- Gunakan tombol “Download predictions as CSV” untuk mengunduh hasil.

## Conclusion

- **Ringkasan:** Analisis eksploratori dan pemodelan menunjukkan faktor yang dapat memprediksi status siswa (`Graduate`, `Dropout`, `Enrolled`).
- **Faktor penting:** Berdasarkan korelasi dan feature importance, variabel yang paling berpengaruh meliputi `Admission_grade`, indikator finansial (`Tuition_fees_up_to_date`, `Scholarship_holder`), `Educational_special_needs`, serta indikator ekonomi makro (`Unemployment_rate`, `GDP`, `Inflation_rate`).
- **Performa model:** Model RandomForest berhasil dilatih dan memberikan prediksi, namun membutuhkan validasi lebih lanjut pada data eksternal dan penanganan potensi imbalance atau missing value.

### Rekomendasi Action Items

- **Intervensi akademik:** Sediakan program remedial dan bimbingan bagi siswa dengan `Admission_grade` rendah atau tanda penurunan performa akademik.
- **Bantuan finansial:** Perluas akses beasiswa dan skema pembayaran fleksibel untuk siswa yang terlambat membayar `Tuition_fees_up_to_date`.
- **Dukungan kebutuhan khusus:** Sediakan pendampingan dan layanan khusus untuk siswa dengan `Educational_special_needs`.
- **Monitoring pembayaran:** Buat notifikasi otomatis dan alur penagihan proaktif untuk mencegah dropout terkait biaya.
- **Ukur dampak:** Jalankan pilot terukur (mis. A/B test) untuk mengukur efektivitas intervensi sebelum skala penuh.

Catatan: Semua rekomendasi sebaiknya didukung dengan data tambahan dan pengukuran dampak setelah implementasi.


# Data Cleansing API

## Deskripsi
Proyek ini membuat API untuk membersihkan data teks menggunakan Flask, Pandas, dan RegEx. API ini dapat menerima input berupa teks atau file CSV dan mengembalikan teks yang sudah dibersihkan.

## Fitur
- Membersihkan teks dari kata kasar dan mengganti kata alay dengan kata normal.
- Menghapus emoji dari teks.
- Menyimpan data yang sudah dibersihkan ke database SQLite.

## Endpoint
- `POST /clean-text`: Menerima input teks dan mengembalikan teks yang sudah dibersihkan.
- `POST /upload`: Menerima file CSV dan mengembalikan teks yang sudah dibersihkan dalam file.

## Penggunaan
1. Clone repository ini:
    ```sh
    git clone <URL_REPOSITORY_GITHUB>
    cd nama_proyek
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Jalankan aplikasi:
    ```sh
    python app1.py
    ```

## Kontribusi
Silakan buat pull request untuk kontribusi atau perbaikan.

## Lisensi
Proyek ini dilisensikan di bawah MIT License.

# Cara Menjalankan Program

1. Buka file ini dengan Visual Studio Code atau code editor lainnya.
2. Buka terminal yang ada di Visual Studio Code.
3. Install Virtual Environment:
   - ketik perintah berikut pada terminal:
     python -m venv venv
4. Aktifkan Virtual Environment:
   venv\Scripts\activate
   - Jika berhasil, prompt terminal akan berubah dari `base` menjadi `venv`.
5. Install Flask:
   pip install flask
6. Install Torch dan dependensinya:
   pip install torch torchvision nltk
7. Install NLTK:
   pip install nltk
8. Jika cara di atas tidak berhasil untuk NLTK, coba alternatif berikut:
   - Ketik `python` pada terminal.
   - Masukkan perintah berikut satu per satu:
     ```python
     import nltk
     nltk.download('punkt')
     ```
   - Setelah selesai, ketik `quit()` lalu tekan Enter.
9. Atur variabel lingkungan Flask:
     ```sh
     set FLASK_APP=app.py
     ```

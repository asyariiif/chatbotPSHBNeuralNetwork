from flask import Flask, render_template, request, jsonify

from chat import get_response

# Membuat instance dari Flask
app = Flask(__name__)

# Mendefinisikan rute untuk halaman utama dengan metode GET
@app.get("/")
def index_get():
    # Merender template HTML untuk halaman utama
    return render_template("base.html")

# Mendefinisikan rute untuk memproses permintaan prediksi dengan metode POST
@app.post("/predict")
def predict():
    # Mengambil teks pesan dari permintaan JSON
    text = request.get_json().get("message")
    # Mendapatkan respon dari fungsi get_response berdasarkan teks yang diberikan
    response = get_response(text)
    # Menyusun pesan dalam format JSON
    message = {"answer": response}
    # Mengembalikan respon sebagai JSON
    return jsonify(message)

# Menjalankan aplikasi Flask dalam mode debug
if __name__ == "__main__":
    app.run(debug=True)

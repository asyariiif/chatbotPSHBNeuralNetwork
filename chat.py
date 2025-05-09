import random
import json
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Memilih perangkat yang akan digunakan (GPU jika tersedia, jika tidak menggunakan CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Membaca file intents.json yang berisi data intents
with open('datasets.json', 'r') as json_data:
    datasets = json.load(json_data)

# Memuat model yang sudah dilatih
FILE = "model.pth"
data = torch.load(FILE)

input_size = data["input_size"]  # Ukuran input
hidden_size = data["hidden_size"]  # Ukuran lapisan tersembunyi
output_size = data["output_size"]  # Ukuran output
all_words = data['all_words']  # Daftar semua kata
tags = data['tags']  # Daftar tag
model_state = data["model_state"]  # State model yang sudah dilatih

# Membuat model dengan ukuran input, hidden, dan output yang sesuai
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)  # Memuat state model yang sudah dilatih
model.eval()  # Mengatur model ke mode evaluasi

bot_name = "RuangBot"  # Nama bot

def get_response(msg):
    # Memecah kalimat menjadi kata-kata
    sentence = tokenize(msg)
    # Membuat bag of words dari kalimat yang di-tokenisasi
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])  # Mengubah bentuk array untuk diproses oleh model
    X = torch.from_numpy(X).to(device)  # Mengonversi array menjadi tensor dan memindahkannya ke perangkat

    # Menghitung output dari model
    output = model(X)
    _, predicted = torch.max(output, dim=1)  # Mendapatkan indeks dengan nilai probabilitas tertinggi

    tag = tags[predicted.item()]  # Mengambil tag yang sesuai dengan prediksi

    probs = torch.softmax(output, dim=1)  # Menghitung softmax untuk mendapatkan probabilitas
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:  # Jika probabilitas cukup tinggi, pilih respon yang sesuai
        for dataset in datasets['datasets']:
            if tag == dataset["tag"]:
                return random.choice(dataset['responses'])
    
    return "Hi maaf saya tidak tahu soal itu..."  # Respon default jika tidak ada kecocokan

if __name__ == "__main__":
    print("Mari ngobrol! (ketik 'quit' untuk keluar)")
    while True:
        sentence = input("Anda: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

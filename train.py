import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet

# Membaca file JSON yang berisi intents
with open('datasets.json', 'r') as f:
    datasets = json.load(f)

# Menyiapkan daftar untuk menyimpan semua kata, tag, dan pasangan (kata, tag)
all_words = []
tags = []
xy = []

# Loop melalui setiap kalimat dalam pola intents
for dataset in datasets['datasets']:
    tag = dataset['tag']
    # Menambahkan tag ke dalam daftar tags
    tags.append(tag)
    for pattern in dataset['patterns']:
        # Memecah kalimat menjadi kata-kata
        w = tokenize(pattern)
        # Menambahkan kata-kata ke dalam daftar all_words
        all_words.extend(w)
        # Menambahkan pasangan (kata, tag) ke dalam daftar xy
        xy.append((w, tag))

# Menghilangkan karakter-karakter tertentu dan mengkonversi kata menjadi bentuk dasar
ignore_words = ['?', '.', '!']
all_words = [stem(w) for w in all_words if w not in ignore_words]
# Menghapus duplikat dan mengurutkan kata-kata
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Menampilkan jumlah pola, tag, dan kata unik yang telah diproses
print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "unique stemmed words:", all_words)

# Membuat data pelatihan
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: membuat bag of words untuk setiap pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: menggunakan indeks tag sebagai label
    label = tags.index(tag)
    y_train.append(label)

# Mengubah daftar menjadi array numpy
X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters 
num_epochs = 1000  # Jumlah iterasi pelatihan
batch_size = 8  # Jumlah sampel per batch
learning_rate = 0.001  # Kecepatan pembelajaran
input_size = len(X_train[0])  # Ukuran input (jumlah kata unik)
hidden_size = 8  # Ukuran lapisan tersembunyi
output_size = len(tags)  # Jumlah output (jumlah tag)
print(input_size, output_size)

# Membuat kelas dataset khusus untuk digunakan oleh DataLoader
class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)  # Jumlah sampel
        self.x_data = X_train  # Data input
        self.y_data = y_train  # Label

    # Mendukung indexing agar dataset[i] bisa mengembalikan sampel ke-i
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # Mendukung fungsi len(dataset) untuk mengembalikan ukuran dataset
    def __len__(self):
        return self.n_samples

# Membuat objek dataset dan DataLoader
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

# Memilih perangkat yang akan digunakan (GPU jika tersedia, jika tidak menggunakan CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Membuat model neural network dan memindahkannya ke perangkat yang dipilih
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Mendefinisikan fungsi loss dan optimizer
criterion = nn.CrossEntropyLoss()  # Fungsi loss
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  # Optimizer

# Melatih model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)  # Memindahkan data ke perangkat
        labels = labels.to(dtype=torch.long).to(device)  # Memindahkan label ke perangkat dengan tipe long
        
        # Forward pass (menghitung output dari model)
        outputs = model(words)
        loss = criterion(outputs, labels)  # Menghitung loss
        
        # Backward pass dan optimisasi
        optimizer.zero_grad()  # Menghapus gradien sebelumnya
        loss.backward()  # Backpropagation untuk menghitung gradien
        optimizer.step()  # Memperbarui parameter model
        
    # Setiap 100 epoch, menampilkan loss saat ini
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Menampilkan loss terakhir setelah pelatihan selesai
print(f'final loss: {loss.item():.4f}')

# Menyimpan model dan parameter lainnya ke dalam file
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "model.pth"
torch.save(data, FILE)

# Menampilkan pesan bahwa pelatihan telah selesai dan file telah disimpan
print(f'training complete. file saved to {FILE}')

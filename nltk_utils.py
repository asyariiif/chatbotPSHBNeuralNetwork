import numpy as np
import nltk
nltk.download('punkt_tab')
from nltk.stem.porter import PorterStemmer

# Membuat objek stemmer dari PorterStemmer untuk stemming kata
stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Memecah kalimat menjadi array kata/token.
    Token bisa berupa kata, karakter tanda baca, atau angka.
    """
    return nltk.word_tokenize(sentence)

def stem(word):
    """
    Melakukan stemming pada kata, yaitu menemukan bentuk dasar dari kata.
    Contoh:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    """
    Mengembalikan array bag of words:
    1 untuk setiap kata yang dikenal yang ada dalam kalimat, 0 untuk kata lainnya.
    Contoh:
    kalimat = ["halo", "bagaimana", "kabar", "kamu"]
    kata-kata = ["hai", "halo", "saya", "kamu", "selamat tinggal", "terima kasih", "keren"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # Melakukan stemming pada setiap kata dalam kalimat yang sudah di-tokenisasi
    sentence_words = [stem(word) for word in tokenized_sentence]
    # Menginisialisasi bag dengan 0 untuk setiap kata yang ada dalam daftar words
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1  # Menandai dengan 1 jika kata ditemukan dalam kalimat

    return bag

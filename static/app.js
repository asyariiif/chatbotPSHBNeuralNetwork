class Chatbox {
    // Konstruktor untuk menginisialisasi properti dan elemen DOM yang diperlukan
    constructor() {
        // Mendefinisikan elemen DOM untuk tombol, kotak obrolan, dan tombol kirim
        this.args = {
            openButton: document.querySelector('.chatbox__button'), // Tombol untuk membuka/mengaktifkan chatbox
            chatBox: document.querySelector('.chatbox__support'),  // Elemen utama chatbox
            sendButton: document.querySelector('.send__button')    // Tombol untuk mengirim pesan
        }

        this.state = false; // Status awal chatbox (tertutup)
        this.messages = []; // Array untuk menyimpan pesan obrolan
    }

    // Fungsi untuk mengatur event listener dan menampilkan logika interaksi
    display() {
        // Destruktur elemen DOM untuk kemudahan akses
        const {openButton, chatBox, sendButton} = this.args;

        // Tambahkan event listener untuk membuka/tutup chatbox saat tombol diklik
        openButton.addEventListener('click', () => this.toggleState(chatBox));

        // Tambahkan event listener untuk mengirim pesan saat tombol kirim diklik
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        // Ambil input field dalam chatbox dan tambahkan event listener untuk mendeteksi "Enter"
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") { // Jika tombol Enter ditekan
                this.onSendButton(chatBox); // Panggil fungsi untuk mengirim pesan
            }
        });
    }

    // Fungsi untuk mengubah status (buka/tutup) chatbox
    toggleState(chatbox) {
        this.state = !this.state; // Balikkan status chatbox (true <-> false)

        // Tampilkan atau sembunyikan chatbox berdasarkan status
        if(this.state) {
            chatbox.classList.add('chatbox--active'); // Tambahkan kelas untuk menampilkan chatbox
        } else {
            chatbox.classList.remove('chatbox--active'); // Hapus kelas untuk menyembunyikan chatbox
        }
    }

    // Fungsi untuk mengirim pesan
    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input'); // Ambil elemen input untuk pesan
        let text1 = textField.value; // Ambil teks dari input
        if (text1 === "") { // Jika input kosong, hentikan fungsi
            return;
        }

        // Tambahkan pesan pengguna ke array messages
        let msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);

        // Kirim pesan ke server menggunakan fetch API
        fetch('http://127.0.0.1:5000/predict', { // URL endpoint server
            method: 'POST', // Metode HTTP POST
            body: JSON.stringify({ message: text1 }), // Kirim data dalam format JSON
            mode: 'cors', // Mode CORS (untuk lintas asal)
            headers: {
              'Content-Type': 'application/json' // Header untuk tipe konten JSON
            },
        })
        .then(r => r.json()) // Parse respons server sebagai JSON
        .then(r => {
            // Tambahkan balasan server ke array messages
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox); // Perbarui tampilan chatbox
            textField.value = ''; // Kosongkan input field
        })
        .catch((error) => {
            console.error('Error:', error); // Tampilkan error di console
            this.updateChatText(chatbox); // Tetap perbarui tampilan chatbox
            textField.value = ''; // Kosongkan input field
        });
    }

    // Fungsi untuk memperbarui teks dalam chatbox
    updateChatText(chatbox) {
        var html = ''; // Variabel untuk menyimpan HTML pesan
        // Iterasi terbalik array messages untuk menampilkan pesan terbaru di atas
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam") { // Jika pengirim adalah "Sam" (bot)
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else { // Jika pengirim adalah "User"
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        // Masukkan HTML pesan ke elemen chatbox
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

// Membuat instance baru dari Chatbox dan mengaktifkan fungsi display
const chatbox = new Chatbox();
chatbox.display();

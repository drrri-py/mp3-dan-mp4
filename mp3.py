import os
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

class MP3PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("400x300")

        self.current_file = None
        self.playlist = []

        mixer.init()  # Inisialisasi mixer

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Label untuk menampilkan file yang sedang diputar
        self.current_file_label = tk.Label(self.root, text="Tidak ada file yang diputar", wraplength=300)
        self.current_file_label.pack(pady=10)

        # Tombol untuk memilih folder dengan file MP3
        choose_folder_button = tk.Button(self.root, text="Pilih Folder", command=self.choose_folder)
        choose_folder_button.pack(pady=10)

        # Listbox untuk menampilkan playlist
        self.playlist_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10)
        self.playlist_listbox.pack(pady=10)

        # Tombol untuk memutar dan menghentikan lagu
        play_button = tk.Button(self.root, text="Putar", command=self.play_music)
        play_button.pack(pady=5)

        stop_button = tk.Button(self.root, text="Hentikan", command=self.stop_music)
        stop_button.pack(pady=5)

        # Volume slider
        volume_label = tk.Label(self.root, text="Volume")
        volume_label.pack()
        self.volume_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(50)  # Volume default
        self.volume_slider.pack()

    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.playlist = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".mp3")]
            self.update_playlist()

    def update_playlist(self):
        self.playlist_listbox.delete(0, tk.END)
        for file_path in self.playlist:
            self.playlist_listbox.insert(tk.END, os.path.basename(file_path))

    def play_music(self):
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_file = self.playlist[selected_index]

            mixer.music.load(selected_file)
            mixer.music.play()

            self.current_file = selected_file
            self.current_file_label["text"] = f"Sedang diputar: {os.path.basename(selected_file)}"

    def stop_music(self):
        mixer.music.stop()

    def set_volume(self, val):
        volume = int(val) / 100.0
        mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3PlayerApp(root)
    root.mainloop()


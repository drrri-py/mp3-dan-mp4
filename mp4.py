import tkinter as tk
from tkinter import filedialog
import cv2
import threading
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 Player")

        # Inisialisasi variabel
        self.video_path = ""
        self.cap = None
        self.playing = False

        # Membuat UI
        self.create_ui()

    def create_ui(self):
        # Frame untuk menempatkan kontrol
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Tombol Pilih Video
        select_button = tk.Button(control_frame, text="Pilih Video", command=self.select_video)
        select_button.grid(row=0, column=0, padx=10)

        # Tombol Putar/Pause
        play_pause_button = tk.Button(control_frame, text="Putar", command=self.play_pause_video)
        play_pause_button.grid(row=0, column=1, padx=10)

        # Menampilkan video
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if file_path:
            self.video_path = file_path
            self.cap = cv2.VideoCapture(file_path)
            self.play_video()

    def play_pause_video(self):
        if self.playing:
            self.playing = False
        else:
            self.playing = True
            threading.Thread(target=self.update_video).start()

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.canvas.config(width=img.width(), height=img.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.canvas.image = img

            if self.playing:
                self.root.after(30, self.play_video)
        else:
            self.cap.release()
            self.playing = False

    def update_video(self):
        while self.playing:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.canvas.config(width=img.width(), height=img.height())
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.canvas.image = img
            else:
                self.cap.release()
                self.playing = False

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()

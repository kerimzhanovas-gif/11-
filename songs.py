import tkinter as tk
from tkinter import messagebox
import os
import cv2
from PIL import Image, ImageTk
import threading
import time

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Музыкальные видео")
        self.root.geometry("800x600")
        self.root.configure(bg='#FFB6C1')
        
        self.current_video = None
        self.cap = None
        self.playing = False
        self.video_label = None
        
        self.create_widgets()
    
    def create_widgets(self):
        title_label = tk.Label(
            self.root, 
            text="Музыкальные видео",
            font=("Arial", 16, "bold"),
            fg="#8B008B",
            bg='#FFB6C1'
        )
        title_label.pack(pady=10)
        
        self.create_video_player()
        
        video_buttons_frame = tk.Frame(self.root, bg='#FFB6C1')
        video_buttons_frame.pack(pady=10)
        
        btn1 = tk.Button(
            video_buttons_frame,
            text="NewJeans - ASAP",
            font=("Arial", 10, "bold"),
            bg='#FF69B4',
            fg='white',
            width=15,
            height=2,
            command=lambda: self.play_video("newjeans_asap.mp4")
        )
        btn1.grid(row=0, column=0, padx=5, pady=5)
        
        btn2 = tk.Button(
            video_buttons_frame,
            text="ENHYPEN - Outside",
            font=("Arial", 10, "bold"),
            bg='#DB7093',
            fg='white',
            width=15,
            height=2,
            command=lambda: self.play_video("enhypen_outside.mp4")
        )
        btn2.grid(row=0, column=1, padx=5, pady=5)
        
        btn3 = tk.Button(
            video_buttons_frame,
            text="Cortis - Fashion",
            font=("Arial", 10, "bold"),
            bg='#C71585',
            fg='white',
            width=15,
            height=2,
            command=lambda: self.play_video("cortis_fashion.mp4")
        )
        btn3.grid(row=0, column=2, padx=5, pady=5)
        
        control_frame = tk.Frame(self.root, bg='#FFB6C1')
        control_frame.pack(pady=10)
        
        stop_btn = tk.Button(
            control_frame,
            text="Остановить видео",
            font=("Arial", 10, "bold"),
            bg='#8B008B',
            fg='white',
            width=15,
            height=2,
            command=self.stop_video
        )
        stop_btn.pack(padx=5, pady=5)
        
        self.status_label = tk.Label(
            self.root,
            text="Видео появится здесь после выбора",
            font=("Arial", 10),
            fg="#8B008B",
            bg='#FF69B4'
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_video_player(self):
        video_frame = tk.Frame(self.root, bg='black', width=640, height=360)
        video_frame.pack(pady=10)
        video_frame.pack_propagate(False)
        
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(expand=True, fill=tk.BOTH)
    
    def find_video_file(self, filename):
        paths = [
            filename,
            f"videos/{filename}",
            f"video/{filename}",
            f"venv/Lib/site-packages/moviepy/video/{filename}",
            f"venv/lib/site-packages/moviepy/video/{filename}"
        ]
        for path in paths:
            if os.path.exists(path):
                return path
        return None
    
    def play_video(self, filename):
        filepath = self.find_video_file(filename)
        
        if not filepath:
            messagebox.showerror("Ошибка", f"Файл {filename} не найден!")
            return
        
        self.stop_video()
        
        try:
            self.cap = cv2.VideoCapture(filepath)
            if not self.cap.isOpened():
                messagebox.showerror("Ошибка", "Не удалось открыть видео")
                return
            
            self.playing = True
            self.current_video = filepath
            self.status_label.config(text=f"Воспроизводится: {filename}")
            
            thread = threading.Thread(target=self.update_video)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
    
    def update_video(self):
        while self.playing and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            else:
                break
            time.sleep(0.03)
        
        if self.playing:
            self.stop_video()
            self.status_label.config(text="Воспроизведение завершено")
    
    def stop_video(self):
        self.playing = False
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.video_label.configure(image='')
        self.status_label.config(text="Выберите видео для воспроизведения")

def main():
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import cv2
import pyautogui
import tkinter as tk
from tkinter import filedialog
import threading
import numpy as np
import os

class ScreenRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Recorder")
        self.master.geometry("200x200")
        self.master.configure(bg="#CD7F32")

        self.label = tk.Label(self.master, text="ScreenRecorder", bg="#CD7F32", fg="white", font=("Arial", 14, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.recording = False
        self.output_file = ""
        self.default_output_dir = os.path.expanduser("~/Videos")
        self.output_dir_selected = False

        self.start_button = tk.Button(self.master, text="Gravar", command=self.start_recording, bg="white", width=10)
        self.start_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.stop_button = tk.Button(self.master, text="Parar", command=self.stop_recording, state="disabled", bg="#FFCCCC", width=10)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.select_button = tk.Button(self.master, text="Selecionar Local", command=self.select_location, bg="white", width=10)
        self.select_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.file_counter = 1000

    def start_recording(self):
        self.recording = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        if not self.output_dir_selected:
            
            answer = tk.messagebox.askyesno("Local de Salvamento", "Você gostaria de selecionar o local de salvamento?")
            if answer:
                self.select_location()
                self.output_dir_selected = True

        self.output_file = os.path.join(self.default_output_dir, f"record_{self.file_counter}.avi")
        self.file_counter += 1

        threading.Thread(target=self.record_screen).start()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def select_location(self):
        self.default_output_dir = filedialog.askdirectory()
        self.output_dir_selected = True

    def record_screen(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.output_file, fourcc, 20.0, screen_size)

        while self.recording:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame)

        out.release()

def main():
    root = tk.Tk()
    app = ScreenRecorder(root)
    root.mainloop()

if __name__ == "__main__":
    main()

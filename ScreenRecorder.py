import cv2
import pyautogui
import tkinter as tk
from tkinter import filedialog
import threading
import numpy as np

class ScreenRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Recorder")

        self.recording = False
        self.output_file = ""

        self.start_button = tk.Button(self.master, text="Gravar", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(self.master, text="Parar", command=self.stop_recording, state="disabled")
        self.stop_button.pack()

        self.select_button = tk.Button(self.master, text="Selecionar Local", command=self.select_location)
        self.select_button.pack()

    def start_recording(self):
        self.recording = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        self.output_file = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
        if not self.output_file:
            self.recording = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            return

        threading.Thread(target=self.record_screen).start()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def select_location(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])

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

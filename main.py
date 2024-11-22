import tkinter as tk
from tkinter import ttk, font
from dotenv import dotenv_values
import requests
from PIL import Image, ImageTk
import sv_ttk
import sys
import os
from ctypes import windll
from frames.result_frame import ResultFrame
from frames.numpad_frame import NumpadFrame
windll.shcore.SetProcessDpiAwareness(1)
config = dotenv_values(".env")



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reservation")
        self.geometry("800x480")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0,2),  weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.toggle_status = "lbl"
        # Load images
        self.kb_image = ImageTk.PhotoImage(
            Image.open("./images/kb.png").resize((30, 30)))
        self.bp_image = ImageTk.PhotoImage(
            Image.open("./images/backspace.png").resize((30, 30)))
        self.check_image = ImageTk.PhotoImage(
            Image.open("./images/check.png").resize((30, 30)))
        self.kb_down_image = ImageTk.PhotoImage(
            Image.open("./images/kb_down.png").resize((30, 30)))

        # Input Field
        # Using custom font for input field
        self.input = ttk.Entry(self, font=self.get_font())
        self.input.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=3
        )
        self.input.bind("<Return>", self.check_id)
        self.input.focus_set()

        self.labelframe = ResultFrame(self)
        self.labelframe.grid(
            row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=3
        )

        style = ttk.Style(self)
        # Using custom font for buttons
        style.configure("Small.TButton", font=self.get_font())

        self.btn = ttk.Button(
            self, text="開啟鍵盤", image=self.kb_image, compound="left",
            command=self.hide_label, style="Small.TButton")
        self.btn.grid(row=2, column=1, padx=10, pady=10)

        self.back_btn = ttk.Button(
            self, text="刪除", image=self.bp_image, compound="left",
            command=self.delete_btn_press, style="Small.TButton")
        self.back_btn.grid(row=2, column=0, padx=10, pady=10)
        self.back_btn.grid_remove()

        self.confirm_btn = ttk.Button(
            self, text="確認", image=self.check_image, compound="left",
            command=self.confirm_btn_press, style="Small.TButton")
        self.confirm_btn.grid(row=2, column=2, padx=10, pady=10)
        self.confirm_btn.grid_remove()

        self.kbframe = NumpadFrame(self)
        self.kbframe.grid(
            row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=3
        )
        self.kbframe.grid_remove()

    def get_font(self):
        # Use system-installed Noto Sans font
        # Using the system-installed Noto Sans font
        return font.Font(family="Noto Sans TC", size=16)

    def confirm_btn_press(self):
        self.input.delete(0, "end")
        self.hide_label()
        self.check_id()

    def delete_btn_press(self):
        current_text = self.input.get()
        self.input.delete(len(current_text)-1, "end")

    def hide_label(self):
        if self.toggle_status == "lbl":
            self.labelframe.grid_remove()
            self.kbframe.grid()
            self.confirm_btn.grid()
            self.back_btn.grid()
            self.btn.configure(text="收起鍵盤", image=self.kb_down_image)
            self.toggle_status = "kb"
        else:
            self.kbframe.grid_remove()
            self.confirm_btn.grid_remove()
            self.back_btn.grid_remove()
            self.labelframe.grid()
            self.btn.configure(text="開啟鍵盤", image=self.kb_image)
            self.toggle_status = "lbl"

    def check_id(self, event=None):
        try:
            combined_url = f"""{config['API_URL']}/{config['DEVICE_NUM']}/{self.input.get()}"""
            print(f"Code entered: {self.input.get()}")
            r = requests.get(combined_url, timeout=5)
            r.raise_for_status()
            print(r.text)
            self.labelframe.result_msg.configure(text=r.text)
        except Exception as e:
            print(f"Error: {e}")
            self.labelframe.result_msg.configure(text="網路錯誤")
        self.input.delete(0, tk.END)


app = App()
app.mainloop()

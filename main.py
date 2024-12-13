import tkinter as tk
from tkinter import ttk
from dotenv import dotenv_values
from ttkthemes import ThemedTk
from frames.numpad import NumpadFrame
from frames.buttons import ButtonsFrame
from tkinter.font import nametofont
import requests
import time
import sv_ttk
config = dotenv_values(".env")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultation")
        self.geometry("800x480")
        self.attributes("-fullscreen", True)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.is_kb_open = False

        self.input = ttk.Entry(self, font=("Arial", 45))
        self.input.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew",
            columnspan=3
        )
        self.input.bind("<Return>", self.check_id)
        self.input.focus_set()

        self.results = ttk.Label(
            self,
            text="請刷卡或輸入卡號",
            font=("Arial", 45),
            anchor='center'
            )
        self.results.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew",
            columnspan=3
        )

        self.numpad = NumpadFrame(self)
        self.numpad.grid(
            row=1,
            padx=10,
            pady=10,
            sticky="nsew",
            columnspan=3
        )
        self.numpad.grid_remove()

        self.buttons = ButtonsFrame(self)
        self.buttons.grid(
            row=2,
            columnspan=3,
            sticky="nsew"
            )
        self.buttons.confirm_btn.grid_remove()
        self.buttons.delete_btn.grid_remove()

    def hide_label(self):
        if self.is_kb_open:
            self.numpad.grid_remove()
            self.results.grid()
            self.buttons.hide_btns()
            self.is_kb_open = False
            self.input.focus_set()
        else:
            self.results.grid_remove()
            self.numpad.grid()
            self.buttons.show_btns()
            self.is_kb_open = True
    def reset(self):
        
        self.results.configure(text="請刷卡或輸入卡號")
        self.input.focus_set()


    def check_id(self, event=None):
        if self.input.get() == "10369601":
            self.destroy()
        print(self.input.get())
        print(type(self.input.get()))
        self.input.delete(0, "end")
        self.results.configure(text="處理中")
        try:
            combined_url = f"""{
                str(config["API_URL"])}/{str(config["DEVICE_NUM"])}/{self.input.get()}"""
            print(f"code entered: {self.input.get()}")
            r = requests.get(combined_url, timeout=5)
            r.raise_for_status()
            print(r.text)
            self.results.configure(text=str(r.text))
            self.after(3000, self.reset)

        except Exception as e:
            print(f"Error: {e}")
            self.results.configure(text="刷卡失敗")
            self.after(3000, self.reset)


app = App()
sv_ttk.set_theme("light")
nametofont("SunValleyCaptionFont").configure(family='Arial', size=-18)
nametofont("SunValleyCaptionFont").configure(family='Arial', size=-18)
nametofont("SunValleyBodyFont").configure(family='Arial', size=-20)
nametofont("SunValleyBodyStrongFont").configure(family='Arial', size=-18)
nametofont("SunValleyBodyLargeFont").configure(family='Arial', size=-22)
nametofont("SunValleySubtitleFont").configure(family='Arial', size=-22)
nametofont("SunValleyTitleFont").configure(family='Arial', size=-32)
nametofont("SunValleyTitleLargeFont").configure(family='Arial', size=-42)
nametofont("SunValleyDisplayFont").configure(family='Arial', size=-72)
app.mainloop()

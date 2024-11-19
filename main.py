import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

# Initialize the Tkinter root window
root = tk.Tk()

# Now load the images after the root window has been created


class KBFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.create_keyboard()

    def create_keyboard(self):
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
        ]

        for r, row in enumerate(keys):
            row_frame = tk.Frame(self, bg="white")  
            row_frame.grid(row=r, column=0, pady=0, padx=0, sticky="nsew")
            row_frame.grid_columnconfigure(tuple(range(len(row))), weight=1)
            row_frame.grid_rowconfigure(0, weight=1)

            for c, key in enumerate(row):
                btn = ttk.Button(row_frame, text=key, command=lambda k=key: self.type_key(k),
                                     style="Custom.TButton")

                btn.grid(row=0, column=c, padx=5, pady=5, sticky="ns")

    def type_key(self, key):
        print(f"Key pressed: {key}")
        current_text = self.master.input.get()
        self.master.input.delete(0, "end")  
        self.master.input.insert("end", current_text + key)  


class LabelFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.result_msg = ttk.Label(self, text="", font=("Arial", 45))
        self.result_msg.grid(row=0, column=0)


class App(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kb_image = ImageTk.PhotoImage(Image.open("kb.png").resize((30, 30)))
        bp_image = ImageTk.PhotoImage(Image.open("backspace.png").resize((30, 30)))
        check_image = ImageTk.PhotoImage(Image.open("check.png").resize((30, 30)))
        kb_down_image = ImageTk.PhotoImage(Image.open("kb_down.png").resize((30, 30)))

        self.title("Reservation")
        self.geometry("800x480")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.toggle_status = "lbl"
        self.input = ttk.Entry(self, font=("Arial", 90))
        self.input.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)
        self.input.focus_set()

        self.labelframe = LabelFrame(self)
        self.labelframe.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)

        self.btn = ttk.Button(self, text="開啟鍵盤", command=self.hide_label, image=kb_image, compound="left", style="Custom.TButton")
        self.btn.grid(row=2, column=1, padx=10, pady=10)

        self.back_btn = ttk.Button(self, text="刪除", command=self.delete_btn_press, image=bp_image, compound="left", style="Custom.TButton")
        self.back_btn.grid(row=2, column=0, padx=10, pady=10)

        self.back_btn.grid_remove()
        self.confirm_btn = ttk.Button(self, text="確認", command=self.confirm_btn_press, image=check_image, compound="left", style="Custom.TButton")
        self.confirm_btn.grid(row=2, column=2, padx=10, pady=10)

        self.confirm_btn.grid_remove()

        self.kbframe = KBFrame(self)
        self.kbframe.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)
        self.kbframe.grid_remove()

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
            self.btn.configure(text="收起鍵盤", image=kb_down_image)
            self.toggle_status = "kb"
        else:
            self.kbframe.grid_remove()
            self.confirm_btn.grid_remove()
            self.back_btn.grid_remove()  
            self.labelframe.grid()  
            self.btn.configure(text="開啟鍵盤", image=kb_image)
            self.toggle_status = "lbl"

    def check_id(self, event=None):
        try:
            combined_url = f'{str(config["API_URL"])}/{str(config["DEVICE_NUM"])}/{self.input.get()}'
            print(f"code entered: {self.input.get()}")
            r = requests.get(combined_url, timeout=5)
            r.raise_for_status()
            print(r.text)
            self.labelframe.result_msg.configure(text=r.text)
        except Exception as e:
            print(f"Error: {e}")
            self.labelframe.result_msg.configure(text="網路錯誤")
        self.input.delete(0, "end")


if __name__ == "__main__":
    app = App()
    app.mainloop()

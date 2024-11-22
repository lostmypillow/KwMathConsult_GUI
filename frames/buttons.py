from tkinter import ttk
from PIL import Image, ImageTk


class ButtonsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.kb_image = ImageTk.PhotoImage(
            Image.open("./images/kb.png").resize((30, 30)))
        self.bp_image = ImageTk.PhotoImage(
            Image.open("./images/backspace.png").resize((30, 30)))
        self.check_image = ImageTk.PhotoImage(
            Image.open("./images/check.png").resize((30, 30)))
        self.kb_down_image = ImageTk.PhotoImage(
            Image.open("./images/kb_down.png").resize((30, 30)))
        style = ttk.Style(self)

        self.delete_btn = ttk.Button(
            self,
            text="刪除",
            image=self.bp_image,
            compound="left",
            command=self.delete_digit,
        )
        self.delete_btn.grid(row=0, column=0, pady=10)

        self.open_btn = ttk.Button(
            self,
            text="開啟鍵盤",
            image=self.kb_image,
            compound="left",
            command=self.master.hide_label,
        )
        self.open_btn.grid(row=0, column=1, pady=10)

        self.confirm_btn = ttk.Button(
            self,
            text="確認",
            image=self.check_image,
            compound="left",
            command=self.confirm_btn_press,
        )
        self.confirm_btn.grid(row=0, column=2, pady=10)

    def confirm_btn_press(self):

        if self.master.is_kb_open:
            self.master.hide_label()
        self.master.check_id()

    def delete_digit(self):
        current_text = self.master.input.get()
        self.master.input.delete(len(current_text)-1, "end")

    def hide_btns(self):
        self.confirm_btn.grid_remove()
        self.delete_btn.grid_remove()
        self.open_btn.configure(text="開啟鍵盤", image=self.kb_image)

    def show_btns(self):
        self.open_btn.configure(text="收起鍵盤", image=self.kb_down_image)
        self.confirm_btn.grid()
        self.delete_btn.grid()

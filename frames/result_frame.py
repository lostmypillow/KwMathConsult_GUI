from tkinter import ttk
class ResultFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.result_msg = ttk.Label(self, font=master.get_font(), text="請刷卡或輸入卡號")
        self.result_msg.grid(row=0, column=0, sticky="nsew")

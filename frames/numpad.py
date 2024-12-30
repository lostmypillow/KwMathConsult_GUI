from tkinter import ttk


class NumpadFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.create_keyboard()

    def create_keyboard(self):
        keys = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0']
        ]

        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                btn = ttk.Button(
                    self, text=key, command=lambda k=key: self.type_key(k))
                if r == 3 and key == '0':
                    btn.grid(row=r, column=0, columnspan=3,
                             padx=2, pady=2, sticky="nsew")
                else:
                    btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

    def type_key(self, key):
        print(f"Key pressed: {key}")
        current_text = self.master.input.get()
        self.master.input.delete(0, "end")
        self.master.input.insert("end", current_text + key)

import customtkinter
from dotenv import dotenv_values
import requests
from PIL import Image
config = dotenv_values(".env")

kb_image = customtkinter.CTkImage(
    light_image=Image.open("kb.png"), size=(30, 30))
bp_image = customtkinter.CTkImage(
    light_image=Image.open("backspace.png"), size=(30, 30))
check_image = customtkinter.CTkImage(
    light_image=Image.open("check.png"), size=(30, 30))
kb_down_image = customtkinter.CTkImage(
    light_image=Image.open("kb_down.png"), size=(30, 30))


class KBFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2), weight=1)  # Allow columns to stretch
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)  # Allow rows to stretch
        self.create_keyboard()

    def create_keyboard(self):
        keys = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['0']  # Last row, single button spanning all columns
        ]

        # Dynamically create buttons
        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                # Special case for the last row
                if r == 3 and key == '0':
                    btn = customtkinter.CTkButton(
                        self, text=key, command=lambda k=key: self.type_key(
                            k), font=("Arial", 25), height=44
                    )
                    btn.grid(row=r, column=0, columnspan=3,
                             padx=5, pady=5, sticky="nsew")
                else:
                    btn = customtkinter.CTkButton(
                        self, text=key, command=lambda k=key: self.type_key(
                            k), font=("Arial", 25), height=44
                    )
                    btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

    def type_key(self, key):
        print(f"Key pressed: {key}")
        current_text = self.master.input.get()
        self.master.input.delete(0, "end")  # Clear current input
        self.master.input.insert(
            "end", current_text + key)  # Append new key



class LabelFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.result_msg = customtkinter.CTkLabel(
            self,
            font=("Arial", 45),
            text="",
            fg_color="transparent"
        )
        self.result_msg.grid(row=0, column=0)


class App(customtkinter.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Reservation")
        self.geometry("800x480")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0)  # Input field row
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.toggle_status = "lbl"
        # Input Field
        self.input = customtkinter.CTkEntry(
            self,
            font=("Arial", 90),
            placeholder_text="請刷卡",
        )
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

        self.labelframe = LabelFrame(self)
        self.labelframe.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew",
            columnspan=3
        )

        self.btn = customtkinter.CTkButton(
            self, text="開啟鍵盤", font=("Arial", 25), command=self.hide_label, image=kb_image, compound="left", fg_color="gray")
        self.btn.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,

        )
        self.back_btn = customtkinter.CTkButton(
            self, text="刪除", font=("Arial", 25), command=self.delete_btn_press, image=bp_image, compound="left")
        self.back_btn.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,

        )
        self.back_btn.grid_remove()
        self.confirm_btn = customtkinter.CTkButton(
            self, text="確認", font=("Arial", 25), command=self.confirm_btn_press, image=check_image, compound="left", fg_color="green")
        self.confirm_btn.grid(
            row=2,
            column=2,
            padx=10,
            pady=10,

        )
        self.confirm_btn.grid_remove()

        self.kbframe = KBFrame(self)
        self.kbframe.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew",
            columnspan=3
        )
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
            self.labelframe.grid_remove()  # Hide label frame
            self.kbframe.grid()
            self.confirm_btn.grid()
            self.back_btn.grid()  # Show the keyboard frame
            self.btn.configure(text="收起鍵盤")
            self.btn.configure(image=kb_down_image)
            self.toggle_status = "kb"
        else:
            self.kbframe.grid_remove()
            self.confirm_btn.grid_remove()
            self.back_btn.grid_remove()  # Hide keyboard
            self.labelframe.grid()  # Show label frame
            self.btn.configure(text="開啟鍵盤")
            self.btn.configure(image=kb_image)
            self.toggle_status = "lbl"

    def check_id(self, event=None):
        try:
            combined_url = f"""{
                str(config["API_URL"])}/{str(config["DEVICE_NUM"])}/{self.input.get()}"""
            print(f"code entered: {self.input.get()}")
            r = requests.get(combined_url, timeout=5)
            r.raise_for_status()
            print(r.text)
            self.labelframe.result_msg.configure(text=r.text)
        except Exception as e:
            print(f"Error: {e}")
            self.labelframe.result_msg.configure(text="網路錯誤")
        self.input.delete(0, customtkinter.END)


if __name__ == "__main__":
    app = App()
    app.mainloop()

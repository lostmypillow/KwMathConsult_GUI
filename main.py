import customtkinter
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

class InputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.input = customtkinter.CTkEntry(
            self,
            height=90,
            width=20,
            font=('Arial', 90),
            placeholder_text="請刷卡"
        )
        self.input.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky="nsw"
        )
        self.input.bind("<Return>", self.check_id)
        self.input.focus_set()
        self.btn = customtkinter.CTkButton(self, text="yo")
        self.btn.grid(
            row = 0,
            column = 0,
            padx=20,
            pady=20,
            sticky="nse"
        )



class App(customtkinter.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Reservation")
        self.geometry("800x480")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.input_frame  = InputFrame(self)
        self.input_frame.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )


        
        self.result_msg = customtkinter.CTkLabel(
            self,
            height=140,
            font=('Arial', 45),
            text="",
            fg_color="transparent"
        )
        self.result_msg.grid(
            row=1,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )

    def check_id(self, event):
        try:
            combined_url = f'{str(config["API_URL"])}/{str(config["DEVICE_NUM"])}/{self.input.get()}'
            print(f"code entered: {self.input.get()}")
            r = requests.get(combined_url, timeout=5)
            r.raise_for_status()
            print(r.text)
            self.result_msg.configure(text=r.text)
        except Exception as e:
            print(f"Error: {e}")
            self.result_msg.configure(text="網路錯誤")
        self.input.delete(0, customtkinter.END)


if __name__ == "__main__":
    app = App()
    app.mainloop()
import customtkinter
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
def button_callback():
    print("button pressed")


app = customtkinter.CTk()
app.title("Reservation")
app.geometry("640x360")
app.grid_columnconfigure(0, weight=1)


def check_id(event):
    try:
        r = requests.get(f'{str(config["API_URL"])}/{str(config["DEVICE_NUM"])}/{MainInput.get()}')
        ResultMsg.configure(text=r.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        ResultMsg.configure(text="網路錯誤")
    MainInput.delete(0, len(MainInput.get()))

DeviceLabel = customtkinter.CTkLabel(app, height=24, width=20, font=('Arial', 24), text=f'Device No.{str(config["DEVICE_NUM"])}', fg_color="transparent")
DeviceLabel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

MainInput = customtkinter.CTkEntry(app, height=90, width=20, font=('Arial', 90), placeholder_text="請刷卡")
MainInput.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
MainInput.bind("<Return>", check_id)
MainInput.focus_set()

ResultMsg = customtkinter.CTkLabel(app, height=140, font=('Arial', 45), text="", fg_color="transparent")
ResultMsg.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

if __name__ == "__main__":
    app.mainloop()
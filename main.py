import customtkinter
import requests
import argparse

def button_callback():
    print("button pressed")


app = customtkinter.CTk()
app.title("my app")
app.geometry("640x360")
app.grid_columnconfigure(0, weight=1)


def check_id(event):
    try:
        r = requests.get(f'http://127.0.0.1:8000/{str(device_num)}/{MainInput.get()}')
        ResultMsg.configure(text=r.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        ResultMsg.configure(text="網路錯誤")
    MainInput.delete(0, len(MainInput.get()))


MainInput = customtkinter.CTkEntry(app, height=140, width=20, font=('Arial', 90), placeholder_text="請刷卡")
MainInput.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
MainInput.bind("<Return>", check_id)

ResultMsg = customtkinter.CTkLabel(app, height=140, font=('Arial', 45), text="", fg_color="transparent")
ResultMsg.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a device number.')
    parser.add_argument('device_num', type=int, help='The device number to use')
    args = parser.parse_args()
    device_num = args.device_num

    app.mainloop()
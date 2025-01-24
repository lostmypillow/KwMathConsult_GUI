# main_app.py
import sys
import os
import sarasa_font
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import QTimer
from config import BASE_URL, REQUEST_TIMEOUT, FONT_PATH, FONT_SIZE, RESULTS_FONT_SIZE
from network_worker import NetworkWorker
from ui_creation import create_button, create_label, create_input, create_numpad
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("數輔刷卡")
        self.setGeometry(0, 0, 480, 320)

        # Set up the main UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)

        # Create input field for card number
        self.input = create_input(font_size=FONT_SIZE)
        self.layout.addWidget(self.input)
        self.input.returnPressed.connect(self.check_id)

        # Results label
        self.results = create_label("請刷卡或輸入卡號", font_size=RESULTS_FONT_SIZE)
        self.layout.addWidget(self.results)

        # Initialize numpad (can be toggled)
        self.numpad_frame = QWidget()
        self.numpad_layout = QGridLayout(self.numpad_frame)
        self.layout.addWidget(self.numpad_frame)
        self.numpad_frame.hide()
        self.is_kb_open = False
        self.init_numpad()

        # Initialize buttons
        self.buttons_frame = QWidget()
        self.buttons_layout = QGridLayout(self.buttons_frame)
        self.layout.addWidget(self.buttons_frame)
        self.init_buttons()

    def init_buttons(self):
        """Initialize buttons like delete, open keyboard, and confirm"""
        self.delete_btn = create_button("刪除", self.delete_digit)
        self.open_btn = create_button("開啟鍵盤", self.toggle_keyboard)
        self.confirm_btn = create_button("確認", self.check_id)

        self.buttons_layout.addWidget(self.delete_btn, 0, 0)
        self.buttons_layout.addWidget(self.open_btn, 0, 1)
        self.buttons_layout.addWidget(self.confirm_btn, 0, 2)

        self.delete_btn.hide()
        self.confirm_btn.hide()

    def init_numpad(self):
        """Initialize the numpad with keys"""
        keys = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0']
        ]
        create_numpad(self.numpad_layout, keys, self.type_key)

    def type_key(self, key):
        """Handle typing a key in the input field"""
        current_text = self.input.text()
        self.input.setText(current_text + key)

    def check_id(self):
        """Handles ID check and makes network request"""
        user_input = self.input.text()
        if user_input == "10369601":
            self.close()

        self.results.setText("處理中")
        combined_url = f'{BASE_URL}/{os.getenv("DEVICE_NUM")}/{user_input}'

        # Start network worker in a separate thread
        self.worker = NetworkWorker(combined_url)
        self.worker.result_ready.connect(self.handle_result)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.start()

    def handle_result(self, response_text):
        """Handle the response when the network request succeeds"""
        if "老師 刷卡成功" in response_text:
            name = response_text.split(' ')[0].replace("老師", "").replace('"', '')
            if name == self.teacher:
                self.teacher = ""
            else:
                self.teacher = f"老師: {name}\n\n"
        self.results.setText(response_text.replace('"', ''))
        QTimer.singleShot(3000, self.reset)

    def handle_error(self, error_message):
        """Handle errors in the network request"""
        print(f"Error: {error_message}")
        self.results.setText("刷卡失敗")
        QTimer.singleShot(3000, self.reset)

    def reset(self):
        """Resets the UI to initial state"""
        self.results.setText("請刷卡或輸入卡號")
        self.input.clear()

    def delete_digit(self):
        """Deletes a digit from the input field"""
        current_text = self.input.text()
        self.input.setText(current_text[:-1])

    def toggle_keyboard(self):
        """Toggles the on-screen keyboard"""
        if self.is_kb_open:
            self.numpad_frame.hide()
            self.results.show()
            self.is_kb_open = False
            self.open_btn.setText("開啟鍵盤")
        else:
            self.results.hide()
            self.delete_btn.show()
            self.confirm_btn.show()
            self.numpad_frame.show()
            self.is_kb_open = True
            self.open_btn.setText("收起鍵盤")

if __name__ == "__main__":
    # Set up application and global font
    app = QApplication(sys.argv)
    app.setStyle("Material")
    font_id = QFontDatabase.addApplicationFont(FONT_PATH)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    font = QFont(font_family)
    app.setFont(font)

    window = App()
    window.show()
    sys.exit(app.exec())

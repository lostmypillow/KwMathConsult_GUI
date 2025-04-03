import os
import logging
from typing import Optional
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QObject, Slot, QUrl, QByteArray, QTimer
from PySide6.QtGui import QGuiApplication
# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


class Controller(QObject):
    def __init__(self):
        super().__init__()

        # Initialize member variables
        self.engine: Optional[QQmlApplicationEngine] = None
        self.kb_btn: Optional[QObject] = None
        self.numpad_layout: Optional[QObject] = None
        self.main_text: Optional[QObject] = None
        self.teacher_text: Optional[QObject] = None
        self.id_input: Optional[QObject] = None

        self.network_manager = QNetworkAccessManager(self)
        self.current_reply = None

        self.numpad_timer = QTimer(self)
        self.numpad_timer.setSingleShot(True)
        self.numpad_timer.timeout.connect(self.auto_close_numpad)

    def set_engine(self, engine):
        """Store engine reference for UI control."""
        self.engine = engine

    @Slot(QObject)
    def initialize(self, root: QObject):
        """Find UI elements from QML."""

        # Get references to QML elements
        self.kb_btn = root.findChild(QObject, "kb_btn")
        self.numpad_layout = root.findChild(QObject, "numpad_layout")
        self.main_text = root.findChild(QObject, "main_text")
        self.teacher_text = root.findChild(QObject, "teacher_text")
        self.id_input: QObject = root.findChild(QObject, "id_input")

        if self.id_input:
            self.id_input.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Ensure that id_input regains focus if it loses it."""
        if obj == self.id_input and event.type() == 9:  # 9 = FocusOut event
            # Restore focus after a delay
            QTimer.singleShot(500, self.id_input.forceActiveFocus)
        return super().eventFilter(obj, event)

    @Slot(str)
    def handle_input(self, input_text):
        """Handle input text when Enter key is pressed."""
        if input_text:
            self.id_input.setProperty('text', '')
            if input_text == '10369601':
                QGuiApplication.quit()
            else:
                self.make_api_call(input_text)


# API Logic START

    def make_api_call(self, input_text):
        """Send API request without freezing UI."""
        url = QUrl()
        url.setScheme("http")
        url.setHost(str(os.getenv('SERVER_HOST')))
        url.setPort(int(os.getenv('SERVER_PORT')))
        url.setPath(f"/{str(os.getenv('DEVICE_ID'))}/{input_text}")
        logging.info(url)

        request = QNetworkRequest(url)
        self.current_reply = self.network_manager.get(request)
        self.main_text.setProperty('text', '處理中')

        # Set timeout for the request
        QTimer.singleShot(5000, self.abort_request)

        self.current_reply.finished.connect(self.handle_api_response)

    def abort_request(self):
        """Abort the API request if it times out."""
        if self.current_reply and self.current_reply.isRunning():
            logging.info("Request timed out.")
            self.current_reply.abort()

    def handle_api_response(self):
        """Handle the API response asynchronously."""
        if self.current_reply.error() != QNetworkReply.NoError:
            # Handle error response
            logging.error(
                f"Error: {self.current_reply.errorString()}, Code: {self.current_reply.error()}")
            self.main_text.setProperty('text', '刷卡失敗')
            QTimer.singleShot(
                3000, lambda: self.main_text.setProperty('text', '請刷卡或輸入卡號'))
            return
        else:
            # Process successful response
            response_data = self.current_reply.readAll().data()
            try:
                response_json = QByteArray(response_data).data().decode(
                    "utf-8").replace('"', "")
                logging.info(f"API Response:{response_json}")
                self.main_text.setProperty('text', response_json)

                if "老師" in response_json:
                    teacher_name = response_json.split(' ')[0]
                    if self.teacher_text.property('text') == teacher_name:
                        self.teacher_text.setProperty('text', '')
                    else:
                        self.teacher_text.setProperty('text', teacher_name)

                QTimer.singleShot(
                    3000, lambda: self.main_text.setProperty('text', '請刷卡或輸入卡號'))
            except Exception as e:
                logging.info(f"Error decoding response: {e}")
                self.main_text.setProperty('text', '刷卡失敗')
                QTimer.singleShot(
                    3000, lambda: self.main_text.setProperty('text', '請刷卡或輸入卡號'))

        # Reset input and refocus
        self.id_input.setProperty('text', '')
        self.id_input.forceActiveFocus()
        self.current_reply.deleteLater()
# API Logic END

# Numpad Logic START

    @Slot(str)
    def handle_numpad_click(self, button_text):
        """Handle numpad button clicks."""
        self.start_numpad_timer()
        current_input = self.id_input.property('text')

        if button_text != 'Del' and button_text != 'OK':
            self.id_input.setProperty('text', current_input + str(button_text))
        elif button_text == 'Del':
            self.id_input.setProperty('text', current_input[:-1])
        elif button_text == 'OK':
            self.toggle_numpad()
            self.handle_input(current_input)
        logging.info(f"Button pressed: {button_text}")

    @Slot()
    def toggle_numpad(self):
        """Toggle between numpad and results display."""
        if self.numpad_layout and self.main_text and self.teacher_text:
            numpad_visibility = self.numpad_layout.property("visible")
            self.numpad_layout.setProperty("visible", not numpad_visibility)

            new_numpad_text = "開啟鍵盤" if numpad_visibility else "關閉鍵盤"
            self.kb_btn.setProperty("text", new_numpad_text)

            self.main_text.setProperty("visible", numpad_visibility)
            self.teacher_text.setProperty("visible", numpad_visibility)

            # Start/stop timer based on numpad visibility
            if not numpad_visibility:
                self.start_numpad_timer()
            else:
                self.numpad_timer.stop()

    def start_numpad_timer(self):
        """Start a 10-second countdown to close the numpad automatically."""
        self.numpad_timer.start(10000)  # 10 seconds

    def auto_close_numpad(self):
        """Automatically close numpad after timer expires."""
        if self.numpad_layout and self.numpad_layout.property("visible"):
            self.toggle_numpad()
            self.id_input.setProperty('text', '')  # Close numpad
            logging.info("Numpad closed due to inactivity.")

# Numpad Logic END

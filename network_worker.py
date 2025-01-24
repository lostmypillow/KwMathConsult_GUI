# network_worker.py
import requests
from PySide6.QtCore import QThread, Signal

class NetworkWorker(QThread):
    result_ready = Signal(str)  # Signal to send back successful response
    error_occurred = Signal(str)  # Signal to send back error message

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        """Runs the network request in a separate thread"""
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()  # Will raise an exception for 4xx/5xx status codes
            self.result_ready.emit(response.text)  # Emit result if successful
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(str(e))  # Emit error message if request fails

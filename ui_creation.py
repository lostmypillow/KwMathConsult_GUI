# ui_widgets.py
from PySide6.QtWidgets import QPushButton, QLabel, QGridLayout, QVBoxLayout, QLineEdit, QWidget, QSizePolicy
from PySide6.QtCore import Qt

def create_button(text, callback, font_size=18):
    """Creates a button with given text, callback function, and font size"""
    button = QPushButton(text)
    button.font().setPointSize(font_size)  # Set font size
    button.clicked.connect(callback)
    return button

def create_label(text, font_size=18, alignment=Qt.AlignCenter):
    """Creates a label with given text, font size, and alignment"""
    label = QLabel(text)
    label.font().setPointSize(font_size)  # Set font size
    label.setAlignment(alignment)
    return label

def create_input(font_size):
    """Creates a QLineEdit widget for input with a specified font size"""
    input_field = QLineEdit()
    input_field.setFixedHeight(56)
    input_field.font().setPointSize(font_size)
    return input_field

def create_numpad(buttons_layout, keys, callback):
    """Creates a numpad using a grid layout with buttons filling the entire space"""
    # Determine the maximum number of columns
    max_cols = max(len(row) for row in keys)
    
    # Add buttons to the layout
    for r, row in enumerate(keys):
        for c, key in enumerate(row):
            btn = create_button(key, lambda checked, k=key: callback(k))
            # Set button size policy to expand
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            buttons_layout.addWidget(btn, r, c)

    # Add stretch to all rows and columns
    for r in range(len(keys)):
        buttons_layout.setRowStretch(r, 1)
    for c in range(max_cols):
        buttons_layout.setColumnStretch(c, 1)

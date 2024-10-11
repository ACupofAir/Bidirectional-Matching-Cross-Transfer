from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class InfoShowWidget(QWidget):
    def __init__(self, info_label="Info:", info_text="", label_bg_color="#000000", parent=None):
        super(InfoShowWidget, self).__init__(parent)
        self.initUI(info_label, info_text, label_bg_color)

    def initUI(self, info_label_text, info_text, label_bg_color):
        self.info_label = QLabel(info_label_text)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet(
            f"""
            QLabel {{
                font-size: 24px;                 /* 文字大小 */
                color: #ffffff;                  /* 文字颜色 */
                border: 2px solid {label_bg_color};       /* 边框样式 */
                border-top-left-radius: 10px;    /* 左上圆角 */
                border-bottom-left-radius: 10px; /* 左下圆角 */
                border-top-right-radius: 0px;    /* 右上圆角 */
                border-bottom-right-radius: 0px; /* 右下圆角 */
                padding: 10px;                   /* 内边距 */
                background-color: {label_bg_color};       /* 背景颜色 */
            }}
            """
        )

        self.info_text = QLabel(info_text)
        self.info_text.setAlignment(Qt.AlignCenter)
        self.info_text.setStyleSheet(
            f"""
            QLabel {{
                font-size: 24px;                 /* 文字大小 */
                color: #000000;                  /* 文字颜色 */
                border: 2px solid {label_bg_color};       /* 边框样式 */
                border-top-left-radius: 0px;     /* 左上圆角 */
                border-bottom-left-radius: 0px;  /* 左下圆角 */
                border-top-right-radius: 10px;   /* 右上圆角 */
                border-bottom-right-radius: 10px;/* 右下圆角 */
                padding: 10px;                   /* 内边距 */
                background-color: #f0f0f0;       /* 背景颜色 */
            }}
            """
        )

        info_layout = QHBoxLayout()
        info_layout.setSpacing(0)  # 去除两个组件之间的空隙
        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.info_text)

        self.setLayout(info_layout)

    def setText(self, text):
        self.info_text.setText(text)
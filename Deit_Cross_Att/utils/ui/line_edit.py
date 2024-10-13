from PyQt5.QtWidgets import QLineEdit


class AirLineEdit(QLineEdit):
    def __init__(
        self,
        text="",
        height=30,
        bg_color="#ffffff",
        font_color="#000000",
        font_size=None,
        parent=None,
    ):
        super(AirLineEdit, self).__init__(parent)
        self.bg_color = bg_color  # Default background color
        self.font_color = font_color  # Default font color
        self.font_size = font_size if font_size else f"{int(height * 0.8)}px"
        self.setFixedHeight(height)
        self.setPlaceholderText(text)
        self.setStyleSheet(self.style_sheet())

    def style_sheet(self):
        return f"""
            QLineEdit {{
                background-color: {self.bg_color}; /* 背景色 */
                color: {self.font_color};          /* 文字颜色 */
                border-radius: 7px;                /* 圆角半径 */
                border: 2px solid {self.bg_color}; /* 边框样式 */
                font-size: {self.font_size};       /* 文字大小 */
            }}
        """

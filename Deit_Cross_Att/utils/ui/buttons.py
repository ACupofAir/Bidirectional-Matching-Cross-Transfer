from PyQt5.QtWidgets import QPushButton


class AirBtn(QPushButton):
    def __init__(
        self,
        text,
        fixed_size=(160, 80),
        background_color="#000000",
        font_color="#ffffff",
        font_size="24px",
        parent=None,
    ):
        super(AirBtn, self).__init__(text, parent)
        self.fixed_size = fixed_size
        self.background_color = background_color
        self.font_color = font_color
        self.font_size = font_size
        self.initUI()

    def initUI(self):
        self.setFixedSize(*self.fixed_size)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.background_color}; /* 按钮背景色 */
                color: {self.font_color};                    /* 文字颜色 */
                border-radius: 7px;              /* 圆角半径 */
                border: 2px solid {self.background_color};       /* 边框样式 */
                font-size: {self.font_size};                 /* 文字大小 */
                padding: 10px 20px;              /* 内边距 */
            }}
            QPushButton:hover {{
                background-color: #45a049;       /* 鼠标悬停时的背景色 */
            }}
            QPushButton:pressed {{
                background-color: #3E8E41;       /* 按下按钮时的背景色 */
            }}
            """
        )

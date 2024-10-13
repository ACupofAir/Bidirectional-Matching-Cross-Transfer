from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor


class AirBtn(QPushButton):
    def __init__(
        self,
        text,
        fixed_size=(160, 80),
        font_size=None,
        background_color="#000000",
        font_color="#ffffff",
        parent=None,
    ):
        super(AirBtn, self).__init__(text, parent)
        self.fixed_size = fixed_size
        self.bg_color = background_color
        self.font_color = font_color
        self.font_size = font_size if font_size else f"{int(fixed_size[1] * 0.5)}px"
        self.hover_bg_color = self.calculate_hover_color(self.bg_color)
        self.initUI()

    def calculate_hover_color(self, color):
        qcolor = QColor(color)
        if qcolor == QColor("#000000"):
            # 如果颜色是纯黑色，使用一个默认的较亮颜色
            return QColor("#333333").name()
        else:
            # 提高亮度，生成提示色
            return qcolor.lighter(120).name()

    def initUI(self):
        self.setFixedSize(*self.fixed_size)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.bg_color}; /* 按钮背景色 */
                color: {self.font_color};          /* 文字颜色 */
                border-radius: 7px;                /* 圆角半径 */
                border: 2px solid {self.bg_color}; /* 边框样式 */
                font-size: {self.font_size};       /* 文字大小 */
                padding: 10px 20px;                /* 内边距 */
            }}
            QPushButton:hover {{
                background-color: {self.hover_bg_color}; /* 鼠标悬停时的背景色 */
                border: 2px solid {self.hover_bg_color}; /* 边框样式 */
            }}
            QPushButton:pressed {{
                background-color: {self.bg_color};       /* 按下按钮时的背景色 */
                border: 2px solid {self.bg_color}; /* 边框样式 */
            }}
            """
        )

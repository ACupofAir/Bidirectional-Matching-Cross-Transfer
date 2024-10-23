from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog
from .buttons import AirBtn
from .line_edit import AirLineEdit


class FileSelector(QWidget):

    def __init__(
        self,
        selector_text="未选择文件",
        default_file="",
        btn_text="选择",
        filetype="All Files (*)",
        height=50,
        parent=None,
    ):
        super(FileSelector, self).__init__(parent)
        self.selected_file = default_file
        self.height = height
        self.filetype = filetype
        self.file_box_text = selector_text if default_file == "" else default_file
        self.btn_text = btn_text
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()

        self.file_path_edit = AirLineEdit(
            text=self.file_box_text,
            height=self.height,
            font_size=f"{int(self.height * 0.5)}px",
            parent=self,
        )

        self.select_file_btn = AirBtn(
            text=self.btn_text, fixed_size=(self.height * 2, self.height), parent=self
        )
        self.select_file_btn.clicked.connect(self.open_file_dialog)

        self.layout.addWidget(self.file_path_edit)
        self.layout.addWidget(self.select_file_btn)

        self.setLayout(self.layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file",
            "",
            f"{self.filetype}",
            options=options,
        )
        if file_path:
            self.file_path_edit.setText(file_path)
            self.selected_file = file_path

    def get_selected_file(self):
        return self.selected_file


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = FileSelector()
    window.show()
    sys.exit(app.exec_())

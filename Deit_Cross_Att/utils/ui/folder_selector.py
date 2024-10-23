from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog
from .buttons import AirBtn
from .line_edit import AirLineEdit


class FolderSelector(QWidget):

    def __init__(
        self,
        selector_text="未选择文件夹",
        default_folder="",
        btn_text="选择",
        height=50,
        parent=None,
    ):
        super(FolderSelector, self).__init__(parent)
        self.selected_folder = default_folder
        self.height = height
        self.file_box_text = selector_text if default_folder == "" else default_folder
        self.btn_text = btn_text
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()

        self.folder_path_edit = AirLineEdit(
            text=self.file_box_text,
            height=self.height,
            font_size=f"{int(self.height * 0.5)}px",
            parent=self,
        )

        self.select_folder_btn = AirBtn(
            text=self.btn_text, fixed_size=(self.height * 2, self.height), parent=self
        )
        self.select_folder_btn.clicked.connect(self.open_folder_dialog)

        self.layout.addWidget(self.folder_path_edit)
        self.layout.addWidget(self.select_folder_btn)

        self.setLayout(self.layout)

    def open_folder_dialog(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select a folder",
            "",
            options=options,
        )
        if folder_path:
            self.folder_path_edit.setText(folder_path)
            self.selected_folder = folder_path

    def get_selected_folder(self):
        return self.selected_folder


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = FolderSelector()
    window.show()
    sys.exit(app.exec_())
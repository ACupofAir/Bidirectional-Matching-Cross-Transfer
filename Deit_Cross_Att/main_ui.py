import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
)
from train_ui import TrainInterface
from inference_ui import InferenceInterface


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Transfer Learning Software")

        # Set window size to 2/3 of the screen and center it
        screen = QApplication.desktop().screenGeometry()
        width, height = screen.width() * 2 // 3, screen.height() * 2 // 3
        self.setGeometry(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2,
            width,
            height,
        )

        # Layouts
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Buttons to switch between training and inference interfaces
        train_button = QPushButton("训练界面")
        train_button.clicked.connect(self.show_train_interface)
        inference_button = QPushButton("推理界面")
        inference_button.clicked.connect(self.show_inference_interface)

        button_layout.addWidget(train_button)
        button_layout.addWidget(inference_button)

        # Stacked widget to hold different interfaces
        self.stacked_widget = QStackedWidget()
        self.train_interface = TrainInterface()
        self.inference_interface = InferenceInterface()
        self.stacked_widget.addWidget(self.train_interface)
        self.stacked_widget.addWidget(self.inference_interface)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def show_train_interface(self):
        self.stacked_widget.setCurrentWidget(self.train_interface)

    def show_inference_interface(self):
        self.stacked_widget.setCurrentWidget(self.inference_interface)


if __name__ == "__main__":
    os.chdir(r"C:\Users\june\Workspace\Bidirectional-matching-cross-transfer\Deit_Cross_Att")
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

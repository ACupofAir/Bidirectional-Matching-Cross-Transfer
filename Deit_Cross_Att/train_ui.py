import sys
import os
import re
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QLabel,
    QComboBox,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QFrame,
    QDesktopWidget,
)
from PyQt5.QtCore import QProcess


class TrainInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Train Model")

        # Set window size to 2/3 of the screen and center it
        screen = QDesktopWidget().screenGeometry()
        width, height = screen.width() * 2 // 3, screen.height() * 2 // 3
        self.setGeometry(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2,
            width,
            height,
        )

        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_params_layout = QVBoxLayout()
        buttons_layout = QVBoxLayout()
        output_layout = QVBoxLayout()
        result_layout = QHBoxLayout()

        # First Module: Input Parameters
        model_label = QLabel("选择模型参数:")
        self.model_combobox = QComboBox()
        self.model_combobox.addItems(["deit_base", "deit_small"])

        epochs_label = QLabel("设置epochs:")
        self.epochs_spinbox = QSpinBox()
        self.epochs_spinbox.setRange(1, 1000)  # Set range for epochs
        self.epochs_spinbox.setValue(10)  # Set default value

        source_file_label = QLabel("选择源域文件:")
        self.source_file_display = QLabel("未选择文件")
        self.source_file_button = QPushButton("选择文件")
        self.source_file_button.setFixedSize(80, 40)
        self.source_file_button.clicked.connect(self.select_source_file)

        target_file_label = QLabel("选择目标域文件:")
        self.target_file_display = QLabel("未选择文件")
        self.target_file_button = QPushButton("选择文件")
        self.target_file_button.setFixedSize(80, 40)
        self.target_file_button.clicked.connect(self.select_target_file)

        self.train_button = QPushButton("训练")
        self.train_button.setFixedSize(50, 40)
        self.train_button.setStyleSheet("background-color: green; color: white;")
        self.train_button.clicked.connect(self.run_train_script)
        self.transfer_button = QPushButton("迁移")
        self.transfer_button.setFixedSize(50, 40)
        self.transfer_button.clicked.connect(self.run_transfer_script)

        input_params_layout.addWidget(model_label)
        input_params_layout.addWidget(self.model_combobox)

        epochs_layout = QHBoxLayout()
        epochs_layout.addWidget(epochs_label)
        epochs_layout.addWidget(self.epochs_spinbox)
        input_params_layout.addLayout(epochs_layout)

        source_file_layout = QHBoxLayout()
        source_file_layout.addWidget(self.source_file_display)
        source_file_layout.addWidget(self.source_file_button)
        input_params_layout.addWidget(source_file_label)
        input_params_layout.addLayout(source_file_layout)

        target_file_layout = QHBoxLayout()
        target_file_layout.addWidget(self.target_file_display)
        target_file_layout.addWidget(self.target_file_button)
        input_params_layout.addWidget(target_file_label)
        input_params_layout.addLayout(target_file_layout)

        buttons_layout.addWidget(self.train_button)
        buttons_layout.addWidget(self.transfer_button)

        input_layout.addLayout(input_params_layout)
        input_layout.addLayout(buttons_layout)

        # Second Module: Script Output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(QLabel("脚本输出:"))
        output_layout.addWidget(self.output_text)

        # Third Module: Final Accuracy and Export Model
        self.accuracy_label = QLabel("最终准确率:")
        self.export_button = QPushButton("导出模型")
        self.export_button.clicked.connect(self.export_model)

        # Add a red stop button to terminate training
        self.stop_button = QPushButton("终止训练")
        self.stop_button.setStyleSheet("background-color: red; color: white;")
        self.stop_button.clicked.connect(self.stop_training)

        result_layout.addWidget(self.accuracy_label)
        result_layout.addWidget(self.export_button)
        result_layout.addWidget(self.stop_button)

        # Add a line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        # Add layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(line)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(result_layout)

        self.setLayout(main_layout)

        # QProcess to run the script
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def select_source_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self,
            "选择源域文件",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )
        if file:
            self.source_file_path = file
            self.source_file_display.setText(file)

    def select_target_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self,
            "选择目标域文件",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )
        if file:
            self.target_file_path = file
            self.target_file_display.setText(file)

    def run_train_script(self):
        model = self.model_combobox.currentText()
        epochs = self.epochs_spinbox.value()
        if not self.source_file_path or not self.target_file_path:
            self.output_text.append("请提供源域和目标域文件路径")
            return

        cmd = (
            f"python train.py  --config_file configs/pretrain.yml DATASETS.NAMES Shipsear "
            f'OUTPUT_DIR "../logs/pretrain/{model}/shipsear/target" '
            f'DATASETS.ROOT_TRAIN_DIR "{self.source_file_path}" '
            f'DATASETS.ROOT_TEST_DIR "{self.target_file_path}" '
            f"SOLVER.LOG_PERIOD 10 "
            f"SOLVER.MAX_EPOCHS {epochs}"
        )
        self.process.start(cmd)

    def run_transfer_script(self):
        # Implement the transfer script logic here
        pass

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.output_text.append(stdout)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.output_text.append(stderr)

    def process_finished(self):
        self.output_text.append("脚本执行完成")
        # Extract the final accuracy from the last line of the output
        output_lines = self.output_text.toPlainText().split("\n")
        last_line = output_lines[-3] if len(output_lines) > 1 else output_lines[-1]
        match = re.search(r"Accuracy:\s*(\d+)%", last_line)
        if match:
            accuracy = match.group(1)
            self.accuracy_label.setText(f"最终准确率: {accuracy}%")

    def stop_training(self):
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.output_text.append("训练已终止")

    def export_model(self):
        # Implement the export model logic here
        pass


if __name__ == "__main__":
    os.chdir(
        r"C:\Users\june\Workspace\Bidirectional-matching-cross-transfer\Deit_Cross_Att"
    )
    app = QApplication(sys.argv)
    main_window = TrainInterface()
    main_window.show()
    sys.exit(app.exec_())

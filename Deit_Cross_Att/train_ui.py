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
    QTextEdit,
    QMessageBox,
    QFrame,
    QDesktopWidget,
)
from PyQt5.QtCore import QProcess, QTime, QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from utils.ui import AirBtn, InfoShowWidget, FileSelector


class TrainInterface(QWidget):
    def __init__(self):
        super().__init__()

        # Time log
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_display)
        self.elapsed_time = QTime(0, 0, 0)

        # Acc and loss log
        self.loss_data = []
        self.acc_data = []

        self.source_file_path = None
        self.target_file_path = None

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
        input_params_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()
        output_layout = QVBoxLayout()
        result_layout = QHBoxLayout()

        # First Module: Input Parameters
        model_label = QLabel("模型参数:")
        epochs_label = QLabel("epochs:")
        self.epochs_spinbox = QSpinBox()
        self.epochs_spinbox.setRange(1, 1000)  # Set range for epochs
        self.epochs_spinbox.setValue(10)  # Set default value

        batchsize_label = QLabel("batchsize:")
        self.batchsize_spinbox = QSpinBox()
        self.batchsize_spinbox.setRange(1, 1000)  # Set range for epochs
        self.batchsize_spinbox.setValue(32)  # Set default value

        self.source_file_selector = FileSelector(
            selector_text="未选择源域文件",
            default_file=r"E:\AirFTP\Datasets\DeepShip-Enh\mel-2.5\deepship-enh-2.5.txt",
            btn_text="选择",
            filetype="txt files (*.txt);;all files (*)",
            height=40,
        )
        self.target_file_selector = FileSelector(
            selector_text="未选择目标域文件",
            default_file=r"E:\AirFTP\Datasets\ShipsEar-Enh\mel\shipsear-enh.txt",
            btn_text="选择",
            filetype="txt files (*.txt);;all files (*)",
            height=40,
        )

        self.train_button = AirBtn("训练", fixed_size=(120, 40))
        self.train_button.clicked.connect(self.run_train_script)

        self.transfer_button = AirBtn("迁移", fixed_size=(120, 40))
        self.transfer_button.clicked.connect(self.run_transfer_script)

        epochs_layout = QHBoxLayout()
        epochs_layout.addWidget(epochs_label)
        epochs_layout.addWidget(self.epochs_spinbox)

        batchsize_layout = QHBoxLayout()
        batchsize_layout.addWidget(batchsize_label)
        batchsize_layout.addWidget(self.batchsize_spinbox)

        # input params: model_label, epochs_layout, source_file_layout, target_file_layout
        input_params_layout.addWidget(model_label)
        input_params_layout.addLayout(epochs_layout)
        input_params_layout.addLayout(batchsize_layout)
        input_params_layout.addWidget(self.source_file_selector)
        input_params_layout.addWidget(self.target_file_selector)

        buttons_layout.addWidget(self.train_button)
        buttons_layout.addWidget(self.transfer_button)

        input_layout.addLayout(input_params_layout)
        input_layout.addLayout(buttons_layout)

        # Second Module: Script Output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        output_layout.addWidget(self.canvas)
        output_layout.addWidget(QLabel("日志输出:"))
        output_layout.addWidget(self.output_text)

        # Third Module: Final Accuracy and Export Model
        self.accuracy_info_box = InfoShowWidget("准确率:", "0%")
        self.time_display_box = InfoShowWidget("耗时:", "0s")
        self.export_button = AirBtn("导出模型", fixed_size=(150, 50))
        self.export_button.clicked.connect(self.export_model)

        # Add a red stop button to terminate training
        self.stop_button = AirBtn(
            "终止训练", fixed_size=(150, 50), background_color="red"
        )
        self.stop_button.clicked.connect(self.stop_training)

        result_layout.addWidget(self.accuracy_info_box)
        result_layout.addWidget(self.time_display_box)
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

    def update_time_display(self):
        elapsed = self.elapsed_time.elapsed() // 1000
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.time_display_box.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def run_train_script(self):
        epochs = self.epochs_spinbox.value()
        batchsize = self.batchsize_spinbox.value()
        source_file_path = self.source_file_selector.get_selected_file()
        source_file_name = os.path.splitext(os.path.basename(source_file_path))[0]
        # target_file_path = self.target_file_selector.get_selected_file()
        if not source_file_path:
            QMessageBox.critical(self, "错误", "请提供源域文件路径")
            return

        cmd = (
            f"python train.py  --config_file configs/pretrain.yml DATASETS.NAMES Shipsear "
            f'OUTPUT_DIR "../logs/pretrain/{source_file_name}/bs{batchsize}-epoch{epochs}" '
            f'DATASETS.ROOT_TRAIN_DIR "{source_file_path}" '
            f'DATASETS.ROOT_TEST_DIR "{source_file_path}" '
            f"SOLVER.LOG_PERIOD 10 "
            f"SOLVER.IMS_PER_BATCH {batchsize} "
            f"SOLVER.MAX_EPOCHS {epochs}"
        )
        self.elapsed_time.start()
        self.timer.start(1000)  # Update every second
        self.process.start(cmd)

    def run_transfer_script(self):
        # Implement the transfer script logic here
        epochs = self.epochs_spinbox.value()
        batchsize = self.batchsize_spinbox.value()
        source_file_path = self.source_file_selector.get_selected_file()
        source_file_name = os.path.splitext(os.path.basename(source_file_path))[0]
        target_file_path = self.target_file_selector.get_selected_file()
        target_file_name = os.path.splitext(os.path.basename(target_file_path))[0]
        if not source_file_path or not target_file_path:
            QMessageBox.critical(self, "错误", "请提供源域和目标域文件路径")
            return

        cmd = (
            f"python train.py  --config_file configs/uda.yml "
            f"DATASETS.NAMES Shipsear "
            f"DATASETS.NAMES2 Shipsear "
            f'MODEL.PRETRAIN_PATH "../logs/pretrain/deit_base/shipsear/target/transformer_10.pth" '
            f'OUTPUT_DIR "../logs/uda/{source_file_name}-to-{target_file_name}/bs{batchsize}-epoch{epochs}" '
            f'DATASETS.ROOT_TRAIN_DIR "{source_file_path}" '
            f'DATASETS.ROOT_TRAIN_DIR2 "{target_file_path}" '
            f'DATASETS.ROOT_TEST_DIR "{target_file_path}" '
            f"SOLVER.LOG_PERIOD 10 "
            f"SOLVER.IMS_PER_BATCH {batchsize} "
            f"SOLVER.MAX_EPOCHS {epochs}"
        )
        self.elapsed_time.start()
        self.timer.start(1000)  # Update every second
        self.process.start(cmd)

    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(121)
        ax.plot(self.acc_data, label="Accuracy")
        ax.legend()
        ax = self.figure.add_subplot(122)
        ax.plot(self.loss_data, label="Loss", color="red")
        ax.legend()
        self.canvas.draw()

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.output_text.append(stdout)
        loss_match = re.search(r"Loss:\s*([\d.]+)", stdout)
        acc_match = re.search(r"Acc:\s*([\d.]+)", stdout)
        if loss_match and acc_match:
            loss = float(loss_match.group(1))
            acc = float(acc_match.group(1)) * 100
            self.loss_data.append(loss)
            self.acc_data.append(acc)
            self.update_plot()
            self.accuracy_info_box.setText(f"{acc:.2f}%")

    def handle_stderr(self):
        pass
        # data = self.process.readAllStandardError()
        # stderr = bytes(data).decode("utf8")
        # QMessageBox.critical(self, "错误", stderr)

    def process_finished(self):
        self.timer.stop()
        QMessageBox.information(self, "成功", "脚本执行完成")

    def stop_training(self):
        if self.process.state() == QProcess.Running:
            self.process.kill()
            QMessageBox.information(self, "成功", "脚本执行完成")

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

import sys
import os
import time
import torch
import torchvision.transforms as T
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QFrame,
    QLineEdit,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QProcess, Qt
from config import cfg
from model import make_model
from datasets.bases import load_image
from utils.ui import InfoShowWidget, AirBtn, FileSelector
from utils.audio2specgram import audiofile2specfile
import uuid


class InferenceInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Inference Interface")

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
        model_input_layout = QHBoxLayout()
        image_recognition_layout = QHBoxLayout()

        # First Module: Input Parameters
        self.checkpoint_input = FileSelector(
            selector_text="未选择模型文件:",
            btn_text="选择",
            filetype="PyTorch Model Files (*.pth)",
        )
        load_model_button = AirBtn(
            "加载", fixed_size=(100, 50), background_color="#13a460"
        )
        load_model_button.clicked.connect(self.load_model)

        self.audio_file_selector = FileSelector(
            selector_text="未选择音频文件:",
            btn_text="选择",
            filetype="Audio Files (*.wav)",
        )

        model_input_layout.addStretch()
        model_input_layout.addWidget(self.checkpoint_input)
        model_input_layout.addWidget(load_model_button)
        model_input_layout.addStretch()
        model_input_layout.addWidget(self.audio_file_selector)
        model_input_layout.addStretch()

        # Add a line separator
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)

        # Second Module: Single Image Inference
        # image input module
        self.image_box = QLabel("未选择音频时请点击选择图片")
        self.image_box.setAlignment(Qt.AlignCenter)
        self.image_box.setFixedSize(512, 512)
        self.image_box.setStyleSheet("border: 1px solid black;")
        self.image_box.setScaledContents(True)
        self.image_box.mousePressEvent = self.select_image_file

        image_input_layout = QVBoxLayout()
        image_input_layout.addWidget(self.image_box)

        # recognize button
        recognize_img_btn = AirBtn("识别图片", fixed_size=(200, 50))
        recognize_img_btn.clicked.connect(self.recognize_image)

        recognize_audio_btn = AirBtn("识别音频", fixed_size=(200, 50))
        recognize_audio_btn.clicked.connect(self.recognize_audio)

        # Add a line separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        self.result_info_widget = InfoShowWidget(
            info_label="结果", label_bg_color="#000000"
        )
        self.result_time_widget = InfoShowWidget(
            info_label="耗时", label_bg_color="#000000"
        )

        result_layout = QVBoxLayout()
        result_layout.setAlignment(Qt.AlignCenter)
        result_layout.addStretch()
        result_layout.addWidget(recognize_img_btn)
        result_layout.addWidget(recognize_audio_btn)
        result_layout.addStretch()
        result_layout.addWidget(line2)
        result_layout.addStretch()
        result_layout.addWidget(self.result_info_widget)
        result_layout.addWidget(self.result_time_widget)
        result_layout.addStretch()

        # All recognize image layout
        image_recognition_layout.setAlignment(Qt.AlignJustify)
        image_recognition_layout.addStretch()
        image_recognition_layout.addLayout(image_input_layout)
        image_recognition_layout.addStretch()
        image_recognition_layout.addLayout(result_layout)
        image_recognition_layout.addStretch()

        # Add layouts to main layout
        main_layout.addStretch()
        main_layout.addLayout(model_input_layout)
        main_layout.addStretch()
        main_layout.addWidget(line1)
        main_layout.addLayout(image_recognition_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Initialize model and device
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        config_file = "configs/pretrain.yml"
        checkpoint = self.checkpoint_input.get_selected_file()
        if not config_file or not checkpoint:
            QMessageBox.critical(self, "错误", "请提供模型文件路径")
            return

        cfg.merge_from_file(config_file)
        cfg.freeze()
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"

        self.model = make_model(cfg, num_class=4, camera_num=1, view_num=1)
        self.model.load_param_finetune(checkpoint)
        self.model.to(self.device)
        self.model.eval()
        QMessageBox.information(self, "提示", "模型加载成功")

    def select_image_file(self, event):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file",
            "",
            "Image Files (*.png *.jpg *.bmp);;All Files (*)",
            options=options,
        )
        if file_path:
            self.image_paths = [file_path]
            pixmap = QPixmap(self.image_paths[0])
            self.image_box.setPixmap(pixmap)

    def recognize_audio(self):
        if not self.model:
            QMessageBox.critical(self, "错误", "请先加载模型")
            return

        self.audio_path = self.audio_file_selector.get_selected_file()
        if not self.audio_path:
            QMessageBox.critical(self, "错误", "请先选择音频")
            return
        temp_filename = f"tmp_{uuid.uuid4().hex}.png"
        audiofile2specfile(self.audio_path, saved_path=temp_filename)
        pixmap = QPixmap(temp_filename)
        self.image_box.setPixmap(pixmap)
        self.recognize_image([temp_filename])
        os.remove(temp_filename)

    def recognize_image(self, image_paths=None):
        if not self.model:
            QMessageBox.critical(self, "错误", "请先加载模型")
            return

        if not image_paths:
            if not hasattr(self, "image_paths"):
                QMessageBox.critical(self, "错误", "请先选择图片")
                return
            else:
                image_paths = self.image_paths

        transforms = T.Compose(
            [
                T.Resize((256, 256)),
                T.CenterCrop((224, 224)),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        # Single Image Inference
        if len(image_paths) == 1:
            img = load_image(image_paths[0], transforms).to(self.device)
            img = img.unsqueeze(0)
            camids = torch.tensor([0]).to(self.device)
            target_view = torch.tensor([0]).to(self.device)

            inference_start_time = time.time()
            with torch.no_grad():
                probs = self.model(
                    img, cam_label=camids, view_label=target_view, return_logits=True
                )
                _, predicted = torch.max(probs, 1)

            inference_end_time = time.time()
            elapsed_time = (inference_end_time - inference_start_time) * 1000
            predicted_label = predicted.item()
            self.result_info_widget.setText(f"类别{predicted_label}")
            self.result_time_widget.setText(f"{elapsed_time:.2f}ms")
        else:  # Multiple Image Inference
            results = []
            for filename in os.listdir(image_paths):
                if filename.endswith((".png", ".jpg", ".bmp")):
                    img_path = os.path.join(self.image_paths, filename)
                    img = load_image(img_path, transforms).to(self.device)
                    img = img.unsqueeze(0)

                    with torch.no_grad():
                        output = self.model(img)
                        _, predicted = torch.max(output, 1)
                        results.append(f"{filename}: {predicted.item()}")
            result_file = os.path.join(image_paths, "results.txt")
            with open(result_file, "w") as f:
                f.write("\n".join(results))
            self.folder_result_label.setText(f"识别结果已保存到: {result_file}")


if __name__ == "__main__":
    os.chdir(
        r"C:\Users\june\Workspace\Bidirectional-matching-cross-transfer\Deit_Cross_Att"
    )
    app = QApplication(sys.argv)
    main_window = InferenceInterface()
    main_window.show()
    sys.exit(app.exec_())

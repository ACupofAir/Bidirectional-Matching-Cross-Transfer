import sys
import os
import torch
import torchvision.transforms as T
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QFrame,
    QLineEdit,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QProcess
from config import cfg
from model import make_model
from datasets.bases import load_image


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
        input_layout = QVBoxLayout()
        single_image_layout = QVBoxLayout()
        multi_image_layout = QVBoxLayout()

        # First Module: Input Parameters
        checkpoint_label = QLabel("模型路径:")
        self.checkpoint_input = QLineEdit()
        checkpoint_button = QPushButton("选择文件")
        checkpoint_button.clicked.connect(self.select_checkpoint_file)

        load_model_button = QPushButton("加载模型")
        load_model_button.clicked.connect(self.load_model)

        input_layout.addWidget(checkpoint_label)
        input_layout.addWidget(self.checkpoint_input)
        input_layout.addWidget(checkpoint_button)
        input_layout.addWidget(load_model_button)

        # Add a line separator
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)

        # Second Module: Single Image Inference
        single_image_label = QLabel("单张图片识别:")
        self.image_label = QLabel()
        self.image_label.setFixedSize(256, 256)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setScaledContents(True)
        self.image_label.mousePressEvent = self.select_image_file

        self.result_label = QLabel("识别结果:")
        self.result_text = QLabel("")

        recognize_button = QPushButton("识别")
        recognize_button.clicked.connect(self.recognize_image)

        single_image_layout.addWidget(single_image_label)
        single_image_layout.addWidget(self.image_label)
        single_image_layout.addWidget(recognize_button)
        single_image_layout.addWidget(self.result_label)
        single_image_layout.addWidget(self.result_text)

        # Add a line separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        # Third Module: Multiple Images Inference
        multi_image_label = QLabel("多张图片识别:")
        self.folder_input = QLineEdit()
        folder_button = QPushButton("选择文件夹")
        folder_button.clicked.connect(self.select_folder)

        recognize_folder_button = QPushButton("识别文件夹")
        recognize_folder_button.clicked.connect(self.recognize_folder)

        self.folder_result_label = QLabel("")

        multi_image_layout.addWidget(multi_image_label)
        multi_image_layout.addWidget(self.folder_input)
        multi_image_layout.addWidget(folder_button)
        multi_image_layout.addWidget(recognize_folder_button)
        multi_image_layout.addWidget(self.folder_result_label)

        # Add layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(line1)
        main_layout.addLayout(single_image_layout)
        main_layout.addWidget(line2)
        main_layout.addLayout(multi_image_layout)

        self.setLayout(main_layout)

        # Initialize model and device
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def select_checkpoint_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self,
            "选择检查点文件",
            "",
            "PyTorch Model Files (*.pth);;All Files (*)",
            options=options,
        )
        if file:
            self.checkpoint_input.setText(file)

    def load_model(self):
        config_file = "configs/pretrain.yml"
        checkpoint = self.checkpoint_input.text()
        if not config_file or not checkpoint:
            self.result_text.setText("请提供配置文件和检查点文件路径")
            return

        cfg.merge_from_file(config_file)
        cfg.freeze()
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"

        self.model = make_model(cfg, num_class=4, camera_num=1, view_num=1)
        self.model.load_param_finetune(checkpoint)
        self.model.to(self.device)
        self.model.eval()
        self.result_text.setText("模型加载成功")

    def select_image_file(self, event):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片文件",
            "",
            "Image Files (*.png *.jpg *.bmp);;All Files (*)",
            options=options,
        )
        if file:
            self.image_path = file
            pixmap = QPixmap(file)
            self.image_label.setPixmap(pixmap)

    def recognize_image(self):
        if not self.model:
            self.result_text.setText("请先加载模型")
            return

        if not hasattr(self, "image_path"):
            self.result_text.setText("请先选择图片")
            return

        transforms = T.Compose(
            [
                T.Resize((256, 256)),
                T.CenterCrop((224, 224)),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        img = load_image(self.image_path, transforms).to(self.device)
        img = img.unsqueeze(0)

        camids = torch.tensor([0]).to(self.device)
        target_view = torch.tensor([0]).to(self.device)

        with torch.no_grad():

            probs = self.model(img, cam_label=camids, view_label=target_view, return_logits=True)
            _, predicted = torch.max(probs, 1)
            self.result_text.setText(f"识别结果: {predicted.item()}")

    def select_folder(self):
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(
            self, "选择文件夹", "", options=options
        )
        if folder:
            self.folder_input.setText(folder)

    def recognize_folder(self):
        if not self.model:
            self.folder_result_label.setText("请先加载模型")
            return

        folder_path = self.folder_input.text()
        if not folder_path:
            self.folder_result_label.setText("请先选择文件夹")
            return

        transforms = T.Compose(
            [
                T.Resize((256, 256)),
                T.CenterCrop((224, 224)),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        results = []
        for filename in os.listdir(folder_path):
            if filename.endswith((".png", ".jpg", ".bmp")):
                img_path = os.path.join(folder_path, filename)
                img = load_image(img_path, transforms).to(self.device)
                img = img.unsqueeze(0)

                with torch.no_grad():
                    output = self.model(img)
                    _, predicted = torch.max(output, 1)
                    results.append(f"{filename}: {predicted.item()}")

        result_file = os.path.join(folder_path, "results.txt")
        with open(result_file, "w") as f:
            f.write("\n".join(results))

        self.folder_result_label.setText(f"识别结果已保存到: {result_file}")


if __name__ == "__main__":
    os.chdir(r"C:\Users\june\Workspace\Bidirectional-matching-cross-transfer\Deit_Cross_Att")
    app = QApplication(sys.argv)
    main_window = InferenceInterface()
    main_window.show()
    sys.exit(app.exec_())

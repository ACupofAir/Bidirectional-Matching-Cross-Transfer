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
from PyQt5.QtCore import QProcess, Qt
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
        model_input_layout = QHBoxLayout()
        image_recognition_layout = QHBoxLayout()

        # First Module: Input Parameters
        checkpoint_label = QLabel("模型路径:")
        self.checkpoint_input = QLineEdit()
        checkpoint_button = QPushButton("选择文件")
        checkpoint_button.clicked.connect(self.select_checkpoint_file)
        load_model_button = QPushButton("加载模型")
        load_model_button.clicked.connect(self.load_model)

        model_input_layout.addStretch()
        model_input_layout.addWidget(checkpoint_label)
        model_input_layout.addWidget(self.checkpoint_input)
        model_input_layout.addWidget(checkpoint_button)
        model_input_layout.addWidget(load_model_button)
        model_input_layout.addStretch()

        # Add a line separator
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)

        # Second Module: Single Image Inference
        # image input module
        single_image_label = QLabel("目标识别:")
        self.image_box = QLabel("点击选择图片")
        self.image_box.setAlignment(Qt.AlignCenter)
        self.image_box.setFixedSize(512, 512)
        self.image_box.setStyleSheet("border: 1px solid black;")
        self.image_box.setScaledContents(True)
        self.image_box.mousePressEvent = self.select_image_file

        image_input_layout = QVBoxLayout()
        image_input_layout.addWidget(single_image_label)
        image_input_layout.addWidget(self.image_box)

        # recognize button
        recognize_button = QPushButton("识别")
        recognize_button.clicked.connect(self.recognize_image)
        recognize_button.setFixedSize(160, 80)
        recognize_button.setStyleSheet("""
                    QPushButton {
                        background-color: #b4c3a8;       /* 按钮背景色 */
                        color: white;                    /* 文字颜色 */
                        border-radius: 7px;             /* 圆角半径 */
                        border: 2px solid #3E8E41;       /* 边框样式 */
                        font-size: 28px;                 /* 文字大小 */
                        padding: 10px 20px;              /* 内边距 */
                    }
                    QPushButton:hover {
                        background-color: #45a049;       /* 鼠标悬停时的背景色 */
                    }
                    QPushButton:pressed {
                        background-color: #3E8E41;       /* 按下按钮时的背景色 */
                    }
                """)
        # Add a line separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        # result show module
        self.result_label = QLabel("识别结果:")
        self.result_text = QLabel("")

        result_layout = QVBoxLayout()
        result_layout.setAlignment(Qt.AlignCenter)
        result_layout.addStretch()
        result_layout.addWidget(recognize_button)
        result_layout.addStretch()
        result_layout.addWidget(line2)
        result_layout.addStretch()
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.result_text)
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
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_dialog.setNameFilters(["Image Files (*.png *.jpg *.bmp)", "All Files (*)"])
        file_dialog.setViewMode(QFileDialog.Detail)

        if file_dialog.exec_():
            files = file_dialog.selectedFiles()
            if files:
                self.image_paths = files
                pixmap = QPixmap(self.image_paths[0])
                self.image_box.setPixmap(pixmap)

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

        if len(self.image_paths) == 1:
            img = load_image(self.image_paths[0], transforms).to(self.device)
            img = img.unsqueeze(0)
            camids = torch.tensor([0]).to(self.device)
            target_view = torch.tensor([0]).to(self.device)

            with torch.no_grad():

                probs = self.model(
                    img, cam_label=camids, view_label=target_view, return_logits=True
                )
                _, predicted = torch.max(probs, 1)
                self.result_text.setText(f"识别结果: {predicted.item()}")
        else:
            results = []
            for filename in os.listdir(self.image_paths):
                if filename.endswith((".png", ".jpg", ".bmp")):
                    img_path = os.path.join(self.image_paths, filename)
                    img = load_image(img_path, transforms).to(self.device)
                    img = img.unsqueeze(0)

                    with torch.no_grad():
                        output = self.model(img)
                        _, predicted = torch.max(output, 1)
                        results.append(f"{filename}: {predicted.item()}")
            result_file = os.path.join(self.image_paths, "results.txt")
            with open(result_file, "w") as f:
                f.write("\n".join(results))
            self.folder_result_label.setText(f"识别结果已保存到: {result_file}")


if __name__ == "__main__":
    os.chdir(
        r"C:\Users\timet\Workspace\Bidirectional-matching-cross-transfer\Deit_Cross_Att"
    )
    app = QApplication(sys.argv)
    main_window = InferenceInterface()
    main_window.show()
    sys.exit(app.exec_())

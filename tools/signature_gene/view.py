from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QMessageBox, QProgressBar, QSlider,
    QFileDialog, QColorDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor
from core.widgets import DropZone
from .controller import ImageController

#后台线程
class WorkerThread(QThread):
    finished=pyqtSignal(bool,str)

    def __init__(self,fn,*args,**kwargs):
        super().__init__()
        self._fn=fn
        self._args=args
        self._kwargs=kwargs

    def run(self):
        try:
            msg=self._fn(*self._args, **self._kwargs)
            self.finished.emit(True,msg)
        except Exception as e:
            self.finished.emit(False, str(e))

class ColorButton(QPushButton):
    def __init__(self, color: QColor = QColor(0, 0, 0), parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(32, 32)
        self.setObjectName("colorBtn")
        self._update_style()

    def mousePressEvent(self, event):
        picked = QColorDialog.getColor(self.color, self, "选择签名颜色")
        if picked.isValid():
            self.color = picked
            self._update_style()

    def _update_style(self):
        self.setStyleSheet(f"""
            QPushButton#colorBtn {{
                background: {self.color.name()};
                border: 2px solid #45475a;
                border-radius: 6px;
            }}
            QPushButton#colorBtn:hover {{ border-color: #89b4fa; }}
        """)

    def get_rgb(self):
        return self.color.red(), self.color.green(), self.color.blue()

#生成电子签名
class SignatureGene(QWidget):
    def __init__(self, controller: ImageController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._preview_path = None
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        self.drop = DropZone(
            "点击或拖拽图片文件",
            file_filter="Image Files (*.png *.jpg *.jpeg *.bmp)",
            extensions=[".png", ".jpg", ".jpeg", ".bmp"]
        )
        self.drop.setMinimumHeight(140)

        # ── 阈值滑块 ──
        threshold_row = QHBoxLayout()
        threshold_row.addWidget(QLabel("去背景阈值："))
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setRange(50, 250)
        self.threshold_slider.setValue(180)
        self.threshold_value_label = QLabel("180")
        self.threshold_value_label.setFixedWidth(30)
        self.threshold_slider.valueChanged.connect(
            lambda v: self.threshold_value_label.setText(str(v))
        )
        threshold_row.addWidget(self.threshold_slider)
        threshold_row.addWidget(self.threshold_value_label)

        # ── 签名颜色 ──
        color_row = QHBoxLayout()
        color_row.addWidget(QLabel("签名颜色："))
        self.color_btn = ColorButton(QColor(0, 0, 0))
        color_row.addWidget(self.color_btn)
        color_row.addStretch()

        # ── 预览区 ──
        self.preview_label = QLabel("处理后预览将显示在这里")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setObjectName("previewLabel")
        self.preview_label.setMinimumHeight(160)

        # ── 按钮 ──
        btn_row = QHBoxLayout()
        self.btn_preview = QPushButton("预览效果")
        self.btn_preview.setObjectName("secondaryBtn")
        self.btn_save = QPushButton("保存签名 PNG")
        self.btn_save.setObjectName("primaryBtn")
        self.btn_save.setEnabled(False)
        btn_row.addWidget(self.btn_preview)
        btn_row.addWidget(self.btn_save)

        self.progress = QProgressBar()
        self.progress.setVisible(False)

        # ── 组装 ──
        layout.addWidget(QLabel("✍️  生成电子签名"))
        layout.addWidget(self.drop)
        layout.addLayout(threshold_row)
        layout.addLayout(color_row)
        layout.addWidget(self.preview_label)
        layout.addLayout(btn_row)
        layout.addWidget(self.progress)
        layout.addStretch()

        self.btn_preview.clicked.connect(self._run_preview)
        self.btn_save.clicked.connect(self._save)

    def _run_preview(self):
        if not self.drop.files:
            QMessageBox.warning(self, "提示", "请先选择一张图片")
            return
        import tempfile, os
        self._preview_path = os.path.join(tempfile.gettempdir(), "_sig_preview.png")
        self.btn_preview.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker = WorkerThread(
            self.controller.process_signature,
            self.drop.files[0],
            self._preview_path,
            self.threshold_slider.value(),
            self.color_btn.get_rgb()
        )
        self._worker.finished.connect(self._on_preview_done)
        self._worker.start()

    def _on_preview_done(self, ok, msg):
        self.btn_preview.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            pixmap = QPixmap(self._preview_path)
            self.preview_label.setPixmap(
                pixmap.scaled(
                    self.preview_label.width(),
                    self.preview_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            self.btn_save.setEnabled(True)
        else:
            QMessageBox.critical(self, "错误", msg)

    def _save(self):
        if not self._preview_path:
            return
        out, _ = QFileDialog.getSaveFileName(
            self, "保存签名", "signature.png", "PNG Files (*.png)"
        )
        if not out:
            return
        import shutil
        shutil.copy(self._preview_path, out)
        QMessageBox.information(self, "完成", f"签名已保存 → {out}")

class SignatureWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ImageController()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(SignatureGene(self.controller))

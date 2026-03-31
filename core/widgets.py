from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class DropZone(QFrame):
    def __init__(self, text="点击或拖拽文件到此处", multi=False,
                 file_filter="All Files (*)", extensions=None, parent=None):
        """
        file_filter : QFileDialog 过滤字符串，例如：
                      "PDF Files (*.pdf)"
                      "Image Files (*.png *.jpg *.jpeg *.bmp)"
        extensions  : 拖拽时校验的后缀列表，例如：
                      [".pdf"]
                      [".png", ".jpg", ".jpeg", ".bmp"]
                      传 None 则不校验后缀，接受所有文件
        """
        super().__init__(parent)
        self.multi = multi
        self.file_filter = file_filter
        self.extensions = extensions
        self.files = []
        self.setAcceptDrops(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("dropZone")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon_label = QLabel("📂")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFont(QFont("Segoe UI Emoji", 28))

        self.hint_label = QLabel(text)
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setObjectName("hintLabel")

        self.file_label = QLabel("")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setObjectName("fileLabel")
        self.file_label.setWordWrap(True)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.hint_label)
        layout.addWidget(self.file_label)

    def _match(self, path: str) -> bool:
        if not self.extensions:
            return True
        return any(path.lower().endswith(ext) for ext in self.extensions)

    def mousePressEvent(self, event):
        if self.multi:
            paths, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", self.file_filter)
        else:
            path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", self.file_filter)
            paths = [path] if path else []
        if paths:
            self._set_files(paths)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        paths = [
            u.toLocalFile() for u in event.mimeData().urls()
            if self._match(u.toLocalFile())
        ]
        if paths:
            self._set_files(paths if self.multi else [paths[0]])

    def _set_files(self, paths):
        self.files = paths
        if len(paths) == 1:
            self.file_label.setText(paths[0].split("/")[-1].split("\\")[-1])
        else:
            self.file_label.setText(f"已选择 {len(paths)} 个文件")
        self.icon_label.setText("✅")

    def clear(self):
        self.files = []
        self.icon_label.setText("📂")
        self.file_label.setText("")
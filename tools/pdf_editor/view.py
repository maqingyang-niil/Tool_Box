from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QListWidget, QListWidgetItem,
    QStackedWidget, QFrame, QLineEdit, QSpinBox,
    QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon
from .controller import PdfController

#后台线性
class WorkerThread(QThread):
    finished=pyqtSignal(bool,str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            msg = self._fn(*self._args, **self._kwargs)
            self.finished.emit(True, msg or "操作成功！")
        except Exception as e:
            self.finished.emit(False, str(e))


# ── 通用：带虚线边框的文件拖放区 ────────────────────────────────────
class DropZone(QFrame):
    def __init__(self, text="点击或拖拽文件到此处", multi=False, parent=None):
        super().__init__(parent)
        self.multi = multi
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

    def mousePressEvent(self, event):
        if self.multi:
            paths, _ = QFileDialog.getOpenFileNames(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
            paths = [path] if path else []
        if paths:
            self._set_files(paths)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        paths = [u.toLocalFile() for u in event.mimeData().urls() if u.toLocalFile().endswith(".pdf")]
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


# ── 合并 PDF 页面 ────────────────────────────────────────────────────
class MergePage(QWidget):
    def __init__(self, controller: PdfController, parent=None):
        super().__init__(parent)
        self.controller = controller
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        self.drop = DropZone("点击或拖拽多个 PDF 文件", multi=True)
        self.drop.setMinimumHeight(140)

        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(120)
        self.list_widget.setObjectName("fileList")

        btn_row = QHBoxLayout()
        self.btn_up = QPushButton("↑ 上移")
        self.btn_down = QPushButton("↓ 下移")
        self.btn_del = QPushButton("✕ 移除")
        for b in (self.btn_up, self.btn_down, self.btn_del):
            b.setObjectName("secondaryBtn")
            btn_row.addWidget(b)

        self.btn_run = QPushButton("合并 PDF")
        self.btn_run.setObjectName("primaryBtn")

        self.progress = QProgressBar()
        self.progress.setVisible(False)

        layout.addWidget(QLabel("📎  选择要合并的 PDF（可调整顺序）"))
        layout.addWidget(self.drop)
        layout.addWidget(self.list_widget)
        layout.addLayout(btn_row)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addStretch()

        self.drop.mousePressEvent = self._on_drop_click
        self.drop.dropEvent = self._on_drop_drop
        self.btn_run.clicked.connect(self._run)
        self.btn_up.clicked.connect(self._move_up)
        self.btn_down.clicked.connect(self._move_down)
        self.btn_del.clicked.connect(self._remove)

    def _on_drop_click(self, event):
        paths, _ = QFileDialog.getOpenFileNames(self, "选择 PDF", "", "PDF Files (*.pdf)")
        if paths:
            self._add_files(paths)

    def _on_drop_drop(self, event):
        paths = [u.toLocalFile() for u in event.mimeData().urls() if u.toLocalFile().endswith(".pdf")]
        self._add_files(paths)

    def _add_files(self, paths):
        for p in paths:
            name = p.split("/")[-1].split("\\")[-1]
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, p)
            self.list_widget.addItem(item)

    def _move_up(self):
        row = self.list_widget.currentRow()
        if row > 0:
            item = self.list_widget.takeItem(row)
            self.list_widget.insertItem(row - 1, item)
            self.list_widget.setCurrentRow(row - 1)

    def _move_down(self):
        row = self.list_widget.currentRow()
        if row < self.list_widget.count() - 1:
            item = self.list_widget.takeItem(row)
            self.list_widget.insertItem(row + 1, item)
            self.list_widget.setCurrentRow(row + 1)

    def _remove(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.list_widget.takeItem(row)

    def _run(self):
        paths = [self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
                 for i in range(self.list_widget.count())]
        if len(paths) < 2:
            QMessageBox.warning(self, "提示", "请至少选择 2 个 PDF 文件")
            return
        out, _ = QFileDialog.getSaveFileName(self, "保存合并结果", "merged.pdf", "PDF Files (*.pdf)")
        if not out:
            return
        self._start_worker(self.controller.merge, paths, out)

    def _start_worker(self, fn, *args):
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker = WorkerThread(fn, *args)
        self._worker.finished.connect(self._on_done)
        self._worker.start()

    def _on_done(self, ok, msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            QMessageBox.information(self, "完成", msg)
        else:
            QMessageBox.critical(self, "错误", msg)


# ── 拆分 PDF 页面 ────────────────────────────────────────────────────
class SplitPage(QWidget):
    def __init__(self, controller: PdfController, parent=None):
        super().__init__(parent)
        self.controller = controller
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        self.drop = DropZone("点击或拖拽一个 PDF 文件")
        self.drop.setMinimumHeight(140)

        range_row = QHBoxLayout()
        range_row.addWidget(QLabel("页码范围（如 1-3,5,7-9）："))
        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("留空则每页单独拆分")
        range_row.addWidget(self.range_input)

        self.btn_run = QPushButton("拆分 PDF")
        self.btn_run.setObjectName("primaryBtn")
        self.progress = QProgressBar()
        self.progress.setVisible(False)

        layout.addWidget(QLabel("✂️  拆分 PDF"))
        layout.addWidget(self.drop)
        layout.addLayout(range_row)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addStretch()

        self.btn_run.clicked.connect(self._run)

    def _run(self):
        if not self.drop.files:
            QMessageBox.warning(self, "提示", "请先选择一个 PDF 文件")
            return
        out_dir = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if not out_dir:
            return
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker = WorkerThread(
            self.controller.split,
            self.drop.files[0],
            out_dir,
            self.range_input.text().strip()
        )
        self._worker.finished.connect(self._on_done)
        self._worker.start()

    def _on_done(self, ok, msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            QMessageBox.information(self, "完成", msg)
        else:
            QMessageBox.critical(self, "错误", msg)

# ── 主 Widget ────────────────────────────────────────────────────────
class PdfEditorWidget(QWidget):
    """PDF 编辑器主界面，左侧导航 + 右侧功能页"""

    STYLE = """
        QWidget {
            background: #1e1e2e;
            color: #cdd6f4;
            font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
            font-size: 14px;
        }
        /* 左侧导航 */
        #navPanel {
            background: #181825;
            border-right: 1px solid #313244;
        }
        #navTitle {
            color: #89b4fa;
            font-size: 16px;
            font-weight: bold;
            padding: 20px 16px 8px 16px;
        }
        #navBtn {
            text-align: left;
            padding: 10px 20px;
            border: none;
            background: transparent;
            color: #a6adc8;
            font-size: 14px;
            border-radius: 6px;
            margin: 2px 8px;
        }
        #navBtn:hover    { background: #313244; color: #cdd6f4; }
        #navBtn:checked  { background: #45475a; color: #89b4fa; font-weight: bold; }
        /* 拖放区 */
        #dropZone {
            border: 2px dashed #45475a;
            border-radius: 12px;
            background: #181825;
        }
        #dropZone:hover { border-color: #89b4fa; }
        #hintLabel { color: #6c7086; font-size: 13px; }
        #fileLabel  { color: #a6e3a1; font-size: 13px; margin-top: 4px; }
        /* 按钮 */
        #primaryBtn {
            background: #89b4fa;
            color: #1e1e2e;
            border: none;
            border-radius: 8px;
            padding: 10px 0;
            font-size: 14px;
            font-weight: bold;
        }
        #primaryBtn:hover    { background: #b4befe; }
        #primaryBtn:disabled { background: #45475a; color: #6c7086; }
        #secondaryBtn {
            background: #313244;
            color: #cdd6f4;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
        }
        #secondaryBtn:hover { background: #45475a; }
        /* 文件列表 */
        #fileList {
            background: #181825;
            border: 1px solid #313244;
            border-radius: 8px;
            color: #cdd6f4;
        }
        /* 输入框 */
        QLineEdit, QSpinBox {
            background: #181825;
            border: 1px solid #45475a;
            border-radius: 6px;
            padding: 6px 10px;
            color: #cdd6f4;
        }
        QLineEdit:focus, QSpinBox:focus { border-color: #89b4fa; }
        /* 进度条 */
        QProgressBar {
            background: #313244;
            border-radius: 4px;
            height: 6px;
            text-align: center;
        }
        QProgressBar::chunk { background: #89b4fa; border-radius: 4px; }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(self.STYLE)
        self.controller = PdfController()

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── 左侧导航 ──
        nav = QFrame()
        nav.setObjectName("navPanel")
        nav.setFixedWidth(160)
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)

        title = QLabel("PDF 编辑器")
        title.setObjectName("navTitle")
        nav_layout.addWidget(title)

        self.nav_buttons = []
        pages_info = [
            ("📎  合并", MergePage),
            ("✂️  拆分", SplitPage),
        ]

        self.stack = QStackedWidget()
        for i, (label, PageClass) in enumerate(pages_info):
            btn = QPushButton(label)
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, idx=i: self._switch(idx))
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.stack.addWidget(PageClass(self.controller))

        nav_layout.addStretch()

        root.addWidget(nav)
        root.addWidget(self.stack)

        self._switch(0)

    def _switch(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
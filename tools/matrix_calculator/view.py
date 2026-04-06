from PyQt6.QtWidgets import (
    QWidget,QHBoxLayout, QPushButton,
    QMessageBox, QProgressBar,QFrame,QStackedWidget,
    QLabel, QVBoxLayout, QTextEdit
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFont
import numpy as np
from .controller import MatrixController

def parse_matrix(matrix_str:str)->np.ndarray:
    rows = [row.strip() for row in matrix_str.strip().split(";")]
    matrix = []
    for row in rows:
        if row:
            matrix.append([float(x) for x in row.split()])
    result = np.array(matrix)
    if result.ndim != 2:
        raise ValueError("矩阵格式不正确")
    return result

class WorkerThread(QThread):
    finished = pyqtSignal(bool,object)

    def __init__(self,fn,*args,**kwargs):
        super().__init__()
        self._fn=fn
        self._args=args
        self._kwargs=kwargs

    def run(self):
        try:
            msg=self._fn(*self._args,**self._kwargs)
            self.finished.emit(True,msg)
        except Exception as e:
            self.finished.emit(False,str(e))

# ── 通用：矩阵输入区 ─────────────────────────────────────────────────
def make_matrix_input(label: str) -> tuple:
    """返回 (layout, QTextEdit)"""
    layout = QVBoxLayout()
    layout.addWidget(QLabel(label))
    text_edit = QTextEdit()
    text_edit.setPlaceholderText("例如：1 2; 3 4")
    text_edit.setFixedHeight(80)
    text_edit.setObjectName("matrixInput")
    layout.addWidget(text_edit)
    return layout, text_edit
 
 
# ── 通用：结果显示区 ─────────────────────────────────────────────────
def make_result_area() -> tuple:
    """返回 (layout, QLabel)"""
    layout = QVBoxLayout()
    layout.addWidget(QLabel("计算结果："))
    result_label = QLabel("")
    result_label.setObjectName("resultLabel")
    result_label.setWordWrap(True)
    result_label.setFont(QFont("Courier New", 12))
    result_label.setMinimumHeight(80)
    layout.addWidget(result_label)
    return layout, result_label
 
 
# ── 格式化矩阵输出 ───────────────────────────────────────────────────
def format_matrix(result) -> str:
    if isinstance(result, np.ndarray):
        if result.ndim == 1:
            return "  ".join(f"{v:.4f}" for v in result)
        rows = []
        for row in result:
            rows.append("  ".join(f"{v:.4f}" for v in row))
        return "\n".join(rows)
    elif isinstance(result, float):
        return f"{result:.6f}"
    return str(result)
 
 
# ── 双矩阵运算页面基类 ───────────────────────────────────────────────
class TwoMatrixPage(QWidget):
    def __init__(self, controller: MatrixController, title: str, fn, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.fn = fn
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
 
        layout.addWidget(QLabel(title))
 
        a_layout, self.a_input = make_matrix_input("矩阵 A：")
        b_layout, self.b_input = make_matrix_input("矩阵 B：")
        layout.addLayout(a_layout)
        layout.addLayout(b_layout)
 
        self.btn_run = QPushButton("计算")
        self.btn_run.setObjectName("primaryBtn")
        self.progress = QProgressBar()
        self.progress.setVisible(False)
 
        result_layout, self.result_label = make_result_area()
 
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addLayout(result_layout)
        layout.addStretch()
 
        self.btn_run.clicked.connect(self._run)
 
    def _run(self):
        try:
            A = parse_matrix(self.a_input.toPlainText())
            B = parse_matrix(self.b_input.toPlainText())
        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
            return
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker = WorkerThread(self.fn, A, B)
        self._worker.finished.connect(self._on_done)
        self._worker.start()
 
    def _on_done(self, ok, msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            self.result_label.setText(format_matrix(msg))
        else:
            QMessageBox.critical(self, "错误", msg)
 
 
# ── 单矩阵运算页面基类 ───────────────────────────────────────────────
class OneMatrixPage(QWidget):
    def __init__(self, controller: MatrixController, title: str, fn, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.fn = fn
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
 
        layout.addWidget(QLabel(title))
 
        a_layout, self.a_input = make_matrix_input("矩阵 A：")
        layout.addLayout(a_layout)
 
        self.btn_run = QPushButton("计算")
        self.btn_run.setObjectName("primaryBtn")
        self.progress = QProgressBar()
        self.progress.setVisible(False)
 
        result_layout, self.result_label = make_result_area()
 
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addLayout(result_layout)
        layout.addStretch()
 
        self.btn_run.clicked.connect(self._run)
 
    def _run(self):
        try:
            A = parse_matrix(self.a_input.toPlainText())
        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
            return
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker = WorkerThread(self.fn, A)
        self._worker.finished.connect(self._on_done)
        self._worker.start()
 
    def _on_done(self, ok, msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            self.result_label.setText(format_matrix(msg))
        else:
            QMessageBox.critical(self, "错误", msg)
 
 
# ── 主 Widget ────────────────────────────────────────────────────────
class MatrixWidget(QWidget):
    """矩阵计算主界面，左侧导航 + 右侧功能页"""
 
    STYLE = """
        QWidget {
            background: #1e1e2e;
            color: #cdd6f4;
            font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
            font-size: 14px;
        }
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
        #navBtn:hover   { background: #313244; color: #cdd6f4; }
        #navBtn:checked { background: #45475a; color: #89b4fa; font-weight: bold; }
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
        #matrixInput {
            background: #181825;
            border: 1px solid #45475a;
            border-radius: 6px;
            padding: 6px 10px;
            color: #cdd6f4;
            font-family: "Courier New", monospace;
        }
        #matrixInput:focus { border-color: #89b4fa; }
        #resultLabel {
            background: #181825;
            border: 1px solid #313244;
            border-radius: 8px;
            padding: 12px;
            color: #a6e3a1;
        }
        QProgressBar {
            background: #313244;
            border-radius: 4px;
            height: 6px;
        }
        QProgressBar::chunk { background: #89b4fa; border-radius: 4px; }
    """
 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(self.STYLE)
        self.controller = MatrixController()
 
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
 
        title = QLabel("矩阵计算")
        title.setObjectName("navTitle")
        nav_layout.addWidget(title)
 
        self.nav_buttons = []
        pages_info = [
            ("➕  相加",   TwoMatrixPage, "矩阵相加",   self.controller.add_matrices),
            ("➖  相减",   TwoMatrixPage, "矩阵相减",   self.controller.sub_matrices),
            ("✖️  相乘",   TwoMatrixPage, "矩阵相乘",   self.controller.multiply_matrices),
            ("🔄  转置",   OneMatrixPage, "矩阵转置",   self.controller.transpose_matrix),
            ("🔁  求逆",   OneMatrixPage, "矩阵求逆",   self.controller.inverse_matrix),
            ("📐  行列式", OneMatrixPage, "计算行列式", self.controller.determinant_matrix),
            ("λ  特征值", OneMatrixPage, "计算特征值", self.controller.compute_eigenvalues),
            ("v  特征向量", OneMatrixPage, "计算特征向量", self.controller.compute_eigenvectors),
        ]
 
        self.stack = QStackedWidget()
        for i, info in enumerate(pages_info):
            nav_label, PageClass, page_title, fn = info
            btn = QPushButton(nav_label)
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, idx=i: self._switch(idx))
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.stack.addWidget(PageClass(self.controller, page_title, fn))
 
        nav_layout.addStretch()
 
        root.addWidget(nav)
        root.addWidget(self.stack)
 
        self._switch(0)
 
    def _switch(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
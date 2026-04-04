from PyQt6.QtWidgets import (
    QWidget,QHBoxLayout, QPushButton,
    QLineEdit,
    QMessageBox, QProgressBar,QFrame,QStackedWidget
)
from PyQt6.QtCore import QThread, pyqtSignal
from .controller import ControlController
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap,QPixmapCache
class WorkerThread(QThread):
    finished = pyqtSignal(bool,str)

    def __init__(self,fn,*args,**kwargs):
        super().__init__()
        self._fn=fn
        self._args=args
        self._kwargs=kwargs

    def run(self):
        try:
            msg=self._fn(*self._args,**self._kwargs)
            self.finished.emit(True,msg or "操作成功")
        except Exception as e:
            self.finished.emit(False,str(e))

class GetPoles(QWidget):
    def __init__(self,controller:ControlController,parent=None):
        super().__init__(parent)
        self.controller=controller
        layout=QVBoxLayout(self)
        layout.setSpacing(16)

        num_row=QHBoxLayout()
        num_row.addWidget(QLabel("输入分子系数："))
        self.num_input=QLineEdit()
        num_row.addWidget(self.num_input)

        den_row=QHBoxLayout()
        den_row.addWidget(QLabel("输入分母系数："))
        self.den_input=QLineEdit()
        den_row.addWidget(self.den_input)

        self.btn_run=QPushButton("生成根位置图")
        self.btn_run.setObjectName("primaryBtn")
        self.progress=QProgressBar()
        self.progress.setVisible(False)

        layout.addWidget(QLabel("获取闭环特征根"))
        layout.addLayout(num_row)
        layout.addLayout(den_row)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addStretch()

        self.btn_run.clicked.connect(self._run)

    def _run(self):
        num_input=self.num_input.text()
        den_input=self.den_input.text()
        try:
            num_list=[float(x) for x in num_input.split()]
            den_list=[float(x) for x in den_input.split()]
        except ValueError:
            QMessageBox.warning(self,"错误","请输入有效的数字")
            return
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker=WorkerThread(
            self.controller.get_polar,
            num_list,
            den_list
        )

        self._worker.finished.connect(self._on_done)
        self._worker.start()

    def _on_done(self,ok,msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            QPixmapCache.clear()
            dialog = QDialog(self)
            dialog.setWindowTitle("根分布图")
            layout = QVBoxLayout(dialog)
            _label = QLabel()
            _label.setPixmap(QPixmap(msg))
            layout.addWidget(_label)
            dialog.exec()
        else:
            QMessageBox.critical(self,"错误",msg)

class RootLocus(QWidget):
    def __init__(self,controller:ControlController,parent=None):
        super().__init__(parent)
        self.controller=controller
        layout=QVBoxLayout(self)
        layout.setSpacing(16)

        num_row=QHBoxLayout()
        num_row.addWidget(QLabel("输入分子系数："))
        self.num_input=QLineEdit()
        num_row.addWidget(self.num_input)

        den_row=QHBoxLayout()
        den_row.addWidget(QLabel("输入分母系数："))
        self.den_input=QLineEdit()
        den_row.addWidget(self.den_input)

        self.btn_run=QPushButton("生成根轨迹图")
        self.btn_run.setObjectName("primaryBtn")
        self.progress=QProgressBar()
        self.progress.setVisible(False)

        layout.addWidget(QLabel("绘制根轨迹"))
        layout.addLayout(num_row)
        layout.addLayout(den_row)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addStretch()
        self.btn_run.clicked.connect(self._run)

    def _run(self):
        num_input=self.num_input.text()
        den_input=self.den_input.text()
        try:
            num_list=[float(x) for x in num_input.split()]
            den_list=[float(x) for x in den_input.split()]
        except ValueError:
            QMessageBox.warning(self,"错误","请输入有效数字")
            return
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0,0)
        self._worker=WorkerThread(
            self.controller.root_locus,
            num_list,
            den_list
        )
        self._worker.finished.connect(self._on_done)
        self._worker.start()

    def _on_done(self,ok,msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            QPixmapCache.clear()
            dialog = QDialog(self)
            dialog.setWindowTitle("根轨迹图")
            layout = QVBoxLayout(dialog)
            _label = QLabel()
            _label.setPixmap(QPixmap(msg))
            layout.addWidget(_label)
            dialog.exec()
        else:
            QMessageBox.critical(self, "错误", msg)

class BodeGraph(QWidget):
    def __init__(self,controller:ControlController,parent=None):
        super().__init__(parent)
        self.controller=controller
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        num_row = QHBoxLayout()
        num_row.addWidget(QLabel("输入分子系数："))
        self.num_input = QLineEdit()
        num_row.addWidget(self.num_input)

        den_row = QHBoxLayout()
        den_row.addWidget(QLabel("输入分母系数："))
        self.den_input = QLineEdit()
        den_row.addWidget(self.den_input)

        self.btn_run = QPushButton("生成伯德图")
        self.btn_run.setObjectName("primaryBtn")
        self.progress = QProgressBar()
        self.progress.setVisible(False)

        layout.addWidget(QLabel("绘制伯德图"))
        layout.addLayout(num_row)
        layout.addLayout(den_row)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addStretch()
        self.btn_run.clicked.connect(self._run)

    def _run(self):
        num_input = self.num_input.text()
        den_input = self.den_input.text()
        try:
            num_list = [float(x) for x in num_input.split()]
            den_list = [float(x) for x in den_input.split()]
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效数字")
            return
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker = WorkerThread(
            self.controller.bode_graph,
            num_list,
            den_list
        )
        self._worker.finished.connect(self._on_done)
        self._worker.start()

    def _on_done(self,ok,msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            QPixmapCache.clear()
            dialog = QDialog(self)
            dialog.setWindowTitle("伯德图")
            layout = QVBoxLayout(dialog)
            _label = QLabel()
            _label.setPixmap(QPixmap(msg))
            layout.addWidget(_label)
            dialog.exec()
        else:
            QMessageBox.critical(self, "错误", msg)

class NyquistGraph(QWidget):
    def __init__(self,controller:ControlController,parent=None):
        super().__init__(parent)
        self.controller = controller
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        num_row = QHBoxLayout()
        num_row.addWidget(QLabel("输入分子系数："))
        self.num_input = QLineEdit()
        num_row.addWidget(self.num_input)

        den_row = QHBoxLayout()
        den_row.addWidget(QLabel("输入分母系数："))
        self.den_input = QLineEdit()
        den_row.addWidget(self.den_input)

        self.btn_run = QPushButton("生成奈奎斯特图")
        self.btn_run.setObjectName("primaryBtn")
        self.progress = QProgressBar()
        self.progress.setVisible(False)

        layout.addWidget(QLabel("绘制奈奎斯特图"))
        layout.addLayout(num_row)
        layout.addLayout(den_row)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addStretch()
        self.btn_run.clicked.connect(self._run)

    def _run(self):
        num_input = self.num_input.text()
        den_input = self.den_input.text()
        try:
            num_list = [float(x) for x in num_input.split()]
            den_list = [float(x) for x in den_input.split()]
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效数字")
            return
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker = WorkerThread(
            self.controller.nyquist_graph,
            num_list,
            den_list
        )
        self._worker.finished.connect(self._on_done)
        self._worker.start()

    def _on_done(self,ok,msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            QPixmapCache.clear()
            dialog = QDialog(self)
            dialog.setWindowTitle("奈奎斯特图")
            layout = QVBoxLayout(dialog)
            _label = QLabel()
            _label.setPixmap(QPixmap(msg))
            layout.addWidget(_label)
            dialog.exec()
        else:
            QMessageBox.critical(self, "错误", msg)

class StepResponse(QWidget):
    def __init__(self,controller:ControlController,parent=None):
        super().__init__(parent)
        self.controller = controller
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        num_row = QHBoxLayout()
        num_row.addWidget(QLabel("输入分子系数："))
        self.num_input = QLineEdit()
        num_row.addWidget(self.num_input)

        den_row = QHBoxLayout()
        den_row.addWidget(QLabel("输入分母系数："))
        self.den_input = QLineEdit()
        den_row.addWidget(self.den_input)

        self.btn_run = QPushButton("生成单位阶跃响应图")
        self.btn_run.setObjectName("primaryBtn")
        self.progress = QProgressBar()
        self.progress.setVisible(False)

        layout.addWidget(QLabel("绘制单位阶跃响应图"))
        layout.addLayout(num_row)
        layout.addLayout(den_row)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.progress)
        layout.addStretch()
        self.btn_run.clicked.connect(self._run)

    def _run(self):
        num_input = self.num_input.text()
        den_input = self.den_input.text()
        try:
            num_list = [float(x) for x in num_input.split()]
            den_list = [float(x) for x in den_input.split()]
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效数字")
            return
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self._worker = WorkerThread(
            self.controller.step_response,
            num_list,
            den_list
        )
        self._worker.finished.connect(self._on_done)
        self._worker.start()

    def _on_done(self,ok,msg):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        if ok:
            QPixmapCache.clear()
            dialog = QDialog(self)
            dialog.setWindowTitle("单位阶跃响应图")
            layout = QVBoxLayout(dialog)
            _label = QLabel()
            _label.setPixmap(QPixmap(msg))
            layout.addWidget(_label)
            dialog.exec()
        else:
            QMessageBox.critical(self, "错误", msg)

class ControlWidget(QWidget):
    """控制系统工具主界面，左侧导航 + 右侧功能页"""
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
        #secondaryBtn {
            background: #313244;
            color: #cdd6f4;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
        }
        #secondaryBtn:hover { background: #45475a; }
        QLineEdit {
            background: #181825;
            border: 1px solid #45475a;
            border-radius: 6px;
            padding: 6px 10px;
            color: #cdd6f4;
        }
        QLineEdit:focus { border-color: #89b4fa; }
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
        self.controller = ControlController()

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── 左侧导航 ──
        nav = QFrame()
        nav.setObjectName("navPanel")
        nav.setFixedWidth(180)
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)

        title = QLabel("控制系统")
        title.setObjectName("navTitle")
        nav_layout.addWidget(title)

        self.nav_buttons = []
        pages_info = [
            ("📍  特征根", GetPoles),
            ("📍  根轨迹", RootLocus),
            ("📍  伯德图", BodeGraph),
            ("📍  奈奎斯特图", NyquistGraph),
            ("📍  单位阶跃响应", StepResponse),
            # 以后在这里加新功能
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



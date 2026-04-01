from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QIcon
from tools import PdfEditorTool, SignatureTool,ControlTool

#注册所有工具，新增工具需在这里加一行
TOOLS = [
    PdfEditorTool(),
    SignatureTool(),
    ControlTool(),
]

class MainWindow(QMainWindow):

    STYLE = """
        QMainWindow, QWidget {
            background: #1e1e2e;
            color: #cdd6f4;
            font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
        }
        /* 最左侧工具栏 */
        #sidebar {
            background: #11111b;
            border-right: 1px solid #313244;
        }
        #appTitle {
            color: #cba6f7;
            font-size: 13px;
            font-weight: bold;
            padding: 18px 0 12px 0;
            qproperty-alignment: AlignCenter;
        }
        #toolBtn {
            border: none;
            background: transparent;
            color: #6c7086;
            font-size: 22px;
            padding: 12px 0;
            border-radius: 10px;
            margin: 4px 10px;
        }
        #toolBtn:hover   { background: #313244; color: #cdd6f4; }
        #toolBtn:checked { background: #313244; color: #cba6f7; }
        /* 工具名称提示 */
        #toolLabel {
            color: #6c7086;
            font-size: 10px;
            qproperty-alignment: AlignCenter;
            margin-bottom: 4px;
        }
        /* 右侧内容区域顶栏 */
        #topBar {
            background: #181825;
            border-bottom: 1px solid #313244;
        }
        #pageTitle {
            color: #cdd6f4;
            font-size: 16px;
            font-weight: bold;
            padding: 0 20px;
        }
        #pageDesc {
            color: #6c7086;
            font-size: 12px;
            padding: 0 20px;
        }
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("工具箱")
        self.setMinimumSize(860, 580)
        self.setStyleSheet(self.STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── 左侧图标栏 ──────────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(72)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        app_title = QLabel("🧰")
        app_title.setObjectName("appTitle")
        app_title.setFont(QFont("Segoe UI Emoji", 20))
        sidebar_layout.addWidget(app_title)

        self.tool_buttons = []
        self.stack = QStackedWidget()

        for i, tool in enumerate(TOOLS):
            # 图标按钮
            btn = QPushButton()
            btn.setObjectName("toolBtn")
            btn.setCheckable(True)

            icon=QIcon(tool.icon)
            btn.setIcon(icon)
            btn.setIconSize(QSize(32,32))
            btn.setToolTip(tool.name)
            btn.setFont(QFont("Segoe UI Emoji", 18))
            btn.clicked.connect(lambda _, idx=i: self._switch(idx))
            sidebar_layout.addWidget(btn)

            # 工具名称（小字）
            lbl = QLabel(tool.name)
            lbl.setObjectName("toolLabel")
            sidebar_layout.addWidget(lbl)

            self.tool_buttons.append(btn)

            # 将工具 widget 加入堆叠
            self.stack.addWidget(tool.get_widget(self))

        sidebar_layout.addStretch()

        # ── 右侧内容区 ──────────────────────────────────────────────
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # 顶部标题栏
        self.top_bar = QFrame()
        self.top_bar.setObjectName("topBar")
        self.top_bar.setFixedHeight(56)
        top_layout = QVBoxLayout(self.top_bar)
        top_layout.setContentsMargins(0, 8, 0, 8)
        top_layout.setSpacing(2)

        self.title_label = QLabel()
        self.title_label.setObjectName("pageTitle")
        self.desc_label = QLabel()
        self.desc_label.setObjectName("pageDesc")

        top_layout.addWidget(self.title_label)
        top_layout.addWidget(self.desc_label)

        right_layout.addWidget(self.top_bar)
        right_layout.addWidget(self.stack)

        root.addWidget(sidebar)
        root.addWidget(right)

        # 默认选中第一个工具
        self._switch(0)

    def _switch(self, index: int):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.tool_buttons):
            btn.setChecked(i == index)
        tool = TOOLS[index]
        self.title_label.setText(tool.name)
        self.desc_label.setText(tool.description)
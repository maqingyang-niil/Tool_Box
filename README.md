# 🧰 Toolbox

> 一个基于 PyQt6 的桌面工具箱，集成 PDF 处理、电子签名生成、控制系统分析等实用工具。

---

## ✨ 功能一览

### 📄 PDF 编辑器
- **合并** — 将多个 PDF 文件合并为一个，支持自定义顺序
- **拆分** — 按页码范围拆分 PDF，或将每页单独导出
- **剪开** — 将PDF文件从指定的页码位置分成两个文件

### ✍️ 电子签名
- 将手写签名图片处理为**透明背景 PNG**
- 支持自定义签名颜色与去背景阈值
- 实时预览处理效果

### 📊 控制系统分析
- **特征根计算** — 计算闭环传递函数的极点分布
- **根轨迹** — 绘制系统根轨迹图
- **伯德图** — 绘制幅频与相频响应曲线
- **奈奎斯特图** — 绘制极坐标频率响应图
- **单位阶跃响应图** — 绘制系统的单位阶跃响应曲线

---

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Windows 10/11

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

```bash
python main.py
```

---

## 📦 依赖列表

```
PyQt6
pypdf
reportlab
Pillow
numpy
scipy
matplotlib
opencv-python
```

---

## 📁 项目结构

```
toolbox/
├── main.py              # 入口文件
├── requirements.txt
├── core/
│   ├── app.py           # 主窗口
│   ├── base_tool.py     # 工具基类
│   ├── widgets.py       # 公共组件
│   └── utils.py         # 工具函数
└── tools/
    ├── pdf_editor/      # PDF 编辑器
    ├── signature/       # 电子签名
    └── control/         # 控制系统分析
```

---

## 🛠️ 打包为可执行文件

```bash
python -m nuitka --standalone --onefile --windows-disable-console --enable-plugin=pyqt6 main.py
```

---

## 📖 使用说明

### PDF 合并
1. 点击或拖拽多个 PDF 文件到拖放区
2. 使用上移/下移按钮调整顺序
3. 点击**合并 PDF**，选择保存路径

### PDF 拆分
1. 选择一个 PDF 文件
2. 输入页码范围（如 `1-3,5,7-9`），留空则每页单独导出
3. 点击**拆分 PDF**，选择输出文件夹

### 电子签名
1. 选择手写签名图片，不要出现中文路径
2. 调整去背景阈值和签名颜色
3. 点击**预览效果**确认结果
4. 点击**保存签名 PNG**导出

### 控制系统分析
- 输入传递函数的**分子系数**和**分母系数**，系数之间用空格分隔
- 例如开环传递函数 $\dfrac{s+1}{s^2+2s+1}$ 输入：
  - 分子：`1 1`
  - 分母：`1 2 1`

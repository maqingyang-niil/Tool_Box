from core.base_tool import BaseTool
from tools.pdf_editor.view import PdfEditorWidget
from tools.signature_gene.view import SignatureWidget
from core.utils import resource_path
#各工具的属性
class PdfEditorTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name="PDF编辑器"
        self.icon=resource_path("assets/icons/PDF.png")
        #self.icon="assets/icons/PDF.png"
        self.description="合并拆分PDF页面"

    def get_widget(self,parent):
        return PdfEditorWidget(parent)

class SignatureTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name="签名生成器"
        self.icon = resource_path("assets/icons/Signature.png")
        #self.icon="assets/icons/Signature.png"
        self.description="生成电子签名"

    def get_widget(self,parent):
        return SignatureWidget(parent)

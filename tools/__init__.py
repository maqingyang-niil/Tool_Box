from core.base_tool import BaseTool
from tools.pdf_editor.view import PdfEditorWidget

class PdfEditorTool(BaseTool):
    name="PDF编辑器"
    icon="assets/icons/PDF.png"
    description ="合并，拆分PDF页面"
    def get_widget(self,parent):
        return PdfEditorWidget(parent)


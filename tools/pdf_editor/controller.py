"""
PDF 操作的业务逻辑，与 UI 完全解耦。
依赖：pypdf（合并/拆分）、reportlab（水印）
安装：pip install pypdf reportlab
"""

import os
import re
from os import write

from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

class PdfController:

    #合并
    def merge(self,input_paths:list[str],output_path:str)->str:
        writer=PdfWriter()
        processed_count=0
        skipped_files=[]
        for path in input_paths:
            if os.path.exists(path) and path.lower().endswith(".pdf"):
                try:
                    reader=PdfReader(path)
                    for page in reader.pages:
                        writer.add_page(page)
                    processed_count+=1
                except Exception as e:
                    skipped_files.append(f"{os.path.basename(path)}(读取失败)")
            else:
                skipped_files.append(os.path.basename(path))
        if processed_count==0:
            return "合并失败：未发现有效的PDF文件。"
        with open(output_path,"wb") as f:
            writer.write(f)
        msg=f"已完成！合并了{processed_count}个文件。"
        if skipped_files:
            msg+=f"\n一忽略非PDF或损坏文件：{','.join(skipped_files)}"
        return msg

    #拆分
    def split(self,input_path:str,output_dir:str,page_range:str="")->str:
        reader=PdfReader(input_path)
        total=len(reader.pages)
        base=os.path.splitext(os.path.basename(input_path))[0]
        indices=self._parse_range(page_range,total) if page_range else list(range(total))

        saved=0
        if page_range:#提取部分页面
            writer=PdfWriter()
            for i in indices:
                writer.add_page(reader.pages[i])
            out=os.path.join(output_dir,f"{base}_split.pdf")
            with open(out,"wb") as f:
                writer.write(f)
            saved=1
        else:
            for i in indices:#逐页拆分
                writer=PdfWriter()
                writer.add_page(reader.pages[i])
                out=os.path.join(output_dir,f"{base}_page{i+1}.pdf")
                with open(out,"wb") as f:
                    writer.write(f)
                saved+=1
        return f"已拆分为{saved}个文件，保存至：{output_dir}"


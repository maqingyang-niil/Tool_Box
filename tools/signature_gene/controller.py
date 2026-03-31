import cv2
import numpy as np
from PIL import  Image

class ImageController:
    def SignatureGene(self,input_path,output_path)->str:
        img=cv2.imread(input_path,cv2.IMREAD_GRAYSCALE)
        #处理光照不均
        _, mask = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        #去噪
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # 组合成 RGBA
        result = np.zeros((*img.shape, 4), dtype=np.uint8)
        result[:, :, 3] = mask  # 笔迹不透明，背景透明

        Image.fromarray(result).save(output_path, "PNG")
        return f"签名已生成->{output_path}"
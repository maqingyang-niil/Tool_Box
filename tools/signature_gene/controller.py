import cv2
import numpy as np
from PIL import  Image

class ImageController:
    def signature_gene(self, input_path, output_path,
                          threshold=180, color_rgb=(0, 0, 0)) -> str:
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        _, mask = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        result = np.zeros((*img.shape, 4), dtype=np.uint8)
        result[:, :, 0] = color_rgb[0]
        result[:, :, 1] = color_rgb[1]
        result[:, :, 2] = color_rgb[2]
        result[:, :, 3] = mask
        Image.fromarray(result).save(output_path, "PNG")
        return f"签名已生成 → {output_path}"
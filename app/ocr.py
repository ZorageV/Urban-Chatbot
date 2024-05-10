import cv2
import numpy as np
import easyocr
from PIL import Image
import os
import Levenshtein as lev


def ocr(img_path):
    reader = easyocr.Reader(['en'])  # specify the language(s)
    img = Image.open(img_path).convert("RGB")
    img = np.array(img)
    result = reader.readtext(img)
    
    # Extracting text
    text = ' '.join([item[1] for item in result])
    
    return text



# if __name__ == "__main__":
print(ocr("../app/images/a01-000u.png"))
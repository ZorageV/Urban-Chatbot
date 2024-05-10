from PIL import Image
import os

def crop(img_path):
    img = Image.open(img_path)

    width, height = img.size

    left_img = img.crop((0, 0, width, height/5))
    right_img = img.crop((0, height/5, width, 4*height/5))
    


def process_images(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            crop(os.path.join(folder_path, filename))
        print(filename)

process_images("../app/images")
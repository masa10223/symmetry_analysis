import cv2
import numpy as np
from IPython.display import Image, display
from ipywidgets import widgets
from matplotlib import pyplot as plt



def imshow(img):
    """画像を Notebook 上に表示する。
    """
    encoded = cv2.imencode(".png", img)[1]
    display(Image(encoded))


def process(thresh, type_):
    type_ = eval(type_)
    IMG = img.copy()
    ret, binary = cv2.threshold(IMG, thresh, 255, type_)
    image, contours, hierarchy = cv2.findContours(binary,
                                               cv2.RETR_LIST,
                                               cv2.CHAIN_APPROX_SIMPLE)
    img_contour = cv2.drawContours(IMG, contours, -1, (255, 255, 0), 5)
    imshow(img_contour)

def main(args):

    param_widgets = {}
    param_widgets["thresh"] = widgets.IntSlider(
    min=0, max=255, step=1, value=0, description="thresh: "
        )
    options = [
        "cv2.THRESH_BINARY",
        "cv2.THRESH_BINARY_INV",
        "cv2.THRESH_TRUNC",
        "cv2.THRESH_TOZERO",
        "cv2.THRESH_TOZERO_INV",
        "cv2.THRESH_OTSU",
        "cv2.THRESH_BINARY + cv2.THRESH_OTSU"
    ]
    param_widgets["type_"] = widgets.Dropdown(options=options, description="type: ")

    for x in param_widgets.values():
        x.layout.width = "400px"

    img_path = str(args.path)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # ウィジェットを表示する。
    widgets.interactive(process, **param_widgets)



if __name__ == '__main__' :
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
                'path',
                type = str,
                help = 'input the absolute path of image'
                )

    args = parser.parse_args()   
    main(args)
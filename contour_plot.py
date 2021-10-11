import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def extract_region(path, THR):
    img  = cv2.imread(path, 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ## Binarize
    ret, img_binary = cv2.threshold(
                        img_gray,
                        THR, 255,
                        cv2.THRESH_BINARY
                        )
    ## Extract Contour
    image, contours, hierarchy = cv2.findContours(
                                    img_binary,
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_NONE
                                    )
    ## Draw Contour on the original image
    img_contour = cv2.drawContours(
                    img, contours, 
                    -1, 
                    (0, 255, 0), 
                    15
                    )
    return img_contour

def main(args):
    path = Path(args.path)
    THR =  Path(args.threshold)

    img = extract_region(path, THR)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

if __name__ == '__main__' :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
                'path',
                type = 'str',
                help = 'input the absolute path of image'
                )
    parser.add_argument(
                '-t',
                '--threshold',
                type = int,
                help = 'input value of threshold of binarizing image'
                )
    args = parser.parse_args()               
    
    main(args)
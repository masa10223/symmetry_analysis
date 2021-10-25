import cv2
import numpy as np
import sys

## 発現領域を抽出する。
def crop_expression_area(path, thr, area_min = 6000, area_max = 100000):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    IMG = img.copy()
    ret, binary = cv2.threshold(IMG, thr, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary,
                                            cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_SIMPLE)
    for i in range(0, len(contours)):
        if len(contours[i]) > 0:
        # remove small objects
            if (cv2.contourArea(contours[i]) > area_min )& (cv2.contourArea(contours[i]) < area_max ) :
                rect = contours[i]
                x, y, w, h = cv2.boundingRect(rect)
    ## 抽出領域が2個以上の場合わけを後で考える。
    buffer = 30
    img_exp = (img[y-buffer:y+h+buffer,x-buffer:x+w+buffer])    
    return img_exp

def split_crop_area(img_exp, thr):
    ret, binary = cv2.threshold(img_exp, thr, 1, cv2.THRESH_BINARY_INV)
    ## 左右の領域に分割する。
    Left = binary[:,:int(binary.shape[1]/2)]
    Right = np.fliplr(binary[:,int(binary.shape[1]/2):])
    return Left, Right

## 左右の ピクセル単位での overlap と unionを算出する。
def iou(a,b):
    union = 0
    intersection = 0
    union_coord = np.zeros([a.shape[0],a.shape[1]])
    intersection_coord =  np.zeros([a.shape[0],a.shape[1]])
    if (a.shape[0] == b.shape[0]) and (a.shape[1] == b.shape[1]):
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                if (a[i,j] == 1) and  (b[i,j] == 1):
                    intersection += 1
                    union += 1
                    union_coord[i,j] = 1
                    intersection_coord[i,j] = 1
                elif ((a[i,j] == 0) and  (b[i,j] == 1)) or ((a[i,j] == 1) and  (b[i,j] == 0)):
                    union += 1
                    union_coord[i,j] = 1
                else:
                    continue
                    
    return union, intersection, union_coord, intersection_coord


def main(args):
    path  = args.path
    thr = args.thr
    img_exp = crop_expression_area(path, thr)
    Left, Right = split_crop_area(img_exp, thr)
    union, intersection , union_coord, intersection_coord = iou(Left, Right)
    print("Rate of Assymetry is {}".format(intersection/union))


if __name__ == '__main__' :
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
                'path',
                type = str,
                help = 'input the absolute path of image'
                )

    parser.add_argument(
            '--thr',
            '-t',
            type = int,
            help = 'input the threshold of binarizing'
            )

    args = parser.parse_args()   
    main(args)
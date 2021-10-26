import cv2
import numpy as np
import sys

def preprocess(img_exp, thr, kernel_size = 4):
    _, binary = cv2.threshold(img_exp, thr, 1, cv2.THRESH_BINARY_INV)
    kernel = np.ones((kernel_size,kernel_size), np.uint8)
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(opening,
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)
    ## 最大領域を抽出。
    max_cnt = max(contours, key=lambda x: cv2.contourArea(x))
    ## 塗りつぶし
    out = np.zeros_like(binary)
    img_exp_pre = cv2.drawContours(out, [max_cnt], -1, color=1, thickness=-1)

    return img_exp_pre



## 発現領域を抽出する。
def crop_expression_area(path, thr, area_min = 6000, area_max = 100000):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    IMG = img.copy()
    _, binary = cv2.threshold(IMG, thr, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary,
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

def split_crop_area(binary):
    #ret, binary = cv2.threshold(img_exp, thr, 1, cv2.THRESH_BINARY_INV)
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


def rotate_binary_img(img_exp_pre, angle = 0):
    mu = cv2.moments(img_exp_pre, False)
    gx,gy= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
    #高さを定義
    height = img_exp_pre.shape[0]                         
    #幅を定義
    width = img_exp_pre.shape[1]  

    #スケールを指定
    scale = 1.0
    #getRotationMatrix2D関数を使用
    trans = cv2.getRotationMatrix2D((gx,gy), angle , scale)
    #アフィン変換
    img_exp_rotate = cv2.warpAffine(img_exp_pre, trans, (width,height))

    return img_exp_rotate


def padding_img(img_exp_rotate):
    if img_exp_rotate.shape[1] % 2 == 1:
        ## 横の長さが偶数になるように調整。
        img_exp_rotate = np.pad(img_exp_rotate,((0,0,),(0,1)))
    return img_exp_rotate

def main(args):
    path  = args.path
    thr = args.thr
    angle = args.angle
    img_exp = crop_expression_area(path, thr)
    img_exp_pre = preprocess(img_exp, thr)
    img_exp_pre = padding_img(img_exp_pre)
    img_exp_rotate = rotate_binary_img(img_exp_pre, angle)
    Left, Right = split_crop_area(img_exp_rotate)
    union, intersection , union_coord, intersection_coord = iou(Left, Right)
    #print("Rate of Assymetry is {}".format(1 - intersection/union))
    return 1 - intersection/union


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

    parser.add_argument(
        '--angle',
        '-a',
        type = int,
        default = 0, 
        help = 'input the angle of rotation'
        )

    args = parser.parse_args()   
    assym = main(args)
    print("Rate of Assymetry is {}".format(assym))
from calculate_iou import *
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

def change_angle_thr(path, THR_MIN = 0, THR_MAX = 50):
    result = []
    for thr in range(THR_MIN,THR_MAX):
        print('calculating IoU at  thr = {} ...'.format(thr))
        for angle in range(180):
            img_exp = crop_expression_area(path, thr)
            img_exp_pre = preprocess(img_exp, thr)
            img_exp_pre = padding_img(img_exp_pre)
            img_exp_rotate = rotate_binary_img(img_exp_pre, angle)
            Left, Right = split_crop_area(img_exp_rotate)
            union, intersection , _, _ = iou(Left, Right)
            assym = 1 - intersection/union
            result.append([thr,angle,assym])
    Result = pd.DataFrame(np.array(result))
    Result.columns = ['thr','angle','assym']
    return Result
    
def main(args):
    path  = args.path
    THR_MIN = args.thr_min
    THR_MAX = args.thr_max
    Result = change_angle_thr(path,THR_MIN,THR_MAX)
    Result.to_csv('./CSV/Result_path_{}_thrmin_{}_thrmax_{}.csv'.format(path,THR_MIN,THR_MAX))
    print("Calculation is Done.")
    plt.figure(figsize=(10,10))
    plot_result = []
    print('Now ploting... ')
    for thr in tqdm(range(THR_MIN,THR_MAX)):
        assym_min = np.min(Result[Result.thr == thr].assym)
        plot_result.append([thr,assym_min])
    plot_result = np.array(plot_result)
    plt.scatter(plot_result[:,0],plot_result[:,1])
    plt.plot(plot_result[:,0],plot_result[:,1])
    plt.xlabel('Threshold', fontsize = 20)
    plt.ylabel('IoU (lower limit)', fontsize = 20)
    plt.savefig('./IoU_angle_thr.png')


if __name__ == '__main__' :
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
                'path',
                type = str,
                help = 'input the absolute path of image'
                )

    parser.add_argument(
            '--thr_min',
            '-min',
            type = int,
            default=0,
            help = 'input the threshold of binarizing'
            )

    parser.add_argument(
        '--thr_max',
        '-max',
        type = int,
        default = 50, 
        help = 'input the angle of rotation'
        )

    args = parser.parse_args()   
    main(args)



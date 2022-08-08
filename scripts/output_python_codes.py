import pandas as pd
import glob, os, re
import matplotlib.pyplot as plt
from tqdm import tqdm

## このパスはいずれ変更する。
df = pd.read_csv('/Volumes/GoogleDrive/マイドライブ/Uchida/RawData/WISH/results.csv')
## df.shape = (303,5)

f = open('./scripts/extract_script.sh','w')
f.write('#!/bin/sh\n')
f.write('\n')
for i in tqdm(range(df.shape[0])):
    filename = df.iloc[i]['FILENAME']
    try:
        AA = [path for path in glob.glob('/Volumes/GoogleDrive/マイドライブ/Uchida/RawData/WISH/2*/*.tif') if filename in path][0]
        path = './{}/{}'.format(os.path.basename(os.path.dirname(AA)),os.path.basename(AA))
        gene = re.findall(r'[A-Za-z0-9]+',filename)[0]
        tmin = df.iloc[i]['LOW']
        tmax = df.iloc[i]['HIGH']
        codes = 'python test_select_gene.py -tmin {} -tmax {} -amin 4000 -amax 20000 -g {} -p {} \n'.format(tmin, tmax, gene, path)
        f.write(codes)
    except:
        pass
f.close()
import glob
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns



def concat_csv():
    i = 0 
    for CSV in sorted(glob.glob('../CSV/20220608/result*.csv')):
        print("concatenating on {}".format(CSV))
        if i == 0:
            tmp = pd.read_csv(CSV, index_col=0)
        else: 
            df = pd.read_csv(CSV, index_col=0)
            tmp = pd.concat([tmp, df])
        i += 1
    tmp['tag'] = tmp['filename'].apply(lambda x:x[:-13])
    tmp_r = tmp.reset_index()
    gene_result = tmp_r.groupby(['tag']).apply(lambda d:d.loc[d['assym'].idxmin()]).reset_index(drop=True)
    
    return gene_result

def extract_gene_csv(gene_result):
    #bmp2_assym = gene_result[gene_result.gene == 'bmp2']['assym']
    #bmp4_assym = gene_result[gene_result.gene == 'bmp4']['assym']
    #bmp7_assym = gene_result[gene_result.gene == 'bmp7']['assym']
    ndl_assym = gene_result[gene_result.gene == 'ndr2']['assym']
    szl_assym = gene_result[gene_result.gene == 'szl']['assym']
    
    return bmp2_assym, bmp4_assym, bmp7_assym, ndl_assym, szl_assym

def plot_violin(bmp2_assym, bmp4_assym, bmp7_assym, ndl_assym, szl_assym):
    df = pd.DataFrame({
        'bmp2': bmp2_assym,
        'bmp4': bmp4_assym,
        'bmp7': bmp7_assym,
        'ndr': ndl_assym,
        'szl': szl_assym
    })
    df_melt = pd.melt(df)
    fig = plt.figure(figsize=(10,7))
    sns.set_style('whitegrid')
    ax = fig.add_subplot(1, 1, 1)

    sns.violinplot(x='variable', y='value', data=df_melt, jitter=True, color = '#DDDDDD', ax=ax)
    sns.stripplot(x='variable', y='value', data=df_melt,size=10,
                jitter=True, linewidth=2,palette = 'gist_ncar')

    ax.set_xlabel('Gene', fontsize = 20)
    ax.set_ylabel('Rate of Assymetry ' ,fontsize = 20)
    ax.set_xticklabels(['bmp2', 'bmp4','bmp7', 'ndr', 'szl'],fontsize=16)
    plt.savefig('../Figs/violinplot_each_gene.png')
    
    
if __name__ == '__main__' :
    import datetime
    gene_result = concat_csv()
    bmp2_assym, bmp4_assym, bmp7_assym, ndl_assym, szl_assym = extract_gene_csv(gene_result)
    plot_violin(bmp2_assym, bmp4_assym, bmp7_assym, ndl_assym, szl_assym )
    
    gene_result.to_csv('../each_gene_lower_bound_result_{}.csv'.format(datetime.datetime.now().date()))
    



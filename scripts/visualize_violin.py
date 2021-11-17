import glob
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns



def concat_csv():
    i = 0 
    for CSV in sorted(glob.glob('../CSV/result*.csv')):
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
    chd_assym = gene_result[gene_result.gene == 'Chordin']['assym']
    ndl_assym = gene_result[gene_result.gene == 'Nodal']['assym']
    szl_assym = gene_result[gene_result.gene == 'Szl']['assym']
    
    return chd_assym, ndl_assym, szl_assym

def plot_violin(chd_assym, ndl_assym, szl_assym):
    df = pd.DataFrame({
        'chd': chd_assym,
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
    ax.set_xticklabels(['chd', 'ndr', 'szl'],fontsize=16)
    plt.savefig('../Figs/violinplot_each_gene.png')
    
    
if __name__ == '__main__' :
    import datetime
    gene_result = concat_csv()
    chd_assym, ndl_assym, szl_assym = extract_gene_csv(gene_result)
    plot_violin( chd_assym, ndl_assym, szl_assym )
    
    gene_result.to_csv('../each_gene_lower_bound_result_{}.csv'.format(datetime.datetime.now().date()))
    



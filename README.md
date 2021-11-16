# 多階層揺らぎ解析による多様性の発生基盤の解明(仮)　
Shunsuke Ichii, Masato Tsutsumi, Yui Uchida et al., 
## smFISH パート
tmr と dapi と呼ばれる染色を用いてそれぞれでの蛍光画像を重ね合わせた画像から、mRNAの数を数える。



## WISH パート
遺伝子を発現させ、胚の表面領域でどのように発現しているのかをその領域の対称度合いを用いて解析する。


### 作業ブランチの説明。
- main 
 main branchこれを最終的な pulish として出す。基本いじらない。 README.md と 原稿のmanuscriptぐらいを置いておく予定。
- smFISH-ichii
@ichii-shunsuke smFISH 担当ブランチ。smFISH の解析　主な言語は MATLAB
- smFISH-tsutsumi
@masa10223 smFISH 担当ブランチ。smFISH の解析　主な言語は python
- WISH-ichii
@ichii-shunsuke WISH 担当ブランチ。smFISH の解析　主な言語は MATLAB
- WISH-tsutsumi
@masa10223 smFISH 担当ブランチ。smFISH の解析　主な言語は python


## script の説明
とある [gene] のtif 画像[filename]から、ある閾値[thr min] からある閾値[thr max]まで二値化した画像からある面積[area min]からある面積[area max]までの範囲にある発現領域をとる。
```
$ conda activate DLC-CPU
$ python ./scripts/test_select_gene.py -tmin [thr min] -tmax [thr max] -amin [area min] -amax [area max] -g [gene name] -p [filename]
```
visualize violin plot
```
$ python ./scripts/visualize_violin.py
```
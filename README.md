# 多階層揺らぎ解析による多様性の発生基盤の解明(仮)　
Shunsuke Ichii, Masato Tsutsumi, Yui Uchida et al., 

## 何をどこまでやるか

### やること

### ターゲット遺伝子
#### 背腹軸形成：
	chrd, szl, bmp2b, bmp7
#### 頭尾軸形成：
	bmp2b, Wnt5a, Wnt7, Wnt8a, ndr2


### どういうFigureを用意するか
#### Figure1：
	(a)ターゲット遺伝子、どこで発現してどの軸形成に関わるか、発現量揺らぎがでかいか小さいか

#### Figure2：
	(a) smFISHの実験と解析の概要 
	(b) データ処理してこういう像が見えました事例
	(c) mRNAカウント数のヒストグラム？　
	(d) mRNA分子数揺らぎ（sdかなんか）のプロット

#### Supplemental Figure1：
	(a) バックグラウンド
	(b) probe入れない場合の自家蛍光
	(c) 非発現領域の蛍光
	(輝度ヒストグラムをつけるか）

#### Figure3：
	(a) WISH解析の概要
	(b) データ処理してこういう像が見えました事例
	(c) 非対称度のプロット

#### Supplemental Figure 2：
	(a~) （域値取るなら）別の域値でやるとこういう結果になった

#### Supplemental Figure 3：
	(a~) 別の指標でやるとこうなった

#### Figure4：
	(a) 発現量揺らぎの大小、細胞内発現量揺らぎの大小、発現領域揺らぎの大小のまとめ



## 手法内容
## smFISH パート
tmr と dapi と呼ばれる染色を用いてそれぞれでの蛍光画像を重ね合わせた画像から、mRNAの数を数える。（使える細胞10個、サンプル6replicates（上下１個ずつ捨てる）くらいの感じで）



## WISH パート
遺伝子を発現させ、胚の表面領域でどのように発現しているのかをその領域の対称度合いを用いて解析する。

## About this Repository
### 作業ブランチの説明。
1. main 
   - main branch これを最終的にpublishする。基本いじらない。 README.md と 原稿のmanuscriptぐらいを置いておく予定。
2. smFISH-ichii
   - @ichii-shunsuke smFISH 担当ブランチ。smFISH の解析　主な言語は MATLAB
3. smFISH-tsutsumi
   - @masa10223 smFISH 担当ブランチ。smFISH の解析　主な言語は python
4. WISH-ichii
   - @ichii-shunsuke WISH 担当ブランチ。smFISH の解析　主な言語は MATLAB
5. WISH-tsutsumi
   - @masa10223 smFISH 担当ブランチ。smFISH の解析　主な言語は python

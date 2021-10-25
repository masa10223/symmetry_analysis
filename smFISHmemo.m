% smFISH
close all
% データ読み込み
data = lsmread("RawData/smFISH/20211005/Chordin/chordin_211005_sample1_1_DAPI=1_TMR=40_average8_2048^2_interval=0_slice1.lsm");
% 輝度のヒストグラム
h = histogram(data(1,2,1,:,:));
h.BinWidth = 1;
hvalues = h.Values; % ヒストグラムのデータ
%x = 1:max(data(:));

% 閾値はmatlab内の曲線近似のアプリケーションを使ってガウス分布2個でfitして、ズレ始めたところを使用

% gauss filterの大きさ
filterWidth = 7;
% 画像データを[0 1]のdoubleに変換
rescaledData = rescale(double(squeeze(data(1,2,1,:,:))));
% 閾値を切ってノイズでない領域を決める
denoisedArea = imgaussfilt(double(squeeze(data(1,2,1,:,:)>20)), filterWidth)>0.9;
% 輝度の勾配を計算
gradient = imgradient(imgaussfilt(rescaledData, filterWidth));
imshow(rescale(gradient.*denoisedArea)); % ノイズでない領域で勾配を表示

% 閾値を切って表示
figure;
imshow(rescale(squeeze(double(z(1,2,1,:,:)).*double(z(1,2,1,:,:)>20))));

% そのまま表示
figure;
imshow(rescale(squeeze(double(z(1,1,1,:,:)))));

% dapiが赤、TMRが緑
figure;
colorFig = zeros([size(z, [4,5]), 3]);
colorFig(:,:,1) = rescale(double(z(1,1,1,:,:)));
colorFig(:,:,2) = rescale(double(z(1,2,1,:,:)));
imshow(colorFig);

% 先行研究の方法に従ってrolling ballみたいなものをやろうとした結果
% Jは1回
% J2はfilterかけてもう一度
% J3はさらにもう一回
close all
I = squeeze(data(1,2,1,:,:));
se = strel('disk',30);
J = imsubtract(imadd(I,imtophat(I,se)),imbothat(I,se));
figure
imshow(J)
I2 = imgaussfilt(J,3);
se2 = strel('disk',15);
J2 = imsubtract(imadd(I2,imtophat(I2,se2)),imbothat(I2,se2));
figure
imshow(J2)
I3 = imgaussfilt(J2,3);
se3 = strel("disk", 7);
J3 = imsubtract(imadd(I3,imtophat(I3,se3)),imbothat(I3,se3));
figure
imshow(J3)

% パラメータを調整
close all
I = squeeze(data(1,1,1,:,:));
se = strel('disk',6);
J = imsubtract(imadd(I,imtophat(I,se)),imbothat(I,se));
figure
imshow(J)
I2 = imgaussfilt(J,1);
se2 = strel('disk',3);
J2 = imsubtract(imadd(I2,imtophat(I2,se2)),imbothat(I2,se2));
figure
imshow(J2)
I3 = imgaussfilt(J2,1);
se3 = strel("disk", 1);
J3 = imsubtract(imadd(I3,imtophat(I3,se3)),imbothat(I3,se3));
figure
imshow(J3)

% J3のうち上位0.5%の輝度の部分を抽出
top = zeros(size(J3));
[~,ind] = maxk(J3(:),ceil(size(J3(:),1)*0.005));
top(ind) = 1;
figure
imshow(top);

% topのうちareaが小さいやつを除く
L = bwlabel(top);
stats = regionprops(L, "Area");
for i = 1:size(stats, 1)
    if stats(i).Area < 3
        L(L==i) = 0;
    end
end
imshow(top.*(L>0));

% 検出されたものをtmrに重ねて見る
colorFig = repmat(squeeze(data(1,1,1,:,:)), [1,1,3]);
existence = zeros(size(colorFig), "logical");
existence(:,:,1) = L>0;
colorFig(existence) = 512;
imshow(colorFig)



RawData = lsmread("RawData/smFISH/20211011/NoProbe/noprobe_211011 _sample1_1_DAPI%=2_TMR%=10_sum=4_size=512_interval=0_slice=1.lsm");
RawData = lsmread("RawData/smFISH/20211011/probe conc. 2%/ndr2_211011 _sample1_2_DAPI%=1_TMR%=10_TMRgain=900__sum=4_size=512_interval=0_slice=1.lsm");
tmr = rescale(double(squeeze(RawData(1,1,1,:,:))));
dapi = rescale(double(squeeze(RawData(1,2,1,:,:))));



%main.mに作ったが、highlightの閾値で結果がかなり変わる
%調整が必要 interactiveにできるか？
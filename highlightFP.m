function FP = highlightFP(data)
%data = lsmread("RawData/smFISH/20211005/Chordin/chordin_211005_sample1_1_DAPI=1_TMR=40_average8_2048^2_interval=0_slice1.lsm");
%{
close all
I = squeeze(data(1,1,1,:,:));
se = strel('disk',6);
J = imsubtract(imadd(I,imtophat(I,se)),imbothat(I,se));
%figure
%imshow(J)
I2 = imgaussfilt(J,1);
se2 = strel('disk',3);
J2 = imsubtract(imadd(I2,imtophat(I2,se2)),imbothat(I2,se2));
%figure
%imshow(J2)
I3 = imgaussfilt(J2,1);
se3 = strel("disk", 1);
J3 = imsubtract(imadd(I3,imtophat(I3,se3)),imbothat(I3,se3));
%figure
%imshow(J3)

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
%}

% readTifSeqの場合
% rolling ball
se = strel('disk',20);
J = imsubtract(imadd(data,imtophat(data,se)),imbothat(data,se));
I2 = imgaussfilt(J,1);
se2 = strel('disk',15);
J2 = imsubtract(imadd(I2,imtophat(I2,se2)),imbothat(I2,se2));
I3 = imgaussfilt(J2,1);
se3 = strel("disk", 10);
J3 = imsubtract(imadd(I3,imtophat(I3,se3)),imbothat(I3,se3));
%imshow(J3);

% 上位0.5パーセント%の輝度
top = zeros(size(J3), "logical");
[~,ind] = maxk(J3(:),ceil(size(J3(:),1)*0.01));
top(ind) = true;

% 連結した部分を抽出して面積が3未満の孤立したものノイズとして除く
L = bwlabel(top);
stats = regionprops(L, "Area");
for i = 1:size(stats, 1)
    if stats(i).Area < 5
        L(L==i) = 0;
    end
end
FP = logical(L);
end

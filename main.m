function [tmrHighlight, dapiHighlight] = main(tifFilename, Npage, ROIFilename, figSize)
% tifFilename tifの名前
% Npage tifに何枚含まれるか
% ROIFilename imageJで作ったROIデータの名前
% figSize 画像の1辺のpixelサイズ
tifData = readTifSeq(tifFilename, Npage*2);
tmrData = tifData(1:2:Npage*2,:,:);
dapiData = tifData(2:2:Npage*2,:,:);
tmrHighlight = zeros(size(tmrData));
dapiHighlight = zeros(size(tmrData));
for t = 1:Npage
    tmrHighlight(t,:,:) = highlightFP(squeeze(tmrData(t,:,:)));
end
for t = 1:Npage
    dapiHighlight(t,:,:) = highlightFP(squeeze(dapiData(t,:,:)));
end
ROIs = readROIs(ROIFilename, figSize);
tmrinROI = zeros(1,size(ROIs,1));
dapiinROI = zeros(1,size(ROIs,1));
for i = 1:size(ROIs,1)
    for t = 1:Npage
        tmrinCell = squeeze(ROIs(i,:,:)&tmrHighlight(t,:,:));
        CC = bwconncomp(tmrinCell);
        tmrinROI(i) = tmrinROI(i)+CC.NumObjects;
        dapiinCell = squeeze(ROIs(i,:,:)&dapiHighlight(t,:,:));
        CC = bwconncomp(dapiinCell);
        dapiinROI(i) = dapiinROI(i)+CC.NumObjects;
    end
end
close all
figure
plot(1, tmrinROI, "+");
hold on
plot(2, dapiinROI, "+");
xticks([1 2]);
xticklabels(["TMR", "DAPI"])
xlim([0 3])
end
function [tmrinROI, tmrHighlight] = plotNFP(tmrData, ROIs, param)
% tifFilename tifの名前
% Npage tifに何枚含まれるか
% ROIFilename imageJで作ったROIデータの名前
% figSize 画像の1辺のpixelサイズ
tmrHighlight = zeros(size(tmrData));
Npage = size(tmrData, 1);
disp(Npage)
for t = 1:Npage
    tmrHighlight(t,:,:) = highlightFP(squeeze(tmrData(t,:,:)), param);
end
tmrinROI = zeros(1,size(ROIs,1));
for i = 1:size(ROIs,1)
    for t = 1:Npage
        tmrinCell = squeeze(ROIs(i,:,:)&tmrHighlight(t,:,:));
        CC = bwconncomp(tmrinCell);
        tmrinROI(i) = tmrinROI(i)+CC.NumObjects;
    end
end
end
function areaListT = readROIs(filename, figSize)
sROIs = ReadImageJROI(filename);
sRegions = ROIs2Regions(sROIs, [figSize figSize]);
areaList = zeros(size(sRegions.PixelIdxList, 2), figSize, figSize, "logical");
for i = 1:size(sRegions.PixelIdxList, 2)
    areaList(i, sRegions.PixelIdxList{i}) = true;
end
areaListT = zeros(size(sRegions.PixelIdxList, 2), figSize, figSize, "logical");
for i = 1:size(sRegions.PixelIdxList, 2)
    areaListT(i,:,:) = squeeze(areaList(i,:,:)).';
end
end
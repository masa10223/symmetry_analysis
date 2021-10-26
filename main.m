tifData = readTifSeq(tifFilename);
tmrData = tifData(1:2:end,:,:);
dapiData = tifData(2:2:end,:,:);
figSize = size(tifData, 3);
ROIs = readROIs(ROIFilename, figSize);
plotNFP(tmrData, dapiData, ROIs);
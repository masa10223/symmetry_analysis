% filenameの取り込み
% ls *.tif >> tifFilenamelist.tx
% ls *.zip >> ROIFilenamelist.txt などとしておく
szlTifFilename = "RawData/smFISH/20211018/"+splitlines(string(fileread("RawData/smFISH/20211018/szlTifFilename.txt")));
szlTifFilename = szlTifFilename(1:end-1);
szlROIFilename = "RawData/smFISH/20211018/"+splitlines(string(fileread("RawData/smFISH/20211018/szlROIFilename.txt")));
szlROIFilename = szlROIFilename(1:end-1);
chrdTifFilename = "RawData/smFISH/20211022/"+splitlines(string(fileread("RawData/smFISH/20211022/chrdTifFilename.txt")));
chrdTifFilename = chrdTifFilename(1:end-1);
chrdROIFilename = "RawData/smFISH/20211022/"+splitlines(string(fileread("RawData/smFISH/20211022/chrdROIFilename.txt")));
chrdROIFilename = chrdROIFilename(1:end-1);
wntTifFilename = "RawData/smFISH/20211022/"+splitlines(string(fileread("RawData/smFISH/20211022/wntTifFilename.txt")));
wntTifFilename = wntTifFilename(1:end-1);
wntROIFilename = "RawData/smFISH/20211022/"+splitlines(string(fileread("RawData/smFISH/20211022/wntROIFilename.txt")));
wntROIFilename = wntROIFilename(1:end-1);

% szl
szlNFP = cell(1,6);
for sampleIndex = 1:6
    tifFilename = szlTifFilename(contains(szlTifFilename, append("sample", num2str(sampleIndex))));
    ROIFilename = szlROIFilename(contains(szlROIFilename, append("sample", num2str(sampleIndex))));
    for i = 1:size(tifFilename,1)
        tifData = readTifSeq(tifFilename(i));
        tmrData = tifData(1:2:end,:,:);
        figSize = size(tifData, 3);
        ROIs = readROIs(ROIFilename(i), figSize);
        szlNFP{sampleIndex} = [szlNFP{sampleIndex} plotNFP(tmrData, ROIs)];
    end
end

% chrd
chrdNFP = cell(1,6);
for sampleIndex = 1:6
    tifFilename = chrdTifFilename(contains(chrdTifFilename, append("sample", num2str(sampleIndex))));
    ROIFilename = chrdROIFilename(contains(chrdROIFilename, append("sample", num2str(sampleIndex))));
    for i = 1:size(tifFilename,1)
        tifData = readTifSeq(tifFilename(i));
        tmrData = tifData(1:2:end,:,:);
        figSize = size(tifData, 3);
        ROIs = readROIs(ROIFilename(i), figSize);
        chrdNFP{sampleIndex} = [chrdNFP{sampleIndex} plotNFP(tmrData, ROIs)];
    end
end

% wnt
wntNFP = cell(1,6);
for sampleIndex = 1:6
    tifFilename = wntTifFilename(contains(wntTifFilename, append("sample", num2str(sampleIndex))));
    ROIFilename = wntROIFilename(contains(wntROIFilename, append("sample", num2str(sampleIndex))));
    for i = 1:size(tifFilename,1)
        tifData = readTifSeq(tifFilename(i));
        tmrData = tifData(1:2:end,:,:);
        figSize = size(tifData, 3);
        ROIs = readROIs(ROIFilename(i), figSize);
        wntNFP{sampleIndex} = [wntNFP{sampleIndex} plotNFP(tmrData, ROIs)];
    end
end


% plot szl
hold on
for i = 1:6
    if size(szlNFP{i},2) > 0
        plot(i,szlNFP{i},".");
    end
end
xlabel("sample");
ylabel("# in a cell")
xlim([0.5 6.5])
set(gca, "fontsize", 20);
saveas(gca, "szlNFP.png")
close

vec = [];
sample = [];
for i = 1:6
    vec = [vec, szlNFP{i}];
    sample = [sample i*ones(1,size(szlNFP{i},2))];
end
violinplot(vec, sample);
xlabel("sample");
ylabel("# in a cell");
xlim([0.5 6.5])
title("szl")
set(gca, "fontsize", 20);
saveas(gca, "szlNFPviolin.png")
close

% plot chrd

hold on
for i = 1:6
    if size(chrdNFP{i},2) > 0
        plot(i,chrdNFP{i},".");
    end
end
xlabel("sample");
ylabel("# in a cell")
xlim([0.5 6.5])
set(gca, "fontsize", 20);
saveas(gca, "chrdNFP.png")
close

vec = [];
sample = [];
for i = 1:6
    vec = [vec, chrdNFP{i}];
    sample = [sample i*ones(1,size(chrdNFP{i},2))];
end
violinplot(vec, sample);
xlabel("sample");
ylabel("# in a cell");
xlim([0.5 6.5])
title("chrd")
set(gca, "fontsize", 20);
saveas(gca, "chrdNFPviolin.png")
close

% plot wnt

hold on
for i = 1:6
    if size(wntNFP{i},2) > 0
        plot(i,wntNFP{i},".");
    end
end
xlabel("sample");
ylabel("# in a cell")
xlim([0.5 6.5])
set(gca, "fontsize", 20);
saveas(gca, "wntNFP.png")
close

vec = [];
sample = [];
for i = 1:6
    vec = [vec, wntNFP{i}];
    sample = [sample i*ones(1,size(wntNFP{i},2))];
end
violinplot(vec, sample);
xlabel("sample");
ylabel("# in a cell");
xlim([0.5 6.5])
title("wnt")
set(gca, "fontsize", 20);
saveas(gca, "wntNFPviolin.png")
close


% sample# が含まれているかはcontainを使う
%{
index = 2;
tifData = readTifSeq(tifFilenamelist(index));
tmrData = tifData(1:2:end,:,:);
figSize = size(tifData, 3);
ROIs = readROIs(ROIFilenamelist(index), figSize);
[x,y] = plotNFP(tmrData, ROIs);
%}
%{
tmrNFP = [];
for index = 1:size(tifFilenamelist,1)
    tifData = readTifSeq(tifFilenamelist(index));
    tmrData = tifData(1:2:end,:,:);
    dapiData = tifData(2:2:end,:,:);
    figSize = size(tifData, 3);
    ROIs = readROIs(ROIFilenamelist(index), figSize);
    [tmrinROI, dapiinROI] = plotNFP(tmrData, dapiData, ROIs);
    cat(1, tmrNFP, tmrinROI);
    cat(1, dapiNFP, dapiinROI);
end
figure
plot(1, tmrNFP, "+");
hold on
plot(2, dapiNFP, "+");
xticks([1 2]);
xticklabels(["TMR", "DAPI"])
xlim([0 3])
%}
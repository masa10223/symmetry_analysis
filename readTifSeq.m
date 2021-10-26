function output = readTifSeq(filename)
info = imfinfo(filename);
length = size(info, 1);
output(1,:,:) = imread(filename, 1, "Info", info);
sz = size(output);
output(2:length,:,:) = zeros(length-1, sz(2), sz(3));
for i = 2:length
    output(i,:,:) = imread(filename, i, "Info", info);
end
%   Tiff Sequenceを読み込み
end
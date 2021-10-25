function output = readTifSeq(filename, length)
output(1,:,:) = imread(filename, 1);
sz = size(output);
output(2:length,:,:) = zeros(length-1, sz(2), sz(3));
for i = 2:length
    output(i,:,:) = imread(filename, i);
end
%   Tiff Sequenceを読み込み
end
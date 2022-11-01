function output = readTifSeq(filename)
info = imfinfo(filename);
length = size(info, 1);
outputtest = imread(filename, 1, "Info", info);
if ndims(outputtest) > 3
    disp(filename)
    disp("dimension error")
elseif ndims(outputtest) == 3
    N = size(outputtest,3);
    stdnlist = zeros(1,N);
    for n = 1:N
        stdnlist(n) = std(double(outputtest(:,:,n)),1,"all");
    end
    [M,I] = max(stdnlist);
    disp(filename)
    disp([M,I,N]);
    output(1,:,:) = outputtest(:,:,I);
    sz = size(output);
    output(2:length,:,:) = zeros(length-1, sz(2), sz(3));
    for i = 2:length
        outputtest= imread(filename, i, "Info", info);
        output(i,:,:) = outputtest(:,:,I);
    end
else
    output(1,:,:) = imread(filename, 1, "Info", info);
    sz = size(output);
    output(2:length,:,:) = zeros(length-1, sz(2), sz(3));
    for i = 2:length
        output(i,:,:) = imread(filename, i, "Info", info);
    end
end
%   Tiff Sequenceを読み込み
end
function [] = displayTens_Alona(T,slices,txt,isCell)
% displays tensor along slices given by "slices" using subfigures
% slices are indices corresponding to slices along mode 1

if nargin < 4
    isCell = 0;
end

if ~isCell
    n1 = size(T,1);
    n2 = size(T,2);

    figure
    hold on
    for i=1:length(slices)
        x1=subplot(2,ceil(length(slices)/2),i);
        theslice = reshape(T(:,:,slices(i)),n1,n2);
        imagesc(theslice);
        caxis(x1,[0,1.2]);
        title([txt,'Slice ', num2str(slices(i))]);
    end
    hold off
else
    figure
    hold on
    for i=1:length(slices)
        subplot(2,ceil(length(slices)/2),i);
        theslice = T{i};
        imagesc(theslice);
        
        title([txt,'Matrix ', num2str(slices(i))]);
    end
    hold off
end


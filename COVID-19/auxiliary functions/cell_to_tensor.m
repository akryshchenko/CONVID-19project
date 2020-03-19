function data_tensor = cell_to_tensor(data_cell)
%returns a tensor object, as opposed to a vanilla matlab array 

K = length(data_cell);
data_point_cell_1 = data_cell{1};    %this is a rank 1 k-tensor
sizes = size(data_point_cell_1);
I = sizes(1);
J = sizes(2);

data_tensor = zeros(I, J, K);

for k = 1:K
    data_point_ktensor = data_cell{k}; 
    data_point_tensor = tensor(data_point_ktensor);
    data_point_tensor = double(data_point_tensor);
    data_tensor(:, :, k) = data_point_tensor;
end
    
data_tensor = tensor(data_tensor);
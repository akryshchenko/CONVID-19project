function data_tensor = cell_to_tensor(data_cell)

data_point = data_cell{1};  %this is a ktensor
data_point_tensor = tensor(data_point);
sizes = size(data_point_tensor);

num_data_points = length(data_cell);
sizes = [sizes, num_data_points];
data_tensor = zeros(sizes);

for k = 1:num_data_points
    
    
    data_tensor
    
end
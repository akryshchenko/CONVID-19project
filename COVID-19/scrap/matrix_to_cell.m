function data_cell = matrix_to_cell(data_matrix, cell_of_groups_of_feature_indices)

%Converts your data matrix into a cell array. A cell array is an
%array of cells. Our cells will be kruskal tensors (ktensors), with each
%cell corresponding to a different data point (e.g. patient). Each
%different component/axis of the tensor will correspond to a different group of
%related features. For instance, one group of features might be related to
%geographical location, like longitude, lattitude, altitude. Another might
%be related to intrinsic attributes of the patient, like height, age,
%presence of prexisting medical conditions.

num_data_points = length(data_matrix(:, 1));
num_groups_of_features = length(cell_of_groups_of_feature_indices);

%make empty cell array, with size the number of data points


data_cell = cell([1, num_data_points]);

for i = 1:num_data_points
    
    data_point_cell = cell([1, num_groups_of_features]);
    
    for j = 1:num_groups_of_features
        
        data_point = data_matrix(i, :);
        indices = cell_of_groups_of_feature_indices{j};
        component = data_point(indices);
        component = component';
        data_point_cell{j} = component;
        
    end
    
    data_point_ktensor = ktensor(data_point_cell);
    data_cell{i} = data_point_ktensor;
    
end









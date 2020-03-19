function data_cell = matrix_to_cell(data_matrix, idx_group_1, idx_group_2)

M = length(data_matrix(:, 1));

data_cell = cell([1, M]);


for m = 1:M
    
    data_point = data_matrix(m, :);
    a = data_point(idx_group_1);
    b = data_point(idx_group_2);
    
    a = a';
    b = b';
    data_point_ktensor = ktensor({a, b});
    data_cell{m} = data_point_ktensor;
end


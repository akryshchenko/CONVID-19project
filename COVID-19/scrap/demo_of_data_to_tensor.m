%{

Outline of this demo:

0. convert csv to matrix form
1. function data_cell = frame_to_cell(data_matrix, idx_group_1, idx_group_2)
2. function tensor = data_cell_to_tensor, returns ordinary tensor build from data cell
3. some tensor NMF

Further documentation can be found in the matlab files of the functions
below. 

%}


%%
%Step 0: Convert your data into a matlab array. Each row of the matrix
%should correspond to a different data point, e.g. patient, and each column
%should correspond to a different feature, e.g. height, age, location, etc.
data_matrix = readmatrix('COVID19_line_list_data.csv');


%%
%Step 1: Convert your data matrix into a cell array.

%Indicies of different groups of features. 


%Each cell of this cell array corresponds to a different data point. It is
%a ktensor associated to groups of feature indices above.  
data_cell = matrix_to_cell(data_matrix, cell_of_groups_of_feature_indices);



%%
%Step 2: Convert to your usual tensor format. 
data_tensor = cell_to_tensor(data_cell);


%%
%Step 3: 

%apply some tensor decomposition algorithm. 





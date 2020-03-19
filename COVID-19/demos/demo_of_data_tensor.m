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




%data_matrix = readmatrix('COVID19_line_list_data.csv');

data_matrix = rand(1000, 24);


%%
%Step 1: Convert your data matrix into a cell array.

%Indicies of different groups of features. 

idx_group_1 = [3, 5, 18, 19, 24];
idx_group_2 = [4, 6, 10, 11];


%Each cell of this cell array corresponds to a different data point. It is
%a ktensor associated to the two groups of features above.  
data_cell = matrix_to_cell(data_matrix, idx_group_1, idx_group_2);



%%
%Step 2: Convert to your usual tensor format. 
data_tensor = cell_to_tensor(data_cell);
data_tensor = tensor(data_tensor);


%%
%Step 3: 

%apply some tensor decomposition algorithm. 
R = 10;
X_kr = ncp(data_tensor, R);




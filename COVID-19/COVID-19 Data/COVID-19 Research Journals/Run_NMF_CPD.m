load('sorted_tfidf_features.mat')
load('sorted_feat_names.mat')

data = full(sorted_tifidf_features);

load('wordLemPoS.mat')
count = 0;
for ii = 1:length(feature_names)
    if max(wordLemPoS.word == feature_names(ii))==0
        count = count+1;
        idx(count)=ii; 
    end
end
idx; % the are 174 words that are not in wordLemPoS

feature_names(idx,:)=[];
data(idx,:)=[];

Tbig = zeros(4826,727,9);
for i=1:9
Tbig(:,:,i) = data(:,(((i-1)*727)+1):(i*727));
end

R=10;
[n1,n2,n3] = size(Tbig);
M = tens2mat(Tbig,1,2:3); %Matricize tensor

[Am,Sm] = nnmf(M,R);

col = 0;
for i=1:n3
   S{i} = Sm(:,col+1:col+n2);
   col = col + n2;
   
end
A = Am;
Thatm = ones(n1,n2,n3);

for i=1:n3
   Thatm(:,:,i) = A*S{i}; 
end
display(['Fixed A NTF Reconstruction error: ',num2str(frob(Tbig-Thatm))]);
displayTens_Alona(S,[1:n3],'S-',1)
figure
imagesc(A)
title('A for fixed A NTF');

% The following code runs NCP on Tbig

U1 = rand(n1,R);
U2 = rand(n2,R);
U3 = rand(n3,R);

model = struct;
model.variables.a = U1;
model.variables.b = U2;
model.variables.c = U3;
model.factors.A = {'a', @struct_nonneg};
model.factors.B = {'b', @struct_nonneg};
model.factors.C = {'c', @struct_nonneg};
model.factorizations.tensor.data = Tbig;
model.factorizations.tensor.cpd = {'A', 'B', 'C'};
sol1 = sdf_nls(model);

Usol1 = sol1.factors;
T1hat = cpdgen({Usol1.A,Usol1.B,Usol1.C});

Enls = frob(T1hat-Tbig);
display(['Fixed NNCP(nls) Reconstruction error: ',num2str(frob(T1hat-Tbig))]);
U{1} = Usol1.A;
U{2} = Usol1.B;
U{3} = Usol1.C;
displayTens_Alona(U,[1:3],'ABC-',1)

% The following code runs NNMF on slices of Tbig
That2 = zeros(n1,n2,n3);
for i=1:n3
    Tslice = reshape(Tbig(:,:,i),n1,n2);
    [W{i},H{i}] = nnmf(Tslice,R);
    That2(:,:,i) = W{i} * H{i};
end
display(['NNMF Reconstruction error: ',num2str(norm(tens2vec(Tbig-That2)))]);

WTens = zeros(n1,R,n3);
HTens = zeros(R,n2,n3);

for i=1:n3
    
    WTens(:,:,i) = W{i};
    HTens(:,:,i) = H{i};
end
    
displayTens_Alona(WTens,[1:n3],'W-');
displayTens_Alona(HTens,[1:n3],'H-');

goodBadID = feature_names;


Mw = zeros(10,R);
I = zeros(10,R);
for r=1:R
[Mw(:,r),I(:,r)]=maxk(U{2}(:,r),10);
goodBadID(I(:,r),:)
end
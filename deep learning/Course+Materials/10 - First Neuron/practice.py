import torch
# print(torch.__version__)

# linear equation by tensor operation :


input_x = torch.tensor([1])
weight = torch.tensor([2])
bias=torch.tensor([3])
y_prediction = input_x*weight + bias
print(y_prediction)
print(type(y_prediction))

# let's create our first neural network : 

from torch import nn

model = nn.Linear(1,1)

print(model.bias)
print(model.weight)

import torch 
from torch import nn


X1 = torch.tensor([[10.0]]) # Input: Temperature in °C
y1 = torch.tensor([[50.0]]) # Actual value: Temperature °F

model = nn.Linear(1 ,1) #(input,output) input defines no input we can give to this neuron and out will decide no neuron it will have to calculate output
optimizer = torch.optim.SGD(model.parameters(),lr=0.0001)
loss_fn = nn.MSELoss()

for i in range(0,10000):
 optimizer.zero_grad()
 outputs=model(X1)
 loss=loss_fn(outputs,y1)
 loss.backward()
 optimizer.step()


print(model(X1))

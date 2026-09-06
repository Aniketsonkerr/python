import torch
from torch import nn

#let's create a batch of data sets from where our model will learn 
X1 = torch.tensor([[50],[100]],dtype=torch.float32)
Y1= torch.tensor([[122],[212]],dtype=torch.float32)


model = nn.Linear(1,1)
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(),lr=0.0001)

for i in range(0 , 150000):
 optimizer.zero_grad()
 outputs=model(X1)
 loss=loss_fn(outputs,Y1)
 loss.backward()
 optimizer.step()

print(model.bias)
print(model.weight)

measurements = torch.tensor([
    [37.5]
], dtype=torch.float32)

model.eval()
with torch.no_grad():
    prediction = model(measurements)
    print(prediction)
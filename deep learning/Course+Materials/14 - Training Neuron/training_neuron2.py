import torch
from torch import nn

# Input: Temperature in °C
X1 = torch.tensor([[10]], dtype=torch.float32) 
# Actual value: Temperature °F
y1 = torch.tensor([[50]], dtype=torch.float32) 

# Input: Temperature in °C
X2 = torch.tensor([[37.78]], dtype=torch.float32) 
# Actual value: Temperature °F
y2 = torch.tensor([[100.0]], dtype=torch.float32) 

model = nn.Linear(1, 1)
loss_fn = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.0001)

for i in range(0, 100000):
    # Training pass
    optimizer.zero_grad()
    outputs = model(X1)
    loss = loss_fn(outputs, y1)
    loss.backward()
    optimizer.step()

    optimizer.zero_grad()
    outputs = model(X2)
    loss = loss_fn(outputs, y2)
    loss.backward()
    optimizer.step()

    if i % 100 == 0: 
        print(model.bias)
        print(model.weight)

y1_pred = model(X1)
print("y1_pred =", y1_pred)
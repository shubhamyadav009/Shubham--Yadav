# 1️⃣ Import libraries
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision.datasets import FashionMNIST
from torchvision.transforms import ToTensor

# 2️⃣ Setup device (GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

# 3️⃣ Load dataset
train_data = FashionMNIST(root="data", train=True, download=True, transform=ToTensor())
test_data = FashionMNIST(root="data", train=False, download=True, transform=ToTensor())

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64)

# 4️⃣ Define the model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.linear_stack(x)

model = NeuralNetwork().to(device)

# 5️⃣ Define loss and optimizer
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001)

# 6️⃣ Training loop
epochs = 5
for epoch in range(epochs):
    model.train()
    for X, y in train_loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        pred = model(X)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()
    
    # Evaluation
    model.eval()
    correct, total, test_loss = 0, 0, 0
    with torch.no_grad():
        for X, y in test_loader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).sum().item()
            total += y.size(0)
    print(f"Epoch {epoch+1}: Test Accuracy: {100*correct/total:.2f}%, Avg Loss: {test_loss/len(test_loader):.4f}")

# 1️⃣ Import Libraries
import torch
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import FashionMNIST, MNIST
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

# 2️⃣ Setup device (GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

# ------------------------------------------------------
# PART A: Autoencoder for FashionMNIST
# ------------------------------------------------------

# 3️⃣ Load FashionMNIST dataset
train_data = FashionMNIST(root="data", train=True, download=True, transform=ToTensor())
test_data = FashionMNIST(root="data", train=False, download=True, transform=ToTensor())

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64)

# 4️⃣ Define Autoencoder
class Autoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 28*28),
            nn.Sigmoid()
        )

    def forward(self, x):
        z = self.encoder(x)
        x_recon = self.decoder(z)
        return x_recon.view(-1, 1, 28, 28)

autoencoder = Autoencoder().to(device)
loss_fn = nn.MSELoss()
optimizer = optim.Adam(autoencoder.parameters(), lr=0.001)

# 5️⃣ Train Autoencoder
epochs = 5
for epoch in range(epochs):
    autoencoder.train()
    for X, _ in train_loader:
        X = X.to(device)
        optimizer.zero_grad()
        X_recon = autoencoder(X)
        loss = loss_fn(X_recon, X)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

# 6️⃣ Visualize reconstruction
autoencoder.eval()
with torch.no_grad():
    X, _ = next(iter(test_loader))
    X = X.to(device)
    X_recon = autoencoder(X)

fig, axes = plt.subplots(2, 8, figsize=(12,3))
for i in range(8):
    axes[0,i].imshow(X[i].cpu().squeeze(), cmap='gray')
    axes[0,i].axis('off')
    axes[1,i].imshow(X_recon[i].cpu().squeeze(), cmap='gray')
    axes[1,i].axis('off')
plt.show()

# ------------------------------------------------------
# PART B: Custom Dataset Classification
# ------------------------------------------------------

# 7️⃣ Define a custom dataset (can also use MNIST)
class CustomDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        X, y = self.dataset[idx]
        return X, y

# Use MNIST as custom dataset
custom_train = CustomDataset(MNIST(root="data", train=True, download=True, transform=ToTensor()))
custom_test = CustomDataset(MNIST(root="data", train=False, download=True, transform=ToTensor()))

train_loader = DataLoader(custom_train, batch_size=64, shuffle=True)
test_loader = DataLoader(custom_test, batch_size=64)

# 8️⃣ Define simple classification model
class SimpleClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_stack = nn.Sequential(
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        return self.linear_stack(self.flatten(x))

model = SimpleClassifier().to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 9️⃣ Training loop
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

    # Evaluate
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for X, y in test_loader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            correct += (pred.argmax(1) == y).sum().item()
            total += y.size(0)
    print(f"Epoch {epoch+1}, Test Accuracy: {100*correct/total:.2f}%")

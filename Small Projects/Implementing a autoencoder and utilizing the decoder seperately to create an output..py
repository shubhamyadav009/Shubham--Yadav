# ===============================
# Autoencoder with Decoder Output
# ===============================

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.datasets import FashionMNIST
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

# -------------------------------
# 1. Device setup
# -------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

# -------------------------------
# 2. Load Dataset
# -------------------------------
train_data = FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor()
)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

# -------------------------------
# 3. Define Autoencoder
# -------------------------------
class AutoEncoder(nn.Module):
    def __init__(self):
        super().__init__()

        # Encoder
        self.encoder = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 50)  # Latent dimension
        )

        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(50, 512),
            nn.ReLU(),
            nn.Linear(512, 28*28)
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)

model = AutoEncoder().to(device)
print(model)

# -------------------------------
# 4. Loss and Optimizer
# -------------------------------
loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

# -------------------------------
# 5. Train Autoencoder
# -------------------------------
epochs = 10
for epoch in range(epochs):
    model.train()
    total_loss = 0

    for X, _ in train_loader:
        X = X.to(device)
        target = X.flatten(start_dim=1)

        optimizer.zero_grad()
        output = model(X)
        loss = loss_fn(output, target)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.6f}")

# -------------------------------
# 6. Use Decoder Separately
# -------------------------------
# Create random latent vector
latent_vector = torch.randn(1, 50).to(device)

# Generate image using decoder only
with torch.no_grad():
    generated = model.decoder(latent_vector)

# Reshape to image
generated_image = generated.view(28, 28).cpu()

# -------------------------------
# 7. Visualize Generated Output
# -------------------------------
plt.figure(figsize=(4, 4))
plt.title("Generated Image using Decoder Only")
plt.imshow(generated_image, cmap="gray")
plt.axis("off")
plt.show()

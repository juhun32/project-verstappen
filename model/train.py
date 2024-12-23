import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
import pandas as pd

# Load data
data = pd.read_csv("driving_data.csv")
X = data[["speed", "steering_angle"]].values  # Features
y = data[["throttle", "brake"]].values  # Controls

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Define the model


class DrivingModel(nn.Module):
    def __init__(self):
        super(DrivingModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(2, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.fc(x)


model = DrivingModel()

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Train
for epoch in range(100):
    inputs = torch.tensor(X_train, dtype=torch.float32)
    targets = torch.tensor(y_train, dtype=torch.float32)
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Save the trained model
torch.save(model.state_dict(), "driving_model.pth")

import torch
import torch.nn as nn
import pandas as pd
import torch.nn.functional as F

torch.cuda.empty_cache()
data = pd.read_csv("mixed_game_data_limit.csv", header=None)
torch_data = torch.tensor(data.values).cuda()
train_len = (int(len(torch_data)*.9)//32)*32
test_len = len(torch_data)-train_len
train, test = torch.utils.data.random_split(torch_data, [train_len, test_len])
train_loader = torch.utils.data.DataLoader(train, batch_size=32, shuffle=True, num_workers=0)
test_loader = torch.utils.data.DataLoader(test, batch_size=32, shuffle=True, num_workers=0)


# Compute the size of the minibatch for training set and test set
trainset_batchsize = train_loader.batch_size
testset_batchsize = test_loader.batch_size

# Print sizes of the minibatch
print(trainset_batchsize, testset_batchsize)

# Define the class Net
class Net(nn.Module):
    def __init__(self):
        # Define all the parameters of the net
        super(Net, self).__init__()
        self.fc1 = nn.Linear(64*12+6, 5000, dtype=float)
        self.fc2 = nn.Linear(5000, 1000, dtype=float)
        self.fc3 = nn.Linear(1000, 1000, dtype=float)
        self.fc4 = nn.Linear(1000, 1000, dtype=float)
        self.fc5 = nn.Linear(1000, 1000, dtype=float)
        self.fc6 = nn.Linear(1000, 1000, dtype=float)
        self.fc7 = nn.Linear(1000, 1000, dtype=float)
        self.fc8 = nn.Linear(1000, 1000, dtype=float)
        self.fc9 = nn.Linear(1000, 500, dtype=float)
        self.fc10 = nn.Linear(500, 500, dtype=float)
        self.fc11 = nn.Linear(500, 500, dtype=float)
        self.fc12 = nn.Linear(500, 200, dtype=float)
        self.fc13 = nn.Linear(200, 200, dtype=float)
        self.fc14 = nn.Linear(200, 1, dtype=float)

    def forward(self, x):
        # Do the forward pass
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = F.relu(self.fc5(x))
        x = F.relu(self.fc6(x))
        x = F.relu(self.fc7(x))
        x = F.relu(self.fc8(x))
        x = F.relu(self.fc9(x))
        x = F.relu(self.fc10(x))
        x = F.relu(self.fc11(x))
        x = F.relu(self.fc12(x))
        x = F.relu(self.fc13(x))
        x = self.fc14(x)
        return x


import torch.optim as optim

# Instantiate the Adam optimizer and Cross-Entropy loss function
model = Net().cuda()
#model.load_state_dict(torch.load("model35.pt"))
optimizer = optim.Adam(model.parameters(), lr=3e-4)
criterion = nn.MSELoss()
for i in range(20000):
    epoch_loss = 0.0
    for batch_idx, data_target in enumerate(train_loader):
        data = data_target[: ,0:64*12+6]
        target = data_target[:,-1:]
        optimizer.zero_grad()

        # Compute a forward pass
        output = model(data)
        if batch_idx % 500 == 0:
            print(batch_idx)
        # Compute the loss gradients and change the weights
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        epoch_loss += loss
    print("Epoch:" + str(i))
    print(epoch_loss)
    if i % 5 == 0:
        print("Saving")
        torch.save(model.state_dict(), "model"+str(i)+".pt")

correct, total = 0, 0

torch.save(model.state_dict(), "model.pt")
# Set the model in eval mode
model.eval()

loss = 0.0
for i, data in enumerate(test_loader, 0):
    inputs = data[:,0:64*12+6]
    labels = data[:,-1:]

    # Do the forward pass and get the predictions
    outputs = model(inputs)
    loss = criterion(outputs, labels)
print('The loss of the network is: %d %%' % loss)

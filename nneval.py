import torch
import torch.nn as nn
import pandas as pd
import torchvision
import torchvision.transforms as transforms
from utils.getannotated import *

# Transform the data to torch tensors and normalize it
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307), (0.3081))
])

# Preparing training set and test set
#trainset = torchvision.datasets.MNIST('mnist', train=True, download=True, transform=transform)
#testset = torchvision.datasets.MNIST('mnist', train=False, download=True, transform=transform)
data = pd.read_csv("utils/data.csv", header=None)
torch_data = torch.tensor(data.values)
train_len = (int(len(torch_data)*.9)//256)*256
test_len = len(torch_data)-train_len
train, test = torch.utils.data.random_split(torch_data, [train_len, test_len])
train_loader = torch.utils.data.DataLoader(train, batch_size=32, shuffle=True, num_workers=0)
test_loader = torch.utils.data.DataLoader(test, batch_size=32, shuffle=True, num_workers=0)

# Prepare training loader and test loader
#train_loader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=True, num_workers=0)
#test_loader = torch.utils.data.DataLoader(testset, batch_size=32, shuffle=False, num_workers=0)

#trainset_shape = train_loader.dataset.data.shape
#testset_shape = test_loader.dataset.data.shape

# Print the computed shapes
#print(trainset_shape, testset_shape)

# Compute the size of the minibatch for training set and test set
trainset_batchsize = train_loader.batch_size
testset_batchsize = test_loader.batch_size

# Print sizes of the minibatch
print(trainset_batchsize, testset_batchsize)

import torch.nn.functional as F


# Define the class Net
class Net(nn.Module):
    def __init__(self):
        # Define all the parameters of the net
        super(Net, self).__init__()
        self.fc1 = nn.Linear(64*12+6, 200, dtype=float)
        self.fc2 = nn.Linear(200, 1, dtype=float)

    def forward(self, x):
        # Do the forward pass
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


import torch.optim as optim

# Instantiate the Adam optimizer and Cross-Entropy loss function
model = Net()
optimizer = optim.Adam(model.parameters(), lr=3e-4)
criterion = nn.L1Loss()
for i in range(20):
    epoch_loss = 0.0
    for batch_idx, data_target in enumerate(train_loader):
        data = data_target[: ,0:64*12+6]
        target = data_target[:,-1:]
        #data = data.view(-1, 28 * 28)
        optimizer.zero_grad()

        # Compute a forward pass
        output = model(data)
        #print(output)
        #print(target)

        # Compute the loss gradients and change the weights
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        epoch_loss += loss
    print(epoch_loss)

correct, total = 0, 0

torch.save(model.state_dict(), "model.pt")
# Set the model in eval mode
model.eval()

b = Board("2kr4/1pp1bp1p/2q5/6Q1/8/P5Pb/1P3P1P/R5K1 w - - 0 28")
b2 = convertBoard(b)
print(torch.tensor(b2))
print(model(torch.tensor(b2, dtype=float)))
'''for i, data in enumerate(test_loader, 0):
    inputs, labels = data

    # Put each image into a vector
    inputs = inputs.view(-1, 28 * 28)

    # Do the forward pass and get the predictions
    outputs = model(inputs)
    _, outputs = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += (outputs == labels).sum().item()
print('The test set accuracy of the network is: %d %%' % (100 * correct / total))'''
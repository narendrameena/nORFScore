#!/usr/bin/env python3 
###-----------------------------------------------------------------------------##
#
#@author narumeena
#@descripton class and function to implement multilayer perceptron 
#@inspiration https://medium.com/biaslyai/pytorch-introduction-to-neural-network-feedforward-neural-network-model-e7231cff47cb
#
###-----------------------------------------------------------------------------##

import torch 
import torch.nn as nn
import torch.nn.functional as F 
import numpy



"""
class multiLayerPerceptron(nn.Module):
    def __init__(self):
        super(multiLayerPerceptron, self).__inti__()
        #input layer 
        self.inputLayer             =   nn.Linear(76,40)
        self.relu                   =   nn.ReLU()
        #first hidden layer 
        self.hiddenLayer            =   nn.Linear(40,15)
        self.relu                   =   nn.ReLU()
        #output layer 
        self.outputLayer            =   nn.Linear(15,2)
        self.sigmoid                =   nn.Sigmoid()


    def forward(self,x):
        x   =   F.relu(self.inputLayer(x))
        x   =   F.relu(self.hiddenLayer(x))
        x   =   self.outputLayer(x)
        return x

"""



class Feedforward(torch.nn.Module):
        def __init__(self, input_size, hidden_size):
            super(Feedforward, self).__init__()
            self.input_size = input_size
            self.hidden_size  = hidden_size
            self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)
            self.relu = torch.nn.ReLU()
            self.fc2 = torch.nn.Linear(self.hidden_size, 1)
            self.sigmoid = torch.nn.Sigmoid()
        def forward(self, x):
            hidden = self.fc1(x)
            relu = self.relu(hidden)
            output = self.fc2(relu)
            output = self.sigmoid(output)
            return output




def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    print(device)
    device  =   'cpu'
    print(device)
    # CREATE RANDOM DATA POINTS
    from sklearn.datasets import make_blobs
    def blob_label(y, label, loc): # assign labels
        target = numpy.copy(y)
        for l in loc:
            target[y == l] = label
        return target
    x_train, y_train = make_blobs(n_samples=400000, n_features=76, cluster_std=1.5, shuffle=True)
    print(x_train[0:5,:])
    print(y_train[0:5])
    x_train = torch.FloatTensor(x_train,device=device)
    y_train = torch.FloatTensor(blob_label(y_train, 0, [0]),device=device)
    y_train = torch.FloatTensor(blob_label(y_train, 1, [1,2,3]),device=device)
    x_test, y_test = make_blobs(n_samples=10, n_features=76, cluster_std=1.5, shuffle=True)
    x_test = torch.FloatTensor(x_test,device=device)
    y_test = torch.FloatTensor(blob_label(y_test, 0, [0]),device=device)
    y_test = torch.FloatTensor(blob_label(y_test, 1, [1,2,3]),device=device)


    model = Feedforward(76, 10)
    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr = 0.01)

    model.eval()
    y_pred = model(x_test)
    before_train = criterion(y_pred.squeeze(), y_test)
    print('Test loss before training' , before_train.item())


    model.train()
    epoch = 10
    for epoch in range(epoch):
        optimizer.zero_grad()
        # Forward pass
        y_pred = model(x_train)
        # Compute Loss
        loss = criterion(y_pred.squeeze(), y_train)
   
        print('Epoch {}: train loss: {}'.format(epoch, loss.item()))
        # Backward pass
        loss.backward()
        optimizer.step()

        #Additional Info when using cuda
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        if device == 'cuda:0':
            print(torch.cuda.get_device_name(0))
            print('Memory Usage:')
            print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
            print('Cached:   ', round(torch.cuda.memory_cached(0)/1024**3,1), 'GB')


if __name__ == "__main__":
    main()
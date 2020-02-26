#!/usr/bin/env python3 
#example 

import torch
import numpy 
import pandas as pd
from sklearn.model_selection import train_test_split



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

    data    =   pd.read_csv("../../../analysis/trainingDataSet/training_one_hot_encoding_Coding_region_only.csv", sep="\t")   

    labels  =   data['category']
    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test    =   train_test_split(data.drop('category', axis = 1), labels, test_size = 0.25, random_state = 100)

    x_train =   torch.cuda.DoubleTensor(X_train.values).float()
    print(x_train.shape)
    y_train =   torch.cuda.DoubleTensor(Y_train.values).float()
    x_test  =   torch.cuda.DoubleTensor(X_test.values).float()
    print(x_test.shape)
    y_test  =   torch.cuda.DoubleTensor(Y_test.values).float()

    model = Feedforward(73, 10).to(device)
    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr = 0.01)


    model.eval().to(device)
    y_pred = model(x_test).to(device)
    before_train = criterion(y_pred.squeeze(), y_test)
    print('Test loss before training' , before_train.item())



    model.train().to(device)
    epoch = 100000000
    for epoch in range(epoch):
        optimizer.zero_grad()
        # Forward pass
        y_pred = model(x_train).to(device)
        # Compute Loss
        loss = criterion(y_pred.squeeze(), y_train)
   
        print('Epoch {}: train loss: {}'.format(epoch, loss.item()))


        #Additional Info when using cuda
        if device.type == 'cuda':
            print(torch.cuda.get_device_name(0))
            print('Memory Usage:')
            print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
            print('Cached:   ', round(torch.cuda.memory_cached(0)/1024**3,1), 'GB')

        # Backward pass
        loss.backward()
        optimizer.step()

    model.eval()
    y_pred = model(x_test).to(device)
    after_train = criterion(y_pred.squeeze(), y_test) 
    print('Test loss after Training' , after_train.item())



if __name__ == "__main__":
    main()
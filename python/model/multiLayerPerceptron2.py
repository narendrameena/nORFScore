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
import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split




class multiLayerPerceptron(nn.Module):
    def __init__(self):
        super(multiLayerPerceptron, self).__init__()
        #input layer 
        self.inputLayer             =   nn.Linear(73,40)
   
        #first hidden layer 
        self.hiddenLayer            =   nn.Linear(40,15)

        #output layer 
        self.outputLayer            =   nn.Linear(15,2)


    def forward(self,x):
        x   =   F.relu(self.inputLayer(x))
        x   =   F.relu(self.hiddenLayer(x))
        x   =   self.outputLayer(x)
        return x





def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    print(device)
    device = 'cpu'
    data    =   pd.read_csv("../../../analysis/trainingDataSet/training_one_hot_encoding_Coding_region_only.csv", sep="\t")   

    labels  =   data['category']
    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test    =   train_test_split(data.drop('category', axis = 1), labels, test_size = 0.25, random_state = 100)

    x_train =   torch.FloatTensor(X_train.to_numpy(),device=device)
    y_train =   torch.FloatTensor(Y_train.to_numpy(),device=device)
    x_test  =   torch.FloatTensor(X_test.to_numpy(),device=device)
    y_test  =   torch.FloatTensor(Y_test.to_numpy(),device=device)


    model = multiLayerPerceptron()
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
        y_pred = model(x_train).to(device)
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
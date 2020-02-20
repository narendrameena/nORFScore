#!/usr/bin/env python3 
###-----------------------------------------------------------------------------##
#
#@author narumeena
#@descripton class and function to implement multilayer perceptron 
#@inspiration https://medium.com/biaslyai/pytorch-introduction-to-neural-network-feedforward-neural-network-model-e7231cff47cb
#
###-----------------------------------------------------------------------------##


from __future__ import print_function
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data
import torch.optim as optim
from torch.autograd import Variable
from sklearn.model_selection import train_test_split

def myfunction(x,p=[1,0]):  # function to be learned, with its parameters
    return p[0]*np.sin(100*p[1]*x)    # try just a sine wave, with amplitude & frequency


def myfunc_stacked(X):
    Y = []
    for i in range(X.shape[0]):
        x = X[i,0]
        p1 = X[i,1]
        p2 = X[i,2]
        p = [p1,p2]
        Y.append( myfunction(x,p))
    return np.array(Y)


def stack_params(X, p=None):  # encapsulates parameters with X
    if p is None:
        p0 = np.random.rand(len(X))  # random values throughout X
        p1 = np.random.rand(len(X)) 
    else:
        p0 = np.ones(len(X)) * p[0]  # stack copies of params with X
        p1 = np.ones(len(X)) * p[1]

    return np.array(list(zip(X,p0,p1)))


def gen_data(n=1000, n_params=2, rand_all=False):
    X = np.linspace(-1.0,1.0,num=n)
    if (not rand_all):
        p = np.random.random(n_params)-0.5
    else:
        p = None
    X = stack_params(X,p)
    Y = myfunc_stacked(X)
    return X, Y, p
   

def make_model(X, n_hidden):

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.hidden = nn.Linear(X.shape[1], n_hidden)
            self.hidden2 = nn.Linear(n_hidden, n_hidden)
            self.out   = nn.Linear(n_hidden, 1)

        def forward(self, x):
            x = F.relu(self.hidden(x))
            x = F.tanh(self.hidden2(x))
            x = self.out(x)
            return x

        # Note: "backward" is automatically defined by torch.autograd
    
    model = Net()

    if torch.cuda.is_available():
        print("Using CUDA, number of devices = ",torch.cuda.device_count())
        model.cuda()
    return model


def plot_prediction(X_test, Y_test, Y_pred, epoch, n_epochs, p_test):
    fig=plt.figure()
    plt.clf()
    ax = plt.subplot(1,1,1)
    ax.set_ylim([-1,1])
    plt.title("Epoch #"+str(epoch)+"/"+str(n_epochs)+", p = "+str(p_test))
    plt.plot(X_test[:,0],Y_test,'b-',label="True")
    plt.plot(X_test[:,0],Y_pred,'r-',label="Predicted")
    plt.legend()
    plt.savefig('progress.png')
    plt.close(fig)
    return


def train(model, epoch, trainloader, criterion, optimizer):
    model.train()
    for batch_idx, (data, target) in enumerate(trainloader):
        if torch.cuda.is_available():
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output,target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.data[0]))


def predict(model,testloader, X_test, Y_test,  epoch, n_epochs, p_test):
    model.eval()
    print(" Plotting....")
    Y_pred = []
    for data, target in testloader:
        if torch.cuda.is_available():
            data = data.cuda()
        data = Variable(data, volatile=True)
        output = model(data)
        Y_pred.append(output.numpy)

    Y_pred = np.array(Y_pred)
    plot_prediction(X_test, Y_test, Y_pred, epoch, n_epochs, p_test)


def main():
    # parameters for 'size' of run
    n_hidden = 100
    batch_size = 20
    data    =   pd.read_csv("../../../analysis/trainingDataSet/training_one_hot_encoding_Coding_region_only.csv", sep="\t")   

    labels  =   data['category']
    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test    =   train_test_split(data.drop('category', axis = 1), labels, test_size = 0.25, random_state = 100)

    X_train = X_train.to_numpy().astype(float)
    Y_train = Y_train.to_numpy().astype(float)
    X_test  = X_test.to_numpy().astype(float)
    Y_test  = Y_test.to_numpy().astype(float)

    trainset = torch.utils.data.TensorDataset(torch.from_numpy(X_train),torch.from_numpy(Y_train))
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=20, shuffle=True, num_workers=2)
    testset = torch.utils.data.TensorDataset(torch.from_numpy(X_test),torch.from_numpy(Y_test))
    testloader = torch.utils.data.DataLoader(testset, batch_size=1, shuffle=False, num_workers=2)


    print("Defining model")
    model = make_model(X_train, n_hidden)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    n_epochs= 10000
    predict_every = 20
    for epoch in range(n_epochs):
        print("(Outer) Epoch ",epoch," of ",n_epochs,":")

        train(model, epoch, trainloader, criterion, optimizer)

        if (0 == epoch % predict_every):
            predict(model,testloader, X_test, Y_test, epoch, n_epochs, Y_test)

if __name__ == '__main__':
    main()
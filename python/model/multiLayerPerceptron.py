#!/usr/bin/env python3 
###-----------------------------------------------------------------------------------------##
#
#@author narumeena
#@description implementation of multilayer perceptron 
#@source https://medium.com/biaslyai/pytorch-introduction-to-neural-network-feedforward-neural-network-model-e7231cff47cb
#
###------------------------------------------------------------------------------------------##
import time
start_time1 = time.time()
import torch
import numpy 
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix,accuracy_score, roc_curve, auc


class Feedforward(torch.nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Feedforward, self).__init__()
        self.input_size = input_size
        self.hidden_size  = hidden_size
        self.fc1 = torch.nn.Linear(self.input_size, 1000)
        self.relu = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(1000, 50)
        self.relu = torch.nn.ReLU()
        self.fc3 = torch.nn.Linear(50, self.hidden_size)
        self.relu = torch.nn.ReLU()
        self.fc4 = torch.nn.Linear(self.hidden_size, 1)
        self.sigmoid = torch.nn.Sigmoid()
    def forward(self, x):
        hidden  =   self.fc1(x)
        relu    =   self.relu(hidden)
        hidden1 =   self.fc2(relu)
        relu    =   self.relu(hidden1)
        output  =   self.fc3(relu)
        relu    =   self.relu(output)
        output  =   self.fc4(relu)
        output  =   self.sigmoid(output)
        return output



def main():


    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    print(device)

    data    =   pd.read_csv("../../../analysis/trainingDataSet/training_one_hot_encoding_Coding_region_only.csv", sep="\t")   

    labels  =   data['category']
    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test    =   train_test_split(data.drop('category', axis = 1), labels, test_size = 0.25, random_state = 100)
    end_time1 = time.time()
    x_train =   torch.cuda.DoubleTensor(X_train.values).float()
    print(x_train.shape)
    y_train =   torch.cuda.DoubleTensor(Y_train.values).float()
    x_test  =   torch.cuda.DoubleTensor(X_test.values).float()
    print(x_test.shape)
    y_test  =   torch.cuda.DoubleTensor(Y_test.values).float()
    

    start_time2 = time.time()
    model = Feedforward(73, 10).to(device)
    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr = 0.01)


    model.eval().to(device)
    y_pred = model(x_test).to(device)
    before_train = criterion(y_pred.squeeze(), y_test)
    print('Test loss before training' , before_train.item())



    model.train().to(device)
    epoch = 1000000
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

    prediction2 = y_pred.cpu().detach().numpy()
    
    prediction_prob = prediction2[:,0]
    prediction_binary = numpy.where(prediction_prob>0.5,1,0)
 
    #Print accuracy
    acc_NN = accuracy_score(y_test.cpu(), prediction_binary)
    print('Overall accuracy of Neural Network model:', acc_NN)
 
    # #Print Area Under Curve
    false_positive_rate, recall, thresholds = roc_curve( y_test.cpu(), prediction_prob)
    roc_auc = auc(false_positive_rate, recall)
    plt.figure()
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.plot(false_positive_rate, recall, 'b', label = 'AUC = %0.3f' %roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0,1], [0,1], 'r--')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.0])
    plt.ylabel('Recall')
    plt.xlabel('Fall-out (1-Specificity)')
    plt.savefig('/mnt/hdd1/narendra/cambridge/projects/inProgress/nORFScore/figures/firstMLP.png')
    end_time2 = time.time()
 
    print('Loading and pre-processing time: ', end_time1-start_time1)
    print('Execution time: ', end_time2-start_time2)



    after_train = criterion(y_pred.squeeze(), y_test) 
    print('Test loss after Training' , after_train.item())
    plt.show()


if __name__ == "__main__":
    main()
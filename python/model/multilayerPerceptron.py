#!/usr/bin/env python3 
###-----------------------------------------------------------------------------##
#
#@author narumeena
#@descripton class and function to implement multilayer perceptron 
#
###-----------------------------------------------------------------------------##

import torch 
import torch.nn as nn
import torch.nn.functional as F 


class multiLayerPerceptron(nn.Module):
    def __init__(self):
        super(multiLayerPerceptron, self).__inti__()
        #input layer 
        self.inputLayer             =   nn.Linear(76,40)
        #first hidden layer 
        self.hiddenLayer            =   nn.Linear(40,15)
        #output layer 
        self.outputLayer            =   nn.Linear(15,2)

    def forward(self,x):
        x   =   F.relu(self.inputLayer(x))
        x   =   F.relu(self.hiddenLayer(x))
        x   =   self.outputLayer(x)
        return x


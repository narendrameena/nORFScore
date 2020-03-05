#!/usr/bin/env python3 
###-----------------------------------------------------------------------------------------##
#
#@author narumeena
#@description implementation of multilayer perceptron with GAN
#@source https://blog.usejournal.com/train-your-first-gan-model-from-scratch-using-pytorch-9b72987fd2c0
#
###------------------------------------------------------------------------------------------##



import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable

# generating dataset for discriminator
def get_dataset():
    return torch.cuda.FloatTensor(np.random.normal(4,1.25,(1,100)))

# generating noise for generator
def make_noise():
    return torch.cuda.FloatTensor(np.random.uniform(0,0,(1,50)))

class generator(nn.Module):
    
    def __init__(self,inp,out):
        super(generator,self).__init__()
        self.net = nn.Sequential(nn.Linear(inp,300),
                                 nn.ReLU(inplace=True),
                                nn.Linear(300,300),
                                 nn.ReLU(inplace=True),
                                nn.Linear(300,out)
                               )
        
    def forward(self,x):
        x = self.net(x)
        return x

class discriminator(nn.Module):
    
    def __init__(self,inp,out):
        super(discriminator,self).__init__()
        self.net = nn.Sequential(nn.Linear(inp,300),
                                 nn.ReLU(inplace=True),
                                 nn.Linear(300,300),
                                 nn.ReLU(inplace=True),
                                 nn.Linear(300,out),
                                 nn.Sigmoid()
                                )
        
    def forward(self,x):
        x = self.net(x)
        return x







def main():


    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    print(device)

    def stats(array):
        array = array.detach().numpy()
        return [np.mean(array),np.std(array)]

    gen = generator(50,100).to(device)
    x = make_noise()

    x1 = gen(x)
    stats(x1.cpu())
    
    
    discrim = discriminator(100,1).to(device)

    x2 = discrim(x1)
    epochs = 50000

    d_step = 10
    g_step = 8
    criteriond1 = nn.BCELoss().to(device)
    optimizerd1 = optim.SGD(discrim.parameters(), lr=0.001, momentum=0.9)

    criteriond2 = nn.BCELoss().to(device)
    optimizerd2 = optim.SGD(gen.parameters(), lr=0.001, momentum=0.9)

    printing_steps = 20

    for epoch in range(epochs):
    
        if epoch%printing_steps==0:
            print("Epoch:", epoch)
    
        # training discriminator
        for d_i in range(d_step):
            discrim.zero_grad()
            
            #real
            data_d_real = Variable(get_dataset())
            data_d_real_pred = discrim(data_d_real).to(device)
            data_d_real_loss = criteriond1(data_d_real_pred,Variable(torch.ones(1,1).to(device)))
            data_d_real_loss.backward()
            
            
            #fake
            data_d_noise = Variable(make_noise())
            data_d_gen_out = gen(data_d_noise).detach()
            data_fake_dicrim_out = discrim(data_d_gen_out).to(device)
            data_fake_d_loss = criteriond1(data_fake_dicrim_out,Variable(torch.zeros(1,1).to(device)))
            data_fake_d_loss.backward()
            
            optimizerd1.step()
        
        for g_i in range(g_step):
            
            gen.zero_grad()
            
            data_noise_gen = Variable(make_noise())
            data_g_gen_out = gen(data_noise_gen)
            data_g_dis_out = discrim(data_g_gen_out)
            data_g_loss = criteriond2(data_g_dis_out,Variable(torch.ones(1,1).to(device)))
            data_g_loss.backward()
            
            optimizerd2.step()
            
            if epoch%printing_steps==0:
                print(stats(data_g_gen_out.cpu()))
        
        if epoch%printing_steps==0:
            print("\n\n")


if __name__ == "__main__":
    main()


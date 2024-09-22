import torch 
import torch.nn as nn
import torch.nn.functional as F

class cnn2(nn.Module):
    def __init__(self):
        super(cnn2,self ).__init__()
        self.conv1 = nn.Conv2d(3,32,5, padding=2)
        self.maxpool1 = nn.MaxPool2d(5, stride=5,padding=1)
        
        self.conv2 = nn.Conv2d(32,64,5, padding=2)
        self.maxpool2 = nn.MaxPool2d(5, stride=5,padding=1)

        
        self.conv3 = nn.Conv2d(64,128,5, padding=2)
        self.maxpool3 = nn.MaxPool2d(5, stride=5,padding=1)

        self.d1 = nn.Linear( 1152 , 2048 )
        #self.dropout4 = nn.Dropout(p=0.2)

        self.d2 = nn.Linear( 2048, 2048 )
        self.dropout5 = nn.Dropout(p=0.2)
        
        self.d3 = nn.Linear(2048,5)
        self.soft = nn.Softmax(dim =1)
        

    def forward (self , inputs):

        x = F.relu(self.conv1(inputs))
        x = self.maxpool1(x)
        
        x = F.relu(self.conv2(x))
        x = self.maxpool2(x)
        
        x = F.relu(self.conv3(x))
        x = self.maxpool3(x)
        #print( x.shape)

        x = x.view(-1,1152)

        x = F.relu(self.d1(x))

        x = F.relu(self.d2(x))
        x = self.dropout5(x)
        
        x = self.soft(self.d3(x))
        return x  


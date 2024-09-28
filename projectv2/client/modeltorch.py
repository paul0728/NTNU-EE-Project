import torch 
import torch.nn as nn
import torch.nn.functional as F

class cnn(nn.Module):
    def __init__(self):
        super(cnn,self ).__init__()
        self.conv1 = nn.Conv2d(3,32,5, padding=2)
        self.maxpool1 = nn.MaxPool2d(5, stride=5,padding=2)
        self.dropout1=nn.Dropout2d(p=0.2)
        
        self.conv2 = nn.Conv2d(32,64,5, padding=2)
        self.maxpool2 = nn.MaxPool2d(5, stride=5,padding=2)
        self.dropout2=nn.Dropout2d(p=0.2)
        
        self.conv3 = nn.Conv2d(64,32,5, padding=2)
        self.maxpool3 =nn.MaxPool2d(5, stride=5,padding=2)
        self.dropout3=nn.Dropout2d(p=0.2)
        
        self.flatten = nn.Flatten()
        self.d1 = nn.Linear( 512,1024 )
        self.dropout4=nn.Dropout(p=0.2)
        
        self.d2 = nn.Linear(1024,5)
        self.soft = nn.Softmax(dim =1)
        

    def forward (self , inputs):
        x = F.relu(self.conv1(inputs))
        x = self.maxpool1(x)
        x = self.dropout1(x)
        
        x = F.relu(self.conv2(x))
        x = self.maxpool2(x)
        x = self.dropout2(x)
        
        x = F.relu(self.conv3(x))
        x = self.maxpool3(x)
        x = self.dropout3(x)
        
        
        x = self.flatten(x)
        x = F.relu(self.d1(x))
        x = self.dropout4(x)
        
        x = self.soft(self.d2(x))
        return x  



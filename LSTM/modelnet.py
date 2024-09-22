import torch 
import torch.nn as nn
import torch.nn.functional as F


class LSTMnet(nn.Module):
	def __init__(self,inputs,hidden,class_size):
		super(LSTMnet,self).__init__()

		self.hidden=hidden
		self.lstm=nn.LSTM(inputs,hidden)
		self.hidden=nn.Linear(hidden,class_size)

	def forward(self, inputs):
		lstm_out,_=self.lstm(inputs)
		tag_space=self.hidden(lstm_out.view(len(inputs),-1))
		x=F.log_softmax(tag_space,dim=1)
		return x

class CNNnet(nn.Module):
	def __init__(self):
		super(CNNnet,self).__init__()		
		self.c1=nn.Conv2d(1,8,3,padding=1)

	def forward(self, inputs ):
		x=F.relu(self.c1(inputs))
		return x

from modelnet import CNNnet
from modelnet import LSTMnet

from RunBuilder import RunBuilder
from RunBuilder import RunManager

from collections import OrderedDict
import torch
import torch.nn.functional as F

import torchvision
import torchvision.transforms as transforms
from torchvision.transforms  import  ToTensor 
import torch.optim as optim 

def train():
	params=OrderedDict(lr=[.01,.001],
		batch_size=[1],
		epochs=[5])

	train_set =torchvision.datasets.UCF101("/data2/users/paul/UCF-101","/data2/users/paul/ucfTrainTestlist",5,train=True)

	m=RunManager()
	for run  in RunBuilder.get_runs(params):
		lstm=LSTMnet(352*640*8,100,6)
		cnn=CNNnet()
		train_loader=torch.utils.data.DataLoader(train_set ,batch_size=run.batch_size, num_workers=2)
		optimizer=optim.Adam(lstm.parameters(),lr=run.lr)
		optimizer2=optim.Adam(cnn.parameters(),lr=run.lr)
		m.begin_run(run,lstm,cnn,train_loader)

		for epoch in range(run.epochs):
			m.begin_epoch()
			sample=next(iter(train_loader))

			for batch in train_loader:
				seq = batch[0]
				tag = batch[2]
				# seq,tags=get_sequence(video,label)
				seq=cnn(seq)
				size=list(seq.size())
				seq=seq.reshape(size[0],1,size[1]*size[2]*size[3])
				preds=lstm(seq)
				loss=F.cross_entropy(preds,tag)
				loss.backward()
				optimizer.step()
				m.track_loss(loss)
				m.track_num_correct(preds,tag)
				
			m.end_epoch()

		m.end_run()

	m.save('results')



def get_sequence(video,label):
	tags=[]
	seq=torch.zeros(1,1,1080,1080)
	n=0
	video.set(cv2.CAP_PROP_POS_MSEC,(n*100/3))
	success, image=video.read()
	while  success==True:
		img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		imaget=ToTensor()(img_gray)
		imaget=imaget.unsqueeze(0)
		seq=torch.cat((imaget,seq),0)
		tags.append(label)
		n+=1
		video.set(cv2.CAP_PROP_POS_MSEC,(n*100/3))
		success, image=video.read()
	seq=torch.cat([seq[:-1]])
	return seq,tags 

def tag_index(tag_list,tags_index):
	indexes=[]
	for i in tag_list:
		indexes.append(tags_index.index(i))
	indexes=torch.LongTensor(indexes)
	return indexes

train()
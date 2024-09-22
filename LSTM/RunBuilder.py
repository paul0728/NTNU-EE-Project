from collections import OrderedDict
from collections import namedtuple 
from itertools import product 
import torchvision.utils 
import pandas as pd
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from IPython.display import display, clear_output
import time
import json

class RunBuilder():
	@staticmethod 
	def get_runs(params):
		Run =namedtuple('Run',params.keys())
		runs=[]

		for v in product(*params.values()):
			runs.append(Run(*v))

		return runs 

class RunManager():

	def __init__(self):
		self.epoch_count=0
		self.epoch_loss=0
		self.epoch_num_correct=0
		self.epoch_start_time=None

		self.run_params=None 
		self.run_count=0
		self.run_data=[]
		self.run_start_time=None

		self.network= None 
		self.network2= None 
		self.loader=None 
		self.tb=None 

	def begin_run(self,run,network,network2,loader):
		self.run_start_time=time.time()

		self.run_params=run

		self.run_count +=1

		self.network=network
		self.network2=network2
		self.loader=loader
		self.tb=SummaryWriter(comment = "-{}".format(run))

		images,_,labesl=next(iter(self.loader))
		# grid=torchvision.utils.make_grig(images)

		# self.tb.add_video('video',grid)
		# self.tb.add_graph(self.network,images)

	def end_run(self):
		self.tb.close()
		self.epoch_count=0

	def begin_epoch(self):
		self.epoch_start_time=time.time()
		self.epoch_count+=1
		self.epoch_loss=0
		self.epoch_num_correct=0

	def track_loss(self,loss):
		self.epoch_loss+=loss.item()*self.loader.batch_size
		

	def end_epoch(self):
		epoch_duration =time.time()-self.epoch_start_time
		run_duration=time.time() - self.run_start_time 

		loss=self.epoch_loss/len(self.loader.path_list)
		accuracy=self.epoch_num_correct/len(self.loader.path_list)

		# for name, param in self.network.named_parameters():
		# 	self.tb.add_histogram(name,param,self.epoch_count)
		# 	self.tb.add_histogram('{}.grad'.format(name),param.grad,self.epoch_count)

		# for name, param in self.network2.named_parameters():
		# 	self.tb.add_histogram(name,param,self.epoch_count)
		# 	self.tb.add_histogram('{}.grad'.format(name),param.grad,self.epoch_count)


		results=OrderedDict()
		results["run"]=self.run_count
		results["epoch"]=self.epoch_count
		results["loss"]=loss
		results["acurracy"]=accuracy
		results["epoch duration"]=epoch_duration
		results['run duration']=run_duration
		for k,v in self.run_params._asdict().items():results[k]=v
		self.run_data.append(results)
		df=pd.DataFrame.from_dict(self.run_data,orient="columns")

	def track_num_correct(self,preds,labels):
		self .epoch_num_correct+=self._get_num_correct(preds,labels)

	def _get_num_correct(self ,preds,labels):
		return preds.argmax(dim=1).eq(labels).sum().item()

	def save(self,fileName):
		pd.DataFrame.from_dict(self.run_data,orient="columns").to_csv("{}.csv".format(fileName))

		with open("{}.json".format(fileName),'w',encoding='utf-8')as f :
			json.dump(self.run_data,f,ensure_ascii=False,indent=4)
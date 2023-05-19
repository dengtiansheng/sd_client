from datasets import load_dataset
import random

class prompt_generator:

	dataset = None
	ds_len = -1

	def __init__(self):

		self.dataset = load_dataset("parquet", data_files={'train': 'conf/train.parquet'})
		print(self.dataset)
		self.ds_len = len(self.dataset['train'])

	def random_prompt(self):
		print(self.ds_len)
		index = random.randint(0, self.ds_len - 1)
		print(index)
		return self.dataset['train'][index]


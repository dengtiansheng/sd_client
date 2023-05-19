from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
from conf import conf
import random
import prompt



class Item(BaseModel):
	model_id: int | None = 1000
	prompt: str
	negative_prompt: str | None = ""
	seed: int | None = -1 
	width: int | None = 512
	height: int | None = 512

	def to_dict(self):
		return {
			"model_id" : self.model_id,
			"prompt" : self.prompt,
			"negative_prompt" : self.negative_prompt,
			"seed" : self.seed,
			"width" : self.width,
			"height" : self.height
		}


def submit_post(url: str, item: Item):
	return requests.post(url, json.dumps(item.to_dict()))

def check_exist(model_id : int):
	return model_id in MODEL_SETTINGS

def random_route(model_id : int):
	model =  conf.MODEL_SETTINGS[model_id]
	instance_num = len(model['hosts'])
	index = random.randint(0,instance_num - 1) 
	url = "http://"+model['hosts'][index]+"/sdapi/v1/"+model['type']
	return url


app = FastAPI()
prompt_generator = prompt.prompt_generator()


@app.get("/")
def read_root():
	return {"welcome": "glad to see you"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
	return {"item_id": item_id, "q": q}

@app.get("/v1/random_prompt")
def random_prompt():
	return prompt_generator.random_prompt()

@app.post("/v1/text2img")
def text2img(item:Item):
	res = {}
	model_id = item.model_id

	if check_exist == False:
		res["msg"] = STATUS_MODEL_ID_NOT_EXIST
		return res

	txt2img_url = random_route(model_id)
	#txt2img_url = 'http://112.83.192.109:7861/sdapi/v1/txt2img'
	response = submit_post(txt2img_url, item).json()
	image_base64 = response['images']
	res = {"data":{"image_base64": image_base64[0],"detail": ""}}
	return res
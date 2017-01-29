'''For checking the markov model works'''

import os,json
import time
from slackclient import SlackClient
import markovify

###########  Functions for poem generation ###########
def load_model():
	"""
	Load the markov chain model for text generation. 
	Should be called at startup.
	"""
	with open('./markov_model.json', 'r') as f:
		model_json = json.load(f)

	markov_model = markovify.Text.from_json(model_json)
	return markov_model

def write_poem(n_lines):
	poem = []

	for line in range(n_lines):
		poem.append(new_line())
	return poem

def new_line():
	l = markov_model.make_short_sentence(60)
	if l!=None:
		return l
	else:
		l=new_line()
		return l

def print_poem(poem):
	return '\n'.join(poem)

##### Write some poems ####

markov_model = load_model()
pm =write_poem(5)
print(pm)
pm = print_poem(pm)

print(pm)
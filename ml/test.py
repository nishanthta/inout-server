from __future__ import print_function	

from inputHandler import word_embed_meta_data, create_test_data
from config import siamese_config
from operator import itemgetter
from keras.models import load_model
from load import load_sts
import numpy as np
from argparse import ArgumentParser
import json

parser = ArgumentParser(description = "description")
parser.add_argument('--desc', '-ds', default = '')
parser.add_argument('--identity', '-id', default = '0') #0 for app, 1 for ad
args = parser.parse_args()

data,summaries = [],[]

if int(args.identity) == 0:
	with open('./ads.json') as f:
		data = json.load(f)
	data = data[0]
	test_sentence_pairs = []
	summaries = [x['summary'] for x in data]
	for i in range(len(data)):
		temp = (str(args.desc),summaries[i])
		test_sentence_pairs.append(temp)	
else:
	with open('./apps.json') as f:
		data = json.load(f)
	data = data[0]
	test_sentence_pairs = []
	summaries = [x['summary'] for x in data]
	for i in range(len(data)):
		temp = (str(args.desc),summaries[i])
		test_sentence_pairs.append(temp)	

sentences1, sentences2, labels = load_sts('sick2014.txt')

labels_dict = {}

for i in range(len(labels)):
	if labels[i] < 2 :
		labels_dict[i] = [1,0,0,0]
	elif labels[i] < 3:
		labels_dict[i] = [0,1,0,0]
	elif labels[i] < 4:
		labels_dict[i] = [0,0,1,0]
	else:
		labels_dict[i] = [0,0,0,1]

# for i in range(len(labels)):
# 	labels[i] = float(labels[i]) / 5.

is_similar = []

for _,val in labels_dict.items():
	is_similar.append(val)

######## Word Embedding ############

tokenizer, embedding_matrix = word_embed_meta_data(sentences1 + sentences2,  siamese_config['EMBEDDING_DIM'])

embedding_meta_data = {
	'tokenizer': tokenizer,
	'embedding_matrix': embedding_matrix
}

## creating sentence pairs
sentences_pair = [(x1, x2) for x1, x2 in zip(sentences1, sentences2)]
del sentences1
del sentences2

class Configuration(object):
	"""yo"""



CONFIG = Configuration()

CONFIG.embedding_dim = siamese_config['EMBEDDING_DIM']
CONFIG.max_sequence_length = siamese_config['MAX_SEQUENCE_LENGTH']
CONFIG.number_lstm_units = siamese_config['NUMBER_LSTM']
CONFIG.rate_drop_lstm = siamese_config['RATE_DROP_LSTM']
CONFIG.number_dense_units = siamese_config['NUMBER_DENSE_UNITS']
CONFIG.activation_function = siamese_config['ACTIVATION_FUNCTION']
CONFIG.rate_drop_dense = siamese_config['RATE_DROP_DENSE']
CONFIG.validation_split_ratio = siamese_config['VALIDATION_SPLIT']

best_model_path = './lstm_50_50_0.17_0.25.h5'

model = load_model(best_model_path)


# test_sentence_pairs = [('" Men Fashion Clothes Style " Applicatin Includes all the latest fashion trends, news and guides for 2018.style | Get the latest mens fashion and style trends, celebrity style photos ','Shop designer clothes and accessories at Hugo Boss. Find the latest designer suits, clothing &amp; accessories for men and women at the official Hugo Boss online store.')]
# test_sentence_pairs.append(('" Men Fashion Clothes Style " Applicatin Includes all the latest fashion trends, news and guides for 2018.style | Get the latest mens fashion and style trends, celebrity style photos ','Buy trendy apparel, accessories and footwear online. Shop across various collections from Raymond, Park Avenue, ColorPlus &amp; Parx Shirts, T-Shirts, Trousers, Dresses, footwear'))

test_data_x1, test_data_x2, leaks_test = create_test_data(tokenizer,test_sentence_pairs,  siamese_config['MAX_SEQUENCE_LENGTH'])

preds = list(model.predict([test_data_x1, test_data_x2, leaks_test], verbose=1))
scores = []
for pred in preds:
	scores.append(np.argmax(pred))

results = [(x, y, z) for (x, y), z in zip(test_sentence_pairs, scores)]
results.sort(key=itemgetter(2), reverse=True)
idx1,idx2 = 0,0
for i in range(len(data)):
	if summaries[i] == results[0][1]:
		idx1 = i
	elif summaries[i] == results[1][1]:
		idx2 = i
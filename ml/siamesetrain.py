from model import SiameseBiLSTM
from inputHandler import word_embed_meta_data, create_test_data
from config import siamese_config
import pandas as pd
from operator import itemgetter
from keras.models import load_model
from load import load_sts
import numpy as np


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

print('########################################',labels)

is_similar = []

for _,val in labels_dict.items():
	is_similar.append(val)



############ Data Preperation ##########

# df = pd.read_csv('sample_data.csv')

# sentences1 = list(df['sentences1'])
# sentences2 = list(df['sentences2'])
# is_similar = list(df['is_similar'])
# del df

######## Word Embedding ############

tokenizer, embedding_matrix = word_embed_meta_data(sentences1+sentences2,  siamese_config['EMBEDDING_DIM'])

embedding_meta_data = {
	'tokenizer': tokenizer,
	'embedding_matrix': embedding_matrix
}

## creating sentence pairs
sentences_pair = [(x1, x2) for x1, x2 in zip(sentences1, sentences2)]
print("####################",sentences_pair[0])
del sentences1
del sentences2

######## Training ########

class Configuration(object):
    """Dump stuff here"""

CONFIG = Configuration()

CONFIG.embedding_dim = siamese_config['EMBEDDING_DIM']
CONFIG.max_sequence_length = siamese_config['MAX_SEQUENCE_LENGTH']
CONFIG.number_lstm_units = siamese_config['NUMBER_LSTM']
CONFIG.rate_drop_lstm = siamese_config['RATE_DROP_LSTM']
CONFIG.number_dense_units = siamese_config['NUMBER_DENSE_UNITS']
CONFIG.activation_function = siamese_config['ACTIVATION_FUNCTION']
CONFIG.rate_drop_dense = siamese_config['RATE_DROP_DENSE']
# CONFIG.validation_split_ratio = siamese_config['VALIDATION_SPLIT']
CONFIG.validation_split_ratio = 0.05

siamese = SiameseBiLSTM(CONFIG.embedding_dim , CONFIG.max_sequence_length, CONFIG.number_lstm_units , CONFIG.number_dense_units, CONFIG.rate_drop_lstm, CONFIG.rate_drop_dense, CONFIG.activation_function, CONFIG.validation_split_ratio)

best_model_path = siamese.train_model(sentences_pair, is_similar, embedding_meta_data, model_save_directory='./')


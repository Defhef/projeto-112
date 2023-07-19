# Biblioteca de pré-processamento de dados de texto
import nltk
nltk.download('punkt')
nltk.download('wordnet')


from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

import json
import pickle

import numpy as np
import random

words=[] #lista de palavras-raiz únicas nos dados
classes = [] #lista de tags únicas nos dados
pattern_word_tags_list = [] #lista dos pares de (['palavras', 'da', 'frase'], 'tags')

ignore_words = ['?', '!',',','.', "'s", "'m"]

train_data_file = open('./static/assets/chatbot_corpus/intents.json').read()
intents = json.loads(train_data_file)

def get_stem_words(words, ignore_words):
    stem_words = []
    for word in words:
        if word not in ignore_words:
            w = stemmer.stem(word.lower())
            stem_words.append(w)
    return stem_words
 
def create_bot_corpus(words, classes, pattern_word_tags_list, ignore_words):

    for intent in intents['intents']:

        # Adicione todos os padrões e tags a uma lista
        for pattern in intent['patterns']:            
            pattern_word = nltk.word_tokenize(pattern)            
            words.extend(pattern_word)                        
            pattern_word_tags_list.append((pattern_word, intent['tag']))
              
    
        # Adicione todas as tags à lista classes
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
    stem_words = get_stem_words(words, ignore_words) 
    stem_words = sorted(list(set(stem_words)))
    classes = sorted(list(set(classes)))

    return stem_words, classes, pattern_word_tags_list


# Conjunto de Dados de Treinamento: 
# Texto de Entrada----> como Saco de Palavras (Bag Of Words) 
# Tags----------------> como Label

def bag_of_words_encoding(stem_words, pattern_word_tags_list):
    
    bag = []
    for word_tags in pattern_word_tags_list:
        # exemplo: word_tags = (['Ola', 'voce'], 'saudacao']

        pattern_words = word_tags[0] # ['Ola' , 'voce']
        stem_pattern_words = get_stem_words(pattern_words, ignore_words)
        bag_of_words = []

        # Codificando dados de entrada 
        for word in stem_words:            
            if word in stem_pattern_words:              
                bag_of_words.append(1)
            else:
                bag_of_words.append(0)
    
        bag.append(bag_of_words)
    
    return np.array(bag)

def class_label_encoding(classes, pattern_word_tags_list):
    
    labels = []

    for word_tags in pattern_word_tags_list:

        # Comece com uma lista de 0s
        labels_encoding = list([0]*len(classes))  

        # exemplo: word_tags = (['ola', 'voce'], 'saudacao']

        tag = word_tags[1]   # 'saudacao'

        tag_index = classes.index(tag)

        # Codificação de etiquetas
        labels_encoding[tag_index] = 1

        labels.append(labels_encoding)
        
    return np.array(labels)

def preprocess_train_data():
  
    stem_words, tag_classes, word_tags_list = create_bot_corpus(words, classes, pattern_word_tags_list, ignore_words)
    
    # Converta palavras-tronco e classes para o formato de arquivo Python pickle
    pickle.dump(stem_words, open('./static/assets/chatbot_corpus/words.pkl','wb'))
    pickle.dump(tag_classes, open('./static/assets/chatbot_corpus/classes.pkl','wb'))

    train_x = bag_of_words_encoding(stem_words, word_tags_list)
    train_y = class_label_encoding(tag_classes, word_tags_list)
    
    return train_x, train_y

# preprocess_train_data()



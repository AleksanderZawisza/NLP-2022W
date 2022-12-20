from abc import ABC, abstractmethod
from johnsnowlabs import nlu
from nlp_classifier import NLPClassifier
import numpy as np

class NLPTitleEmbedding(ABC):
    def __init__(self):
        self.model = None
        self.name = None
        self.max_words = None
        self.max_words_title = None
        self.embedding_size = None
    
    def get_title_lyrics_embedding(self, lyrics, title):
        pass

class BertTitle(NLPTitleEmbedding):
    def __init__(self, max_words, max_words_title):
        self.model = nlu.load('en.embed.bert')
        self.name = 'bertT'
        self.max_words = max_words
        self.max_words_title = max_words_title
        self.embedding_size = 768
    
    def get_title_lyrics_embedding(self, lyrics, title):
        title = self.__embed(title, self.max_words_title)
        lyrics = self.__embed(lyrics, self.max_words)
        return np.concatenate((title, lyrics), axis=1)

    def __embed(self, data, max_words):
        embeddings = self.model.predict(data, output_level='document')
        return np.array([self.__process_embedding(embedding, max_words) for embedding in embeddings.word_embedding_bert])
    
    def __process_embedding(self, embedding, max_words):
        embedding.resize((max_words, self.embedding_size), refcheck=False)
        return embedding.flatten()
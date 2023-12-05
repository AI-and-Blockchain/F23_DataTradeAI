import string
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import numpy as np
import pandas as pd

def preprocess(data):
    # Load English dictionary
    nlp = spacy.load('en_core_web_sm')
    
    # Define stopwords
    stop_words = [
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 
        'for', 'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 
        'on', 'or', 'such', 'that', 'the', 'their', 'then', 'there', 
        'these', 'they', 'this', 'to', 'was', 'will', 'with'
    ]
    
    # Clean text
    for text in range(len(data)):
        phrase = data['Phrase'].iloc[text]
        sus = data['Suspicious'].iloc[text]
        phrase = phrase.lower()
        sus = sus.lower()
        phrase_ = nlp(phrase)  #stripping unnecesary info
        phrase_words = [word.text for word in phrase_ ]
        phrase_words = list(filter(("").__ne__,[word.translate(str.maketrans('', '', string.punctuation)) for word in phrase_words]))
        sus_ = nlp(sus)
        sus_words = [word.text for word in sus_ ]
        sus_words = list(filter(("").__ne__,[word.translate(str.maketrans('', '', string.punctuation)) for word in sus_words]))
        data['Phrase'].iloc[text] = " ".join(phrase_words)
        data['Suspicious'].iloc[text] = " ".join(sus_words)
    
    # Split text into noun_chunks
    def chunk(phrase):
        chunks = [chunk.text for chunk in nlp(phrase).noun_chunks]
        return chunks

    # Vectorize data
    tfidf_vectorizer = TfidfVectorizer(tokenizer = chunk,norm = None)
    tfidf_vectorizer.fit(data["Phrase"] + " " + data["Suspicious"])
    sus=tfidf_vectorizer.transform(data["Suspicious"])
    act = tfidf_vectorizer.transform(data["Phrase"])
    print((act.toarray()))
    X = [np.matrix(sus.toarray()),np.matrix(act.toarray())]
    y = data["Class"]
    return X,y,tfidf_vectorizer.vocabulary_
        




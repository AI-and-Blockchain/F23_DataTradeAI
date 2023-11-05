import string
import pandas as pd
import numpy as np
import spacy
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

nlp = spacy.load('en_core_web_sm')
stop_words = [
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 
    'for', 'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 
    'on', 'or', 'such', 'that', 'the', 'their', 'then', 'there', 
    'these', 'they', 'this', 'to', 'was', 'will', 'with'
]
data = pd.read_csv("./Dataset/train_snli.csv",sep = "\t",header=0,names = ['Phrase','Suspicious','Class'])
#data provided by https://www.kaggle.com/code/mpwolke/plagiarism-mit-detection
data = data.dropna()[:4000]

words={}
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
    
#define chunks for vectorization
def chunk(phrase):
    chunks = [chunk.text for chunk in nlp(phrase).noun_chunks]
    return chunks

tfidf_vectorizer = TfidfVectorizer(tokenizer = chunk,norm = None)
X = tfidf_vectorizer.fit_transform(data["Phrase"] + " " + data["Suspicious"])
y = data["Class"]

model = LogisticRegression()
model.fit(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_rep)


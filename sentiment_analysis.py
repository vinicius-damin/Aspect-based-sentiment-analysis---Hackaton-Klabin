#!/usr/bin/env python
# coding: utf-8

# In[10]:


#importar as bibliotecas necessárias
import nltk
import pickle
from nltk.tokenize import word_tokenize
from statistics import mode
from nltk.classify import ClassifierI

#primeiro temos que fazer pickle.load em todos os arquivos necessários
words_features_f=open('words_features.pickle','rb')
words_features=pickle.load(words_features_f)
words_features_f.close()

classifiers_str=['NaiveBayes_classifier',
                 'MNB_classifier',
                 'BernoulliNB_classifier',
                 'SGDClassifier_classifier',
                  #retirei 'SVC_classifier',
                 'LinearSVC_classifier',
                 'NuSVC_classifier']
classifiers_list=[]
for classifier in classifiers_str:
    classifier_f=open(classifier+'.pickle','rb')
    classifiers_list.append((pickle.load(classifier_f),classifier))

NaiveBayes_classifier=classifiers_list[0][0]
MNB_classifier=classifiers_list[1][0]
BernoulliNB_classifier=classifiers_list[2][0]
SGDClassifier_classifier=classifiers_list[3][0]
#SVC_classifier=classifiers_list[4][0] da erro
LinearSVC_classifier=classifiers_list[4][0]
#NuSVC_classifier=classifiers_list[5][0]




#Como não é possível fazer pickle.dump na instância de VoteClassifier:
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        #guarda os 8 classificadores
        self.classifiers=classifiers
          
    def classify(self, features):
        votes=[]
        for c in self.classifiers:
            v=c.classify(features)
            #cada classificador vota uma vez
            votes.append(v)
        #o sentimento que é selecionado é o que aparece mais vezes (mais votado)
        return mode(votes)
    def confidence(self,features):
        votes=[]
        for c in self.classifiers:
            v=c.classify(features)
            votes.append(v)
        choice_votes=votes.count(mode(votes))
        conf=choice_votes/len(votes)
        #temos também o valor de confiança de nossa predição
        return conf
voted_classifier=VoteClassifier(NaiveBayes_classifier,
                                MNB_classifier,
                                BernoulliNB_classifier,
                                SGDClassifier_classifier,
                                #retirei 'SVC_classifier',
                                LinearSVC_classifier,
                                LinearSVC_classifier,
                                #NuSVC_classifier
                                )





#Como não é possível fazer pickle.dump na instância de VoteClassifier:
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        #guarda os 8 classificadores
        self.classifiers=classifiers
          
    def classify(self, features):
        votes=[]
        for c in self.classifiers:
            v=c.classify(features)
            #cada classificador vota uma vez
            votes.append(v)
        #o sentimento que é selecionado é o que aparece mais vezes (mais votado)
        return mode(votes)
    def confidence(self,features):
        votes=[]
        for c in self.classifiers:
            v=c.classify(features)
            votes.append(v)
        choice_votes=votes.count(mode(votes))
        conf=choice_votes/len(votes)
        #temos também o valor de confiança de nossa predição
        return conf
voted_classifier=VoteClassifier(NaiveBayes_classifier,
                                MNB_classifier,
                                BernoulliNB_classifier,
                                SGDClassifier_classifier,
                                #retirei 'SVC_classifier',
                                LinearSVC_classifier,
                                #NuSVC_classifier,NuSVC_classifier
                                )


#Definimos a função criada no documento 'Creating the algorithm'
def find_features(document):
    
#temos que usar word_tokenize pois recebemos uma review em formato de string contento várias palavras.
    words=word_tokenize(document)
    features={}
    #cada palavra das 7000 mais frequentes é avaliada se está ou não
    #na review em questão, se estiver ela é marcada como True
    for w in words_features:
        features[w]=(w in words)
    return features

#importar um tradutor
from googletrans import Translator
translator = Translator()

def sentiment(text):

    feats=find_features(text)
    
    return (voted_classifier.classify(feats),voted_classifier.confidence(feats))


#função que recebe uma string e retorna o sentimento dela
def sentiment_pt(texto):
    text=translator.translate(texto,src='pt', dest='en').text
    return sentiment(text)


# In[ ]:
#print(sentiment_pt('amava o café'))
# %%

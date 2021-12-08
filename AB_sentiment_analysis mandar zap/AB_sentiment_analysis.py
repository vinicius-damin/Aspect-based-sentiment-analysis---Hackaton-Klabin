#!/usr/bin/env python
# coding: utf-8

# In[8]:


import spacy
from googletrans import Translator

translator = Translator()
#é preciso fazer python -m spacy download en_core_web_sm antes da proxima linha
nlp=spacy.load("en_core_web_sm")


# Com base em Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
#Criamos duas listas com palavras positivas e negativas
pos_txt=open('positive-words.txt').read()
pos=pos_txt[1282:].split("\n")

neg_txt=open('negative-words.txt').read()
neg=neg_txt[1285:].split("\n")


#recebe um texto e retorna um dicionário com os substantivos e o sentimento deles

def feature_sentiment(Frase):
#essa funcao foi retirada da internet
    text=translator.translate(Frase,src='pt', dest='en').text

    sent_dict = dict()
    sentence = nlp(text)
    opinion_words = neg + pos
    debug = 0
    for token in sentence:
        # check if the word is an opinion word, then assign sentiment
        if token.text in opinion_words:
            sentiment = 1 if token.text in pos else -1
            # if target is an adverb modifier (i.e. pretty, highly, etc.)
            # but happens to be an opinion word, ignore and pass
            if (token.dep_ == "advmod"):
                continue
            elif (token.dep_ == "amod"):
                sent_dict[token.head.text] = sentiment
            # for opinion words that are adjectives, adverbs, verbs...
            else:
                for child in token.children:
                    # if there's a adj modifier (i.e. very, pretty, etc.) add more weight to sentiment
                    # This could be better updated for modifiers that either positively or negatively emphasize
                    if ((child.dep_ == "amod") or (child.dep_ == "advmod")) and (child.text in opinion_words):
                        sentiment *= 1.5
                    # check for negation words and flip the sign of sentiment
                    if child.dep_ == "neg":
                        sentiment *= -1
                for child in token.children:
                    # if verb, check if there's a direct object
                    if (token.pos_ == "VERB") & (child.dep_ == "dobj"):                        
                        sent_dict[child.text] = sentiment
                        # check for conjugates (a AND b), then add both to dictionary
                        subchildren = []
                        conj = 0
                        for subchild in child.children:
                            if subchild.text == "and":
                                conj=1
                            if (conj == 1) and (subchild.text != "and"):
                                subchildren.append(subchild.text)
                                conj = 0
                        for subchild in subchildren:
                            sent_dict[subchild] = sentiment

                # check for negation
                for child in token.head.children:
                    noun = ""
                    if ((child.dep_ == "amod") or (child.dep_ == "advmod")) and (child.text in opinion_words):
                        sentiment *= 1.5
                    # check for negation words and flip the sign of sentiment
                    if (child.dep_ == "neg"): 
                        sentiment *= -1
                
                # check for nouns
                for child in token.head.children:
                    noun = ""
                    if (child.pos_ == "NOUN") and (child.text not in sent_dict):
                        noun = child.text
                        # Check for compound nouns
                        for subchild in child.children:
                            if subchild.dep_ == "compound":
                                noun = subchild.text + " " + noun
                        sent_dict[noun] = sentiment
                    debug += 1
                    
    #os aspects e os sentiments estão salvos em sent_dict, porém quero traduzir as keys do meu dicionário.
    #crio um novo dicionário com as keys traduzidas:
    #print(sent_dict)
    
    dic_sentimentos={}
    for key in sent_dict:
        chave=translator.translate(key,src='en', dest='pt').text
        dic_sentimentos[chave]=sent_dict[key]
    return dic_sentimentos


# In[9]:


#print(feature_sentiment("Gostei do meu chefe mas odiei meu sálario"))


# In[ ]:





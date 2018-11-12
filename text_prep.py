# coding: utf-8

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

from pymystem3 import Mystem
from string import punctuation

import re

def preprocess_text(text,method='stem',stop=True,lang='russian'):
    """function for text preprocessing for RUS/ENG languages"""
    stopwords_list = stopwords.words(lang) if stop else []
    if lang=='english' and stop: stopwords_list.append("n't")
    unicode_dict = {'«':'"','»':'"','—':'-','’':"'"}
    for symbol in unicode_dict:
        text = text.replace(symbol,unicode_dict[symbol])
    
    if method == 'lemmatize':
        if lang == 'russian':
            lemm = Mystem()
            tokens = lemm.lemmatize(text.lower())
            tokens = [token for token in tokens if token not in stopwords_list and token != ' ' and token.strip() not in punctuation and len(token)>2]
        else:
            lemm = WordNetLemmatizer()
            tokens = word_tokenize(text.lower()) # list(text.lower().split()) # english workaround with len
            tokens = [lemm.lemmatize(token) for token in tokens if token not in stopwords_list and token != ' ' and token.strip() not in punctuation and len(token)>2]
    elif method == 'stem':
        stemmer = SnowballStemmer(lang)
        tokens = word_tokenize(text.lower()) # list(text.lower().split()) #english workaround with len
        tokens = [stemmer.stem(token) for token in tokens if token not in stopwords_list and token not in punctuation and len(token)>2]
        
    text = ' '.join(tokens)
    #for symbol in punctuation:
        #text = text.replace(symbol,'')
    for symbol in punctuation:
        text = text.replace(symbol,'')
    text = re.sub(r'\d+','',text)
    return re.sub(' +', ' ',text)

# Examples
txt = """Министр просвещения России Ольга Васильева пообещала, что основанную Владимиром Лениным в 1921 году подмосковную школу «Горки» откроют после ремонта к столетию учреждения. 
На встрече с родителями учеников школы она заверила, что на территории школы не будет построено никаких посторонних зданий.
«На сегодняшний день по моему приказу была подготовлена регистрация земли с обременением — это значит, что на этом участке не может быть ничего, кроме зданий, которые направлены на образовательный процесс <...> Для того, чтобы никто не смог у нас землю отнять, "отжать", выкупить, передать»,— цитирует госпожу Васильеву пресс-служба Минпросвещения. 
Глава ведомства предложила родителям создать инициативную группу, с которой можно проводить регулярные встречи.
Ранее Минпросвещения, которое выступает учредителем школы, объявило о ее закрытии. Чиновники пообещали обновить здание и инфраструктуру, однако родители учащихся выступают против. 
Они считают, что здание планируют снести, а территорию, которая граничит с музеем-заповедником «Горки Ленинские», застроить."""

eng_txt = """Bitcoin (BTC-USD) has been remarkably stable in recent months. In fact, for over two months now Bitcoin has traded in an incredibly narrow range of around $6,000 - $6,800. There doesn’t appear to be much news worthy of moving prices right now. So, Bitcoin remains extremely calm, for now."""

print(preprocess_text(txt,'stem'))
print(preprocess_text(eng_txt,'stem',True,'english'))

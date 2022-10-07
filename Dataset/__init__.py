import os
import sys

import pandas as pd
import re
import emoji
from sklearn.utils import resample
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk
#nltk.download('stopwords')
stop_words = stopwords.words('english')



class Preprocessing:
    def __init__(self,path=os.path.join(sys.path[0], "Dataset\\dataset v.1.2"),preprocess = True):
        print('Reading data...')
        self.path = path
        self.reviews_df = pd.read_csv(path + "\\reviews_df.csv")
        self.users_df = pd.read_csv(path + "\\users.csv")
        self.wines_df = pd.read_csv(path + "\\wine_df.csv")
        self.full_df = pd.read_csv(path + "\\full_dataset.csv")
        #self.full_df = self.full_df.merge(self.users_df, on='User', how='left')

        if preprocess:
            print('Cleaning data...')
            self.full_df['Cleaned'] = self.full_df['Note'].apply(lambda f: self.clean(f))
            print('Tokenizing data...')
            self.full_df['Tokenized'] = self.full_df['Cleaned'].apply(lambda f: self.tokenize(f))
            print('Creating labels...')
            self.full_df['Sentiment'] = self.full_df['User Rating'].apply(lambda f: self.create_label(f))
            print("Balancing data, downsampling.. ")
            self.full_df = self.balance_df(self.full_df)





    def clean(self, text):
        text = str(text)
        no_html = BeautifulSoup(text).get_text()
        clean = re.sub("[^a-z\s]+", " ", no_html, flags=re.IGNORECASE)
        return re.sub("(\s+)", " ", clean).lower()

    def tokenize(self, text):
        #clean = self.clean(text).lower()
        stopwords_en = stopwords.words("english")
        return [w for w in re.split("\W+", text) if not w in stopwords_en]

    def extract_emojis(self, text):
        return ','.join(c for c in text if c in emoji.EMOJI_DATA)


    def extract_hash_tags(self, text):
        return ','.join(part[1:] for part in text.split() if part.startswith('#'))

    def create_label(self,rating):
        if rating > 4:
            return 1
        elif rating < 4:
            return -1
        return 0

    def get_dataset(self):
        return self.reviews_df,self.wines_df,self.users_df,self.full_df

    def pick_only_key_sentence(self, text, word):
        result = re.findall(r'([^.]*' + word + '[^.]*)', str(text).lower())
        return result


    def balance_df(self,df):
        neg = df[df.Sentiment == -1]
        neu = df[df.Sentiment == 0]
        pos = df[df.Sentiment == 1]
        pos_downsampled = resample(pos,
                                   replace=False,
                                   n_samples=len(neg))
        neu_downsampled = resample(neu,
                                   replace=False,
                                   n_samples=len(neg))

        return pd.concat([neu_downsampled, neg, pos_downsampled])

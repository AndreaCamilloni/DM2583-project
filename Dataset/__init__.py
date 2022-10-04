import os
import sys

import pandas as pd
import re
import emoji
import string
import contractions
from nltk.corpus import stopwords
import nltk
#nltk.download('stopwords')
stop_words = stopwords.words('english')

def extract_emojis(text):
    return ','.join(c for c in text if c in emoji.EMOJI_DATA)


def extract_hash_tags(s):
    return ','.join(part[1:] for part in s.split() if part.startswith('#'))


def preprocessing(s):
    result = str(s).lower()
    # remove html tags
    _CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    result = re.sub(_CLEANR, '', result)
    # remove newline
    result = re.sub(r'\\t|\\n|\\r", "\t|\n|\r', '', result)
    # remove http link
    result = re.sub(r'http\S+', '', result)
    # remove mention
    result = re.sub(r'@\S+', '', result)
    # remove hashtags
    result = re.sub(r'#\S+', '', result)
    # remove "rt" retweet
    result = re.sub(r'rt', '', result)
    # remove emojis
    _CLEANR = re.compile(pattern="["
                                 u"\U0001F600-\U0001F64F"  # emoticons
                                 u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                 u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                 u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                 "]+", flags=re.UNICODE)
    result = re.sub(_CLEANR, '', result)
    # remove contractions
    result = contractions.fix(result)
    # remove punctuation
    result = result.translate(str.maketrans(' ', ' ', string.punctuation))

    # remove number
    result = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", result)
    return result


def tokenizer(text):
    stopwords_en = stopwords.words("english")
    return [str(w) for w in re.split("\W+", str(text)) if not w in stopwords_en]

def get_dataset(path=os.path.join(sys.path[0], "Dataset\\dataset v.1.2")):
    reviews_df = pd.read_csv(path+"\\reviews_df.csv")
    users_df = pd.read_csv(path + "\\users.csv")
    wines_df = pd.read_csv(path + "\\wine_df.csv")
    full_df = pd.read_csv(path + "\\full_dataset.csv")
    return reviews_df,wines_df,users_df,full_df

def create_label(rating):
    if rating > 4:
        return 1
    elif rating < 4:
        return -1
    return 0
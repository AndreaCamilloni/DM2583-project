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
    result = s.lower()
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
    return [w for w in re.split("\W+", text) if not w in stopwords_en]


class Tweets_dataset:
    def __init__(self, labels=[0,1],path = None, scraper=None, preprocess=True, tokenize=True):
        self.path = path
        self.labels = labels
        self.df = pd.DataFrame()
        self.scraper = scraper

        if self.path != None:
            self.df = pd.read_csv(path)
        if self.scraper !=None:
            print()
            #self.df = self.scraper.get_tweets()

        if preprocess:
            self.df['Text_preprocessed']=self.df['Text'].apply(lambda f: preprocessing(f))
        if tokenize:
            self.df['Text_preprocessed'] = self.df['Text_preprocessed'].apply(lambda f: tokenizer(f))

    def get(self):
        return self.df



    def tweets_scraper(self):
        return

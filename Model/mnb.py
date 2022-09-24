import math
import numpy as np
from collections import Counter, defaultdict

class MultinomialNaiveBayes:

    def __init__(self, classes):
        self.classes = classes

    # group data by class (0,1)
    def group_by_class(self, X, y):
        data = dict()
        for c in self.classes:
            data[c] = X[np.where(y == c)]
        return data

    def fit(self, X, y):
        self.n_class_items = {}
        self.log_class_priors = {}
        self.word_counts = {}
        self.vocab = set()

        n = len(X)

        grouped_data = self.group_by_class(X, y)  # group

        for c, data in grouped_data.items():
            self.n_class_items[c] = len(data)  # lenght of the data for each class
            self.log_class_priors[c] = math.log(self.n_class_items[c] / n)  # log prior probability
            self.word_counts[c] = defaultdict(lambda: 0)  # init

            for text in data:
                counts = Counter(text)  # counts the occurrences of words
                # print(counts)
                # return 0
                for word, count in counts.items():
                    if word not in self.vocab:
                        self.vocab.add(word)
                        # print(self.vocab)

                    self.word_counts[c][word] += count
                # print(self.word_counts)

        return self

    def laplace_smoothing(self, word, text_class):
        num = self.word_counts[text_class][word] + 1
        denom = self.n_class_items[text_class] + len(self.vocab)
        return math.log(num / denom)

    def predict(self, X):
        result = []
        for text in X:

            class_scores = {c: self.log_class_priors[c] for c in self.classes}

            words = set(text)
            for word in words:
                if word not in self.vocab: continue

                for c in self.classes:
                    log_w_given_c = self.laplace_smoothing(word, c)  # log(w|c)
                    class_scores[c] += log_w_given_c

            result.append(max(class_scores, key=class_scores.get))

        return result
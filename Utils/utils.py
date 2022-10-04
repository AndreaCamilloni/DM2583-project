#wordcloud plot
#confusion matrix
#metrics ...
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from wordcloud import WordCloud
from nltk.corpus import stopwords

def class_report(y_test, y_hat):
    print(classification_report(y_test, y_hat))

#%% Confusion matrix
def cnf_matrix(y_test, y_hat,class_names = ["negative", "neutral", "positive"]):
    cnfm = confusion_matrix(y_test, y_hat)
    fig,ax = plt.subplots()
    sns.heatmap(pd.DataFrame(cnfm), annot=True, cmap="Blues", fmt="d", cbar=False, xticklabels=class_names, yticklabels=class_names)
    ax.xaxis.set_label_position('top')
    plt.tight_layout()
    plt.ylabel('True sentiments')
    plt.xlabel('Predicted sentiments')



def plot_sentiment_pred(y_hat,y_test):
    sentiments = pd.DataFrame({'Predicted': y_hat, 'Real': y_test})

    pred = sentiments.groupby(by="Predicted").count()
    true = sentiments.groupby(by="Real").count()

    sentiments_distr = true.join(pred)
    sentiments_distr.index.names = ['Sentiment']

    sentiments_distr.plot(kind='bar', )

def plot_wordcloud(df_Column):
    text = " ".join(t for t in df_Column.apply(lambda f: str(f)))

    wordcloud = WordCloud(background_color="white", max_words=300, contour_width=3,
                          contour_color='steelblue', width=700, height=500, scale=1,
                          max_font_size=500, collocations=False, stopwords=stopwords.words("english"))
    # Generate a word cloud
    wordcloud.generate(text)
    # plot the WordCloud image
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)

    plt.show()

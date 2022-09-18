# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Dataset.tweets_dataset import Tweets_dataset



# Press the green button in the gutter to run the script.
from WebScraping.twitter import TwitterScraper

if __name__ == '__main__':

    df=Tweets_dataset(path="/Users/andre/PycharmProjects/DM2583-project/Dataset/tweet_df_1.csv")
     #print(df.get())
    print(TwitterScraper().download())




# See PyCharm help at https://www.jetbrains.com/help/pycharm/

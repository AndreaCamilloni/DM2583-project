# Run only if you want to scrape new data.
# Consider that the scraper takes about 5 minutes to scrape each page
# You can find al the craped data in the dataset folder.
import pandas as pd
import time

from WebScraping.vivino_scraper import vivino_scraper

p = 1 # page number
wine_df = pd.DataFrame()
reviews_df = pd.DataFrame()
while p<2:
    reviews, wines  = vivino_scraper(p)
    p += 1
    time.sleep(2)
    print("page: ", p)
    if len(wines) != 0:
      wine_df = pd.concat([wine_df,wines])
      reviews_df = pd.concat([reviews_df,reviews])

wine_df.reset_index()
reviews_df.reset_index()

users_reviews_count = reviews_df.pivot_table(columns=['User'], aggfunc='size')
users_reviews_count = users_reviews_count.sort_values(ascending=False)
print(users_reviews_count.index)
# Run only if you want to scrape new data.
# Consider that the scraper takes about 5 minutes to scrape each page
# You can find al the craped data in the dataset folder.
import os
import sys

import pandas as pd
import time

from WebScraping.vivino_scraper import vivino_scraper, scrape_users

PAGES_TO_SCRAPE = 1

p = 1 # page number
wine_df = pd.DataFrame()
reviews_df = pd.DataFrame()
while p<=PAGES_TO_SCRAPE:
    reviews, wines  = vivino_scraper(p)
    p += 1
    time.sleep(2)
    if len(wines) != 0:
      wine_df = pd.concat([wine_df,wines])
      reviews_df = pd.concat([reviews_df,reviews])

wine_df.reset_index()
reviews_df.reset_index()
full_df = pd.merge(reviews_df,wine_df,on=["Year", "Wine ID", "Wine"])


users_reviews_count = reviews_df.pivot_table(columns=['User'], aggfunc='size')
users_reviews_count = users_reviews_count.sort_values(ascending=False)

users_df = scrape_users(users_reviews_count)

print(users_df)
print(wine_df)
print(reviews_df)
print(full_df)

# Save dataframes to files
print("Saving dataframes into Dataset\\dataset v.1.2")
wine_df.to_csv(os.path.join(sys.path[0], "Dataset\\dataset v.1.2") + "\\wine_df.csv", index=False)
reviews_df.to_csv(os.path.join(sys.path[0], "Dataset\\dataset v.1.2") + "\\reviews_df.csv", index=False)
full_df.to_csv(os.path.join(sys.path[0], "Dataset\\dataset v.1.2") + "\\full_dataset.csv", index=False)
users_df.to_csv(os.path.join(sys.path[0], "Dataset\\dataset v.1.2") + "\\users.csv", index=False)
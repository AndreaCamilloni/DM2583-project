# DM2583-project
## Data scraping
- Data were collected from vivino.com using scraping_script.py
- Scraping data requires lot of time, this is why the collected data were provided.
- The scraping script must be set up to filter the data you want. (e.g. params, number of pages you want)

- Also a script to scrape data from social media was provided, under WebScraping/twitter.py. This script was implemented in the first version of the project, but is now deprecated. It was kept for future implementation.
- Already built Twitter dataset can be found under Dataset/tweet_df_1.csv 

## Setup
- Clone this repo on your local machine
- Download the datasets from this link: https://drive.google.com/file/d/1__xL7EL7_UKqT2ZLAlOjGS1osC_X0C0F/view?usp=sharing
- Extract the datasets into Dataset/dataset v.1.2
- Run notebook.ipynb


## Dataset v.1.2
- 4 different datasets: Wines, Reviews, Users and Full datasets.
- Wines: wines features (Price, average rating, name, year, number of reviews, country ...)
- Reviews: users' reviews and ratings about a wine
- Users: username, country and bio of the user
- Full dataset: wines and reviews joined together.
- Full dataset is about 1600000 entries.


import requests
import time
import pandas as pd

baseurl = "https://www.vivino.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
k = requests.get(baseurl)


def get_wine_data(wine_id, year, page, headers):
    api_url = "https://www.vivino.com/api/wines/{id}/reviews?per_page=50&year={year}&page={page}"  # <-- increased the number of reviews to 9999

    data = requests.get(
        api_url.format(id=wine_id, year=year, page=page), headers=headers
    ).json()

    return data


def wine_scraper(num_pages, headers, url):
    r = requests.get(
        url,
        params={
            # "country_code": "US",
            # "country_codes[]":"pt",
            "currency_code": "EUR",
            # "grape_filter":"varietal",
            "min_rating": "1",
            "order_by": "price",
            "order": "asc",
            "page": num_pages,
            # "price_range_max":"500",
            "price_range_min": "0",
            # "wine_type_ids[]":"1"
        },
        headers=headers
    )

    results = [
        (
            t["vintage"]["wine"]["winery"]["name"],
            t["vintage"]["year"],
            t["vintage"]["wine"]["id"],
            f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
            t["vintage"]["statistics"]["ratings_average"],
            t["vintage"]["statistics"]["ratings_count"],
        )
        for t in r.json()["explore_vintage"]["matches"]
    ]
    wine_df = pd.DataFrame(
        results,
        columns=["Winery", "Year", "Wine ID", "Wine", "Rating", "num_review"],
    )

    return wine_df


class VivinoScraper:

    def __init__(self, headers={
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }, url="https://www.vivino.com/api/explore/explore"):
        self.url = url
        self.headers = headers
        self.num_pages = 1
        self.current_page = 1
        self.wine_df = wine_scraper(self.num_pages, self.headers, self.url)
        self.wine_review_df = pd.DataFrame()

    def wine_review_scraper(self, dataframe=None):
        if dataframe is None:
            dataframe = self.wine_df
        ratings = []
        for _, row in dataframe.iterrows():
            page = 1
            while True:
                # print(
                #    f'Getting info about wine {row["Wine ID"]}-{row["Year"]} Page {page}'
                # )

                d = get_wine_data(row["Wine ID"], row["Year"], page, self.headers)

                if not d["reviews"]:
                    break

                for r in d["reviews"]:
                    ratings.append(
                        [
                            row["Year"],
                            row["Wine ID"],
                            r["rating"],
                            r["note"],
                            r["created_at"],
                        ]
                    )

                page += 1

        ratings = pd.DataFrame(
            ratings, columns=["Year", "Wine ID", "User Rating", "Note", "CreatedAt"]
        )  ##add columns

        df_out = ratings.merge(dataframe)

        return df_out

    def get_wine_df(self,scrape = False,num_page = 1):
        if scrape and num_page>self.current_page:
            for p in range(num_page-self.current_page):
                self.wine_df = pd.concat([self.wine_df,wine_scraper(self.current_page + p,self.headers,self.url) ],ignore_index=True)
                self.current_page += 1
            #self.wine_df.reset_index(drop=True)
            print("Current page: ", self.current_page)
        return self.wine_df


"""
p = 1
wine_df = pd.DataFrame()
while True:
    wine_df_page_p = vivino_scraper(p)
    p += 1
    time.sleep(2)

    if len(wine_df_page_p) == 0:
        break
    wine_df = pd.concat([wine_df, wine_df_page_p])
path = f'/content/drive/My Drive/Tmp/wine_review_vivino.csv'

with open(path, 'w', encoding='utf-8-sig') as f:
    wine_df.to_csv(path, index=False) """

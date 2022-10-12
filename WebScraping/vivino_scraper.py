import requests
import pandas as pd
import time
import numpy as np




def get_user_data(username):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    api_url = "https://www.vivino.com/api/users/{username}"

    data = requests.get(
        api_url.format(username=username), headers=headers
    ).json()

    return data

def scrape_users(users_reviews_count):
    print("Scraping users...")
    user_data = []
    tmp = 0
    for u in users_reviews_count.index:
        user_json = get_user_data(u)
        user_data.append([
            user_json['user']['seo_name'],
            user_json['user']['bio'],
            user_json['user']['address']['country']['seo_name']
        ])
        if tmp == 500:
            time.sleep(5)
            tmp = 0

        tmp += 1

    users = pd.DataFrame(user_data, columns=["User", "Bio", "Country"])
    return users


def get_wine_data(wine_id, year, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    api_url = "https://www.vivino.com/api/wines/{id}/reviews?per_page=50&year={year}&page={page}"

    data = requests.get(
        api_url.format(id=wine_id, year=year, page=page), headers=headers
    ).json()

    return data


def vivino_scraper(p):
    print("Scraping page {}".format(p))
    r = requests.get(
        "https://www.vivino.com/api/explore/explore",
        params={
            # "country_code": "US",
            # "country_codes[]":"pt",
            "currency_code": "EUR",
            # "grape_filter":"varietal",
            "min_rating": "1",
            "order_by": "price",
            "order": "asc",
            "page": p,
            # "price_range_max":"500",
            "price_range_min": "0",
            # "wine_type_ids[]":"1"
        },
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
        }
    )

    results = []

    try:
        results = [
            (
                t["vintage"]["wine"]["winery"]["name"],
                t["vintage"]["year"],
                t["vintage"]["wine"]["id"],
                f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"] if t["vintage"]["year"] != None else " "}',
                t["vintage"]["statistics"]["ratings_average"],
                t["vintage"]["statistics"]["ratings_count"]
                # t['vintage']['wine']['country']['name']

            )
            for t in r.json()["explore_vintage"]["matches"]
        ]
    except:
        print("An exception occurred")
    dataframe = pd.DataFrame(
        results,
        columns=["Winery", "Year", "Wine ID", "Wine", "Rating", "num_review"],
    )

    ratings = []
    for _, row in dataframe.iterrows():
        page = 1
        while True:

            d = get_wine_data(row["Wine ID"], row["Year"], page)
            # print(d)
            if not d["reviews"]:
                break

            for r in d["reviews"]:

                if r["language"] != "en":  # <-- get only english reviews
                    continue

                ratings.append(
                    [
                        row["Wine"],
                        row["Year"],
                        row["Wine ID"],
                        r["rating"],
                        r["note"],
                        r["created_at"],
                        r["user"]["seo_name"],
                    ]

                )

            page += 1

    ratings = pd.DataFrame(
        ratings, columns=["Wine", "Year", "Wine ID", "User Rating", "Note", "CreatedAt", "User"]
    )

    return ratings, dataframe

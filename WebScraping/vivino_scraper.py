import requests
import pandas as pd
import time
import numpy as np




def get_user_data(username):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    api_url = "https://www.vivino.com/api/users/{username}"  # <-- increased the number of reviews to 9999

    data = requests.get(
        api_url.format(username=username), headers=headers
    ).json()

    return data


def get_wine_data(wine_id, year, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    api_url = "https://www.vivino.com/api/wines/{id}/reviews?per_page=50&year={year}&page={page}"  # <-- increased the number of reviews to 9999

    data = requests.get(
        api_url.format(id=wine_id, year=year, page=page), headers=headers
    ).json()

    return data


def vivino_scraper(p):
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
            # print(
            #    f'Getting info about wine {row["Wine ID"]}-{row["Year"]} Page {page}'
            # )

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

import pandas as pd
import sys
import json
import requests


def main():

    orders_df = pd.read_csv(sys.argv[1])
    coins_invested = orders_df["product"].unique()

    print("Average buy prices:")

    # finish up following:
    # total invested
    # total fee payed
    # total profit/loss
    # but also show this for each coin
    # coin: invested
    # coin : fee payed
    # coin: total profit/loss

    for coin in coins_invested:
        relevant_records_df = orders_df[orders_df["product"] == coin]
        total_size = relevant_records_df["size"].sum()
        relevant_records_df = relevant_records_df.reset_index()
        total_invested = 0
        average_buy_price = 0
        total_fee = 0
        for index, row in relevant_records_df.iterrows():
            total_invested = total_invested + row["size"] * row["price"]
            total_fee = total_fee + row["fee"]
            transaction_weighted_price = row["size"] / total_size * row["price"] + row["fee"]
            average_buy_price = average_buy_price + transaction_weighted_price
        print("\t{}: {}".format(coin, average_buy_price))

    url = "https://api.coinbase.com/v2/prices/ETH-EUR/spot"
    data = requests.get(url)
    data = data.json()
    print(data["data"]["amount"])
    # print("price of {} is {}".format(data["symbol"], data["price"]))


if __name__ == "__main__":
    main()

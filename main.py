from config import logo
from bmw import url_constructor
import pandas as pd

df = pd.read_csv('input_search.csv', na_values='_')
df = df.astype(object)
df.fillna('', inplace=True)
search = df.values


def main():
    for car in search:
        url_constructor(model=car[0], motor=car[1], price=car[2], kms=car[3], email=car[4])


if __name__ == "__main__":
    logo.print_bmw_ascii_with_small_by()
    main()



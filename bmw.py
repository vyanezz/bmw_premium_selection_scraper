import requests
from bs4 import BeautifulSoup
import json
from email_alert.mail_data import prepareMail
from email.mime.text import MIMEText
import pandas as pd
import os

path = os.path.abspath('data.csv')
UrlID = {}
newCar = []
news = False
priceChanges = {}


def add_ids(new_value):
    df_new = pd.DataFrame([new_value])
    try:
        df_existing = pd.read_csv(path)
    except FileNotFoundError:
        df_existing = pd.DataFrame()

    df_concatenated = pd.concat([df_existing, df_new], ignore_index=True)

    df_concatenated.to_csv(path, index=False)

def checkPriceChanges(id, priceCar, url, email=None):
    df = pd.read_csv('data.csv')

    row1 = df[df['id'] == id]

    csvPrice = row1.iloc[0]['priceCar']

    idx = df.index[df['id'] == id]

    if priceCar != csvPrice:
        priceChanges[url] = {"previousPrice": csvPrice, "priceCar": priceCar}
        df.loc[idx, 'priceCar'] = priceCar
        df.to_csv('data.csv', index=False)
        print(f"New Price changes for {url}")
        if email:
            changesNot(priceChanges)

def scrapeAlert(url, email=None):
    global news

    print("Requested URL --> ", url)

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    script_tag = soup.find('script', {'type': 'application/ld+json'})

    if script_tag:
        script_content = script_tag.string

        try:
            json_data = json.loads(script_content)

            if 'itemListElement' in json_data:

                itemListElement = json_data['itemListElement']

                for item in itemListElement:
                    url = item.get('url', '')
                    id = url[-9:-1]
                    id = int(id)

                    priceCar = scrapePrices(url)
                    UrlID[id] = {"url": url, "priceCar": priceCar}

                    df_read = pd.read_csv(path)
                    noNews = df_read['id'].isin([id]).any()

                    if not noNews:
                        news = True
                        new_value = {"id": id, "url": url, "priceCar": priceCar}
                        add_ids(new_value)
                        newCar.append(url)
                        print(f'New item found: {id} // {url}// {priceCar}')

                    else:
                        checkPriceChanges(id, priceCar, url, email)



        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')

    if news and email:
        body = "News:\n\n"
        for url in newCar:
            body += f"- {url}\n\n"
        message = MIMEText(body, 'plain')
        message['Subject'] = "🚗New vehicles avalilable🚗"
        prepareMail(message)
        newCar.clear()
        news = False
        return news

def changesNot(priceChanges):
    body = "New price changes:\n\n"
    for url in priceChanges:
        body += f"- {url}\n\n Previous Price: {priceChanges[url]['previousPrice']}€ New Price: {priceChanges[url]['priceCar']}€\n\n"
    message = MIMEText(body, 'plain')
    message['Subject'] = "💲New price changes💲"
    prepareMail(message)
    priceChanges.clear()
    return news

def scrapePrices(url):
    responseURL = requests.get(url)
    soup = BeautifulSoup(responseURL.text, 'html.parser')

    priceCar = soup.find('div', class_='datePrice')
    pricestr = priceCar.find('span').text
    price_str = pricestr[:-2].replace(",", "")

    priceCar = float(price_str)

    return priceCar

def url_constructor(model, motor, price=None, kms=None, email=None):
    spainUrl = "https://www.bmwpremiumselection.es"

    if price or kms:

        params = []

        if price:
            priceParam = f"condicion%5Bprecio_hasta%5D={price}"
            params.append(priceParam)

        if kms:
            kmsParam = f"&condicion%5Bkm_hasta%5D={kms}"
            params.append(kmsParam)

        filters = [model, motor]

        captured_filters = []

        for filter in filters:
            if filter != None:
                filter = "/" + filter
                captured_filters.append(filter)

        for cap in captured_filters:
            spainUrl += cap

        firstIteration = True

        for param in params:
            if firstIteration:
                firstIteration = False
                spainUrl += "/?" + param
            else:
                spainUrl += "&" + param

        return scrapeAlert(spainUrl, email)

    else:
        filters = [model, motor]

        noErrors = True

        for f in filters:
            if len(f) <= 0:
                noErrors = False

        if noErrors:
            captured_filters = []

            for filter in filters:
                if filter != None:
                    filter = "/" + filter
                    captured_filters.append(filter)

            for cap in captured_filters:
                spainUrl += cap

            return scrapeAlert(spainUrl, email)

        else:
            raise ValueError("Mandatory filters like motor or model cannot be empty")

import requests
from bs4 import BeautifulSoup
from email_alert.mail_data import prepare_mail
from email.mime.text import MIMEText
import pandas as pd
import os
import functions
import re

path = os.path.abspath('data.csv')
url_id = {}
new_car = []
news = False
price_changes = {}


def add_ids(new_value):
    df_new = pd.DataFrame([new_value])
    try:
        df_existing = pd.read_csv(path)
    except FileNotFoundError:
        df_existing = pd.DataFrame()

    df_concatenated = pd.concat([df_existing, df_new], ignore_index=True)

    df_concatenated.to_csv(path, index=False)


def check_price_changes(id, car_price, url, email=None):
    df = pd.read_csv('data.csv')

    row1 = df[df['id'] == id]

    csv_price = row1.iloc[0]['car_price']

    idx = df.index[df['id'] == id]

    price_difference = csv_price - car_price

    if price_difference > 0.600 or price_difference < -0.600 and price_difference != 0.0:
        price_changes[url] = {"previous_price": csv_price, "car_price": car_price}
        df.loc[idx, 'car_price'] = car_price
        df.to_csv('data.csv', index=False)
        print(f"New Price changes for {url}")
        if email:
            notify_changes(price_changes)


def scrape_alert(url, email=None):
    global news

    print("Requested URL --> ", url)

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    json_data = functions.correct_json(soup)

    if json_data:

        more_items = get_pagination_items(url, json_data)

        item_list = json_data + more_items

        for item in item_list:
            url = item.get('url', '')
            print(url)
            id = url[-9:-1]
            id = int(id)

            try:
                car_price = scrape_prices(url)
                url_id[id] = {"url": url, "car_price": car_price}
                df_read = pd.read_csv(path)
                noNews = df_read['id'].isin([id]).any()

                if not noNews:
                    news = True
                    new_value = {"id": id, "url": url, "car_price": car_price}
                    add_ids(new_value)
                    new_car.append(url)
                    print(f'New item found: {id} // {url}// {car_price}')

                else:
                    check_price_changes(id, car_price, url, email)
            except ValueError as e:
                print(f"{e}")


    if news and email:
        body = "News:\n\n"
        for url in new_car:
            body += f"- {url}\n\n"
        message = MIMEText(body, 'plain')
        message['Subject'] = "🚗New vehicles avalilable🚗"
        prepare_mail(message)
        new_car.clear()
        news = False
        return news


def notify_changes(price_changes):
    body = "New price changes:\n\n"
    for url in price_changes:
        body += f"- {url}\n\n Previous Price: {price_changes[url]['previous_price']}€ New Price: {price_changes[url]['car_price']}€\n\n"
    message = MIMEText(body, 'plain')
    message['Subject'] = "💲New price changes💲"
    prepare_mail(message)
    price_changes.clear()
    return news


def scrape_prices(url):
    responseURL = requests.get(url)
    if responseURL.status_code != 200:
        raise ValueError(f"Cannot scrape {url}")
    else:
        soup = BeautifulSoup(responseURL.text, 'html.parser')
        car_price = soup.find('div', class_='datePrice')
        str_price = car_price.find('span').text
        price = float(str_price[:-2].replace(",", ""))
        return price


def url_constructor(model, motor, price=None, kms=None, email=None):
    spain_url = "https://www.bmwpremiumselection.es"

    if price or kms:

        params = []

        if price:
            price_param = f"condicion%5Bprecio_hasta%5D={price}"
            params.append(price_param)

        if kms:
            kms_param = f"&condicion%5Bkm_hasta%5D={kms}"
            params.append(kms_param)

        filters = [model, motor]

        captured_filters = []

        for filter in filters:
            if filter != None:
                filter = "/" + filter
                captured_filters.append(filter)

        for cap in captured_filters:
            spain_url += cap

        first_iteration = True

        for param in params:
            if first_iteration:
                first_iteration = False
                spain_url += "/?" + param
            else:
                spain_url += "&" + param

        return scrape_alert(spain_url, email)

    else:
        filters = [model, motor]

        no_errors = True

        for f in filters:
            if len(f) <= 0:
                no_errors = False

        if no_errors:
            captured_filters = []

            for filter in filters:
                if filter != None:
                    filter = "/" + filter
                    captured_filters.append(filter)

            for cap in captured_filters:
                spain_url += cap

            return scrape_alert(spain_url, email)

        else:
            raise ValueError("Mandatory filters like motor or model cannot be empty")


def get_pagination_items(url, first_result):

    url = url + '/?pagina=2&ordenacion=fecha_publicacion_descendente'

    indicator = True

    itemListElement = []

    last_response = first_result

    while indicator:
        response = requests.get(url)
        json_data =  functions.correct_json(BeautifulSoup(response.text, 'html.parser'))
        if json_data == last_response:
            indicator = False
            if not indicator:
                break
        #print("Registered items with pagination --> ", url)
        last_response = json_data
        for element in json_data:
            itemListElement.append(element)
        url = re.sub(r'=(\d+)', lambda m: f"={int(m.group(1)) + 1}", url)

    return itemListElement





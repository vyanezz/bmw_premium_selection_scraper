import pytest
from bmw import scrapeAlert
from bmw import url_constructor
import pandas as pd


url = 'https://www.bmwpremiumselection.es/serie-2/220i-coupe'


def test_mail():
    path = 'data.csv'
    df_read = pd.read_csv(path)
    df_read = df_read.drop(0)
    df_read.to_csv(path, index=False)

    assert scrapeAlert(url, email=True)



def test_no_mail():
    path = 'data.csv'
    df_read = pd.read_csv(path)
    df_read = df_read.drop(0)
    df_read.to_csv(path, index=False)

    assert not scrapeAlert(url, email=False)

def test_news():
    path = 'data.csv'
    df_read = pd.read_csv(path)
    df_read = df_read.drop(0)
    df_read.to_csv(path, index=False)
    delValues = df_read.count().sum()


    scrapeAlert(url, email=False)
    df_read = pd.read_csv(path)
    df_read.to_csv(path, index=False)
    addValues = df_read.count().sum()

    assert delValues < addValues


def test_no_news():
    path = 'data.csv'
    df_read = pd.read_csv(path)
    df_read.to_csv(path, index=False)
    assert not scrapeAlert(url, email=True)


def test_error_mandatory_filters():
    model = 'serie-2'
    motor = ''
    price = ''  # opt
    kms = ''  # opt

    with pytest.raises(ValueError, match='Mandatory filters like motor or model cannot be empty'):
        url_constructor(model=model, motor=motor, price=price, kms=kms, email=False)














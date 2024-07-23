
# Premium Selection Scraper

Scraper for pre-owned vehicles at BMW dealerships. The project has been created for purely educational purposes.

## What it can do

The script allows you to add a specific search model with filters and receive notifications about new vehicles for sale.

It also has a function to check price changes.

## Requisites

- Python 3
- Requests
- Pandas
- BeatifulSoup4
- Pytest
- Python-dotenv

You can install all with:
```bash
  pip install -r requirements.txt
```


You will also need to have a Gmail account or another email provider that allows third-party application access for SMTP configuration.



## Usage/Examples

In the case of setting up a Gmail account, two-step verification must be activated and application passwords (pass_smtp) must be generated in the account that will send the emails. 

Official guide: https://support.google.com/mail/answer/185833?hl=en

Inside the email_alert folder is ```mail_user_data.env``` that will contain the variables for sending emails.


```python
mail_smtp=xxxx
pass_smtp=xxxx

sender_email=xxxx
receiver_emails=xxxx
```


In the input file ```input_search.csv``` you can set yor search. For fields without filter set "_".

```python
model,motor,price,kms,email
serie-1,128ti,_,_,True
serie-3,320i,_,_,True

```

You can set the email value to ```True``` or ```False``` to receive or not receive news alerts.

The output data is stored in the ```data.csv``` file where the ```id``` and ```url``` to each vehicle found is filed.

```python
id,url,price
xxxxxxx,https://www.bmwpremiumselection.es/xxxxxxxx,xx
xxxxxxx,https://www.bmwpremiumselection.es/xxxxxxxx,xx
xxxxxxx,https://www.bmwpremiumselection.es/xxxxxxxx,xx

```





## Features coming soon

- New params to search
- Pagination for scrape number of vehicles
- Scrape more data like kms/fuel
- Scrape for specific countries/provinces
- New forms of notification






## Support

For support, write me an email yanez.vc@gmail.com.


## Authors

- [@vyanezz](https://github.com/vyanezz)


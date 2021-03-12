import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime

data = {
    'commit': 'Sign in',
    'authenticity_token': 'BWbKD/p4pb+blIfx37WnPS4KHzOy+hARrWeOsIh6CtfqbNM55pX3vQjAyYwSjzG8Ml5ZDGA2tFQCt3YakZ18Og==',
    'login': 'carlospepinillos418@gmail.com',
    'password': '4Merica123',
    'trusted_device': '',
    'webauthn-support': 'supported',
    'webauthn-iuvpaa-support': 'unsupported',
    'return_to': '',
    'allow_signup': '',
    'client_id': '',
    'integration': '',
    'required_field_beab': '',
    'timestamp': '1609651422842',
    'timestamp_secret': '76b50e48f6633b67ada4ebe745e30ca13a1f106b92b9f23e58b91afee2035288'
}

cookies = {
    '_octo': 'GH1.1.628872871.1609651294',
    'tz': 'America%2FBuenos_Aires',
    '_device_id': '940bae999b0d22ee2f271c8cd4542076',
    'has_recent_activity': '1',
    'logged_in': 'no',
    '_gh_sess': 'J2rCN50Ea%2F9tkMyWpiZc2SbArHgvM3Mu%2B%2FwbL5moKA8wPRJ0rStxnX%2FP4lWluW7i1cTMelmwVctCFr5lembFRBkQpWM2cFuQWbLR8zdy5EbTLgaV8ltrHBLC4fQTY5NMN267BlREWuiZAvkC6hD1G2FrM1OdsyxMHTIz48l5JI86MRUP8DHbX0qYlnZKELp7Xoq%2FSDr8wm5S7J7KaVIlU21Ignh6ExBuT9l3FvOwRo2RPpUhMC%2BNfWnXWMd2A4BpRhQGUl6YsbdVQck%2B5%2B91eg%3D%3D--HRJxCzCtuSMOlO%2B7--Fy%2Fqax%2BfHIf8gCZMMZRQrA%3D%3D',
    }

url = "https://github.com/session"

# Create the session object
s = requests.Session()

# Example request
response = s.post(url, data=data, cookies=cookies)

headers = {"Accept-Language": "en-US, en;q=0.5"}

results = s.get("https://github.com/CarlosPepinillos?tab=repositories", headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

user_repos_div = soup.find_all('div', class_="col-10 col-lg-9 d-inline-block")

names = []
urls = []
descriptions = []
used_languages = []
last_updates = []
labels = []

for container in user_repos_div:
    
    name_box = container.h3.a
    
    # Name
    name = name_box.text.strip()
    names.append(name)
    
    # Url
    name_url = name_box['href']
    url = f"https://github.com{name_url}"
    urls.append(url)
    
    # Decription
    description = container.find('p', class_='col-9 d-inline-block text-gray mb-2 pr-4').text.strip() if container.find('p', class_='col-9 d-inline-block text-gray mb-2 pr-4') else '-'
    descriptions.append(description)
    
    # Languages
    languages = container.find('span', itemprop='programmingLanguage').text.strip() if container.find('span', itemprop='programmingLanguage') else "-"
    used_languages.append(languages)
    
    # Last Updated
    time = container.find('div', class_="f6 text-gray mt-2").find('relative-time')['datetime']
    last_updates.append(time)
    
    # Label
    label = container.find('span', class_="Label Label--outline v-align-middle ml-1 mb-1").text if container.find('span', class_="Label Label--outline v-align-middle ml-1 mb-1") else "Public"
    labels.append(label)
    

# pandas dataframe
repos = pd.DataFrame({
    'name': names,
    'url': urls,
    'description': descriptions,
    'languages': used_languages,
    'last update': last_updates,
    'label': labels,
})

# print(repos)

#cleaning data 
repos['last update'] = pd.to_datetime(repos['last update'])

# print(repos)

repos.to_csv("repos.csv")
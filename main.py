from bs4 import BeautifulSoup
import requests
import lxml
from selenium import webdriver
import time

driver_path = "<your driver path>"

google_form_link = "<your url>"


URL = "<your url>"

header = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
}

r = requests.get(url=URL, headers=header)

soup = BeautifulSoup(r.content, "lxml")
find_links = soup.select("div .list-card-info a")
find_price = soup.select("div .list-card-info .list-card-price")
find_address = soup.select("div .list-card-info .list-card-addr")

links = [f"https://www.zillow.com{i['href']}" if "http" not in i["href"]
         else i["href"] for i in find_links]
price = [i.text.split("+")[0] for i in find_price]
address = [i.text.split(
    "|")[1] if "|" in i.text else i.text for i in find_address]


driver = webdriver.Chrome(executable_path=driver_path)
driver.get(url=google_form_link)
time.sleep(4)
for i in range(len(links)):
    form_addr = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_addr.send_keys(address[i])
    form_price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_price.send_keys(price[i])
    form_link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_link.send_keys(links[i])

    submit = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()
    time.sleep(2)
    submit_again = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_again.click()

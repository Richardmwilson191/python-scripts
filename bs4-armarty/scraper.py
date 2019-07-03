import requests
from bs4 import BeautifulSoup
import smtplib
from env import *


URL = 'https://armarty.com/product-category/men-clothing/'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find_all(
    class_="woocommerce-loop-product__title")

price = soup.find_all(
    class_="woocommerce-Price-amount amount")


def armarty():
    price_list = []

    for pri in price:
        for pr in pri.children:
            if pr.string != '$':
                price_list.append(float(pr.string))

    clothes_list = []

    for [tit] in title:
        clothes_list.append(tit)

    x = 0
    clothes = ""
    for x in range(len(clothes_list)):
        if price_list[(x + (x+1)) - 1] < 30:
            clothes += f"{clothes_list[x]} {str(price_list[(x + (x+1))-1])}\n"

    send_mail(clothes)


def send_mail(clothes):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(EMAIL, PASSWORD)

    subject = "Men's items below $30"
    body = f"These items are availabel for less than $30:\n{clothes}\nView them here https://armarty.com/product-category/men-clothing/"
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        EMAIL,
        RECEIVING_EMAIL,
        msg
    )

    print('Success')
    server.quit()


armarty()

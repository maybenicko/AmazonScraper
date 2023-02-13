import requests
import csv
from time import sleep
from termcolor import colored
from datetime import datetime
from dhooks import *
from bs4 import BeautifulSoup
import threading


def get_time(thread_num):
    t = str(datetime.utcnow().strftime('%H:%M:%S'))
    (h, m, s) = t.split(":")
    h = int(h) + 1
    final_time = f"{h}:{m}:{s}"
    final = f"[Monitoring] [{final_time}] [{thread_num}]"
    return final


def scraping(url, session, delay, thread_num):
    print(f"{colored(get_time(thread_num), 'blue')} {colored(f'Getting product page', 'cyan')} ")
    r = session.get(url)
    status = int(r.status_code)
    if r.status_code != 200:
        sleep(delay)
        return status, status
    elif r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        txt = r.text
        title = soup.find("span", {"id": "productTitle"}).text.strip()
        whole_price = soup.find("span", {"class": "a-offscreen"}).text
        price_int = whole_price.split(',')[0]
        image = txt.split('var iUrl = "')[1].split('";')[0]
        sleep(delay)
        return status, title, price_int, whole_price, image, soup


def send_webhook(url, title, whole_price, image, thread_num):
    hook = Webhook(
        'https://discord.com/api/webhooks/801844941781073940/8sYwB54PmyK7dp6YAg-YHvz3V1pG887gyKHu35wHGbK29MI4gx7g4tP1AWMgGnQV4WsI')

    now = str(datetime.utcnow().strftime('%d-%m-%Y'))
    embed = Embed(
        color=0x202020
    )
    embed.set_title(title=":fire:Price decrease:fire:", url=url)
    embed.set_author(name="AmazonMonitor",
                     icon_url="https://cdn.discordapp.com/attachments/799962707377127444/990"
                              "984201664888912/bartFoto.PNG")
    embed.add_field(name="Store", value="Amazon")
    embed.add_field(name="Product", value=f"[{title}]({url})")
    embed.set_thumbnail(url=image)
    embed.add_field(name="Price", value=f"{whole_price}")
    embed.set_footer(text=f"{now} • Powered by @nicko",
                     icon_url="https://cdn.discordapp.com/attachments/799962707377127444/9909842"
                              "01664888912/bartFoto.PNG")
    print(f"{colored(get_time(thread_num), 'blue')} {colored(f'Submitting webhook', 'cyan')} ")
    hook.send(embed=embed)
    print(f"{colored(get_time(thread_num), 'blue')} {colored(f'Success', 'green')} ")
    return


def main(url, price_filter, delay, thread_num):
    print(f"{colored(get_time(thread_num), 'blue')} {colored(f'Starting monitoring', 'grey')} ")
    delay = int(delay) / 1000
    session = requests.Session()
    while True:
        info = scraping(url, session, delay, thread_num)
        status = info[0]
        if int(status) == 200:
            int_price = info[2]
            print(f"{colored(get_time(thread_num), 'blue')} {colored(f'Checking price', 'cyan')} ")
            if int(int_price) < int(price_filter):
                print(f"{colored(get_time(thread_num), 'blue')} {colored(f'Price change!', 'green')} ")
                whole_price = info[3]
                image = info[4]
                send_webhook(url, info[1], whole_price, image, thread_num)
                break
        else:
            if int(status) == 503:
                print(f"{colored(get_time(thread_num), 'blue')} {colored(f'Server error [{info[0]}]', 'red')} ")
            elif int(status) == 404:
                print(f"{colored(get_time(thread_num), 'blue')} {colored(f'IP banned [{info[0]}]', 'red')} ")
            else:
                print(f"{colored(get_time(thread_num), 'blue')} "
                      f"{colored(f'Unknown connection error [{info[0]}]', 'red')} ")


def start():
    with open('scrape.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        i = 0
        for row in csv_reader:
            i += 1
            if line_count == 0:
                line_count += 1
            else:
                sleep(0.03)
                try:
                    url = row[0]
                    price_filter = row[1]
                    delay = row[2]
                    thread = threading.Thread(target=main, args=(url, price_filter, delay, (i-2)))
                    thread.start()
                except Exception as e:
                    print(f"{colored(f'CSV error [{e}]', 'red')} ")
                    pass


start()
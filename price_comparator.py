import requests
from bs4 import BeautifulSoup
import mail_setting
from time import sleep
# from resources.headers import header_list
# from resources.asin import asin_list

ASIN1 = "B07PHPXHQS" # (echo-dot-3-generacion-altavoz-inteligente-con-alexa)
ASIN2 = " "

URL = f"https://www.amazon.es/dp/{ASIN1}"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}


def getPrice():
    page = requests.get(URL, headers=HEADER)
    soup = BeautifulSoup(page.content, "lxml")
    price = soup.find(id="corePriceDisplay_desktop_feature_div").get_text()
    price = price[:-2]
    price = price.replace(",",".")
    return price

def readFile():
    f = open("price.txt", "r")
    if f.mode == "r":
        content = f.read()
    f.close()
    return content


def writeFile(number):
    f = open("price.txt", "w")
    if f.mode == "w":
        f.write(number)
    f.close()


def main():
    try:
        open("price.txt")
    except FileNotFoundError:
        writeFile(getPrice())

    while(True):
        oldPrice = readFile()
        newPrice = getPrice()

        if float(newPrice) < float(oldPrice) - 10:
            message = "Su producto ha sido rebajado a " + \
                str(newPrice) + " euros. \n" + "URL: " + str(URL)
            mail_setting.sendemail(message)
            writeFile(newPrice)
            print("Mail sent \n")

        sleep(3600)


if __name__ == "__main__":
    main()


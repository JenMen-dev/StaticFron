import requests
from bs4 import BeautifulSoup
import mail
from time import sleep

URL = "https://www.amazon.es/echo-dot-3-generacion-altavoz-inteligente-con-alexa-tela-de-color-antracita/dp/B07PHPXHQS/ref=sr_1_2?crid=ZXRZX6YY1RLG&keywords=alexa&qid=1648733243&sprefix=alexa%2Caps%2C134&sr=8-2"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}


def getprice():
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
        writeFile(getprice())

    while(True):
        oldprice = readFile()
        newprice = getprice()

        if float(newprice) < float(oldprice) - 10:
            message = "Su producto ha sido rebajado a " + \
                str(newprice) + " euros. \n" + "URL: " + str(URL)
            mail.sendemail(message)
            writeFile(newprice)
            print("Mail sent \n")

        sleep(3600)


if __name__ == "__main__":
    main()


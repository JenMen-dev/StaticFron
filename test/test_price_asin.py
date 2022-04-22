import requests
from bs4 import BeautifulSoup
import mail_setting
from time import sleep
from resources.headers import header_list

ASIN = "B07PHPXHQS"

def get_data(asin):

    URL = f"https://www.amazon.es/dp/{ASIN}"
    data_list=[]

    header_position = 0
    headers={'User-Agent': header_list[header_position]}
    response = False

    while not response:
        if header_position >= (len(header_list)-1):
            data_list=["No se encontraron datos para este ASIN"]
            break
        try:
            response = requests.post(URL,headers=headers)
            if response.status_code == 200:
                texto = response.content
                soup = BeautifulSoup(texto,"lxml")
                response = soup.find(class_="a-unordered-list a-vertical a-spacing-mini").find_all(class_="a-list-item")
                data_list.append(soup.title.text)
                for item in response:
                    data_list.append(item.text)
        except:
            header_position+=1

    return data_list

'''def getprice():
    page = requests.get(URL, headers=HEADER)
    soup = BeautifulSoup(page.content, "lxml")
    mydivs = soup.find("span", {"class": "a-offscreen"}).get_text()
    mydivs = mydivs[:-1]
    mydivs = mydivs.replace(",",".")
    return mydivs'''

'''def readFile():
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

        sleep(2)


if __name__ == "__main__":
    main()'''

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge
import time
import csv

PATH = "C:\Drivers\msedgedriver.exe"
driver = Edge(PATH)

# Seleziono le recensioni con già selezionate le stelle
driver.get('https://www.amazon.it/product-reviews/B000J34HN4/ref=acr_dp_hist_1?ie=UTF8&filterByStar=five_star&reviewerType=all_reviews#reviews-filter-bar')
print("Page title is: %s" % (driver.title))
# Aspetto il caricamento della pagina, trovo il bottone per accettare la policy dei cookie attraverso l'Xpath e lo clicco
# time.sleep(1)
cookiebottone = driver.find_element("xpath", '//*[@id="sp-cc-accept"]')
cookiebottone.click()
# Aspetto il nuovo caricamento della pagina ed estraggo i dati che mi interessano
time.sleep(2)

testoelem = []
for i in range(80, 200):
    elementi = driver.find_elements(
        "xpath", '//div[starts-with(@id,"customer_review")]/div[4]')
    # print(elementi)
    # Uso il try in modo tale che quando trova i video non blocchi l'estrazione
    for index, elem in enumerate(elementi):
        try:
            elemento = "A" + "5" + \
                (str(i)+str(index)).zfill(4), "1", "0", elem.__getattribute__("text")
            testoelem.append(elemento)
        except:
            print("Contiene video")
    # print(testoelem)
    # Clicca l'elemento per avanzare di pagina dopo aver atteso il caricamento (Se non trova più l'elemento mi fermo, significa che sono finite le pagine)
    time.sleep(10)

    try:
        driver.find_element(
            "xpath", "//*[@id='cm_cr-pagination_bar']/ul/li[2]/a").click() #Bottone per avanzamento pagina
    except:
        time.sleep(2)
        print("Esecuzione terminata")
        break
    # Esporto i dati sul file CSV con codifica "UTF-8"
    # print(testoelem)
with open("C:\output.csv", 'a', encoding='utf-8') as data_file:
    writer = csv.writer(data_file, delimiter='\t')
    writer.writerow(testoelem)
    data_file.close()

# Termina l'esecuzione
driver.quit()

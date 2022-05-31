import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge
import time
import csv

PATH = "C:\Drivers\msedgedriver.exe"
driver = Edge(PATH)
stelle = ['one', 'two', 'three', 'four', 'five']
testoelem = []
# Seleziono le recensioni con già selezionate le stelle
for stella in stelle:
    driver.get('https://www.amazon.it/product-reviews/8830101680/ref=acr_dp_hist_5?ie=UTF8&filterByStar=' +
               stella+'_star&reviewerType=all_reviews#reviews-filter-bar')
    print("Page title is: %s" % (driver.title))
    # Aspetto il caricamento della pagina, trovo il bottone per accettare la policy dei cookie attraverso l'Xpath e lo clicco
    # time.sleep(1)
    if stella == 'one':
        cookiebottone = driver.find_element("xpath", '//*[@id="sp-cc-accept"]')
        cookiebottone.click()
    # Aspetto il nuovo caricamento della pagina ed estraggo i dati che mi interessano
    time.sleep(2)

    if stella == 'one':
        codice = range(0, 100)
        star = 1
    elif stella == 'two':
        codice = range(20, 100)
        star = 2
    elif stella == 'three':
        codice = range(40, 100)
        star = 3
    elif stella == 'four':
        codice = range(60, 100)
        star = 4
    else:
        codice = range(80, 100)
        star = 5
    for i in codice:
        elementi = driver.find_elements(
            "xpath", '//div[starts-with(@id,"customer_review")]/div[4]')
        # Uso il try in modo tale che quando trova i video non blocchi l'estrazione
        for index, elem in enumerate(elementi):
            try:
                elemento = "A" + str(star) + \
                    (str(i)+str(index)).zfill(4), elem.__getattribute__("text")
                testoelem.append(elemento)
            except:
                print("Contiene video")
        # print(testoelem)
        # Clicca l'elemento per avanzare di pagina dopo aver atteso il caricamento (Se non trova più l'elemento mi fermo, significa che sono finite le pagine)
        time.sleep(10)
        try:
            driver.find_element(
                "xpath", "//*[@id='cm_cr-pagination_bar']/ul/li[2]/a").click()  # Bottone per andare avanti con le pagine
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

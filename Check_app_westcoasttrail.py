from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import winsound
from datetime import datetime
import pyautogui
import threading
import ctypes

# Konstanty pro zabránění spánku i vypnutí obrazovky
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002  # Přidáme tuto konstantu pro aktivní obrazovku

def zabranit_spanku():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
    while True:
        time.sleep(60)  # Obnovuje stav každou minutu

vlakno_spanku = threading.Thread(target=zabranit_spanku, daemon=True)
vlakno_spanku.start()

# Nastavení Geckodriveru
options = Options()
#options.add_argument("--headless")  # Volitelné: spuštění bez otevření okna
service = Service("C:/Users/BIKEMAX/Downloads/geckodriver.exe")  # cesta k Geckodriveru

# Seznam specifických dnů
povolene_dny = {"July 30", "July 31", "August 1", "August 2", "August 3", "August 4", "August 5", "August 6", }

def kontrolovat_terminy():
    driver = webdriver.Firefox(service=service, options=options)
    volna_mista = []
    # Získání aktuálního času
    aktualni_cas = datetime.now()
    #print(volna_mista)

    try:
        # Otevření webové stránky
        driver.get("https://www.westcoasttrail.app/permits/")
        time.sleep(5)

        # Vyhledání všech prvků s třídou "calendar-cell"
        elements = driver.find_elements(By.CLASS_NAME, "calendar-cell")

        for element in elements:
            bg_color = element.value_of_css_property("background-color")
            if bg_color == "rgb(0, 128, 0)":  # Zelená barva (RGB)
                # Najít nejbližší nadřazený <h2>
                parent = element.find_element(By.XPATH, "./ancestor::table//preceding::h2[1]")
                month = parent.text if parent else "Neznámý měsíc"
                day = element.text.strip()

                full_date = f"{month} {day}"
                if full_date in povolene_dny:
                    volna_mista.append(full_date)

        if volna_mista:
            print("Volné místo:", ", ".join(volna_mista))
            winsound.PlaySound("Dobre_rano_curaci.wav", winsound.SND_FILENAME)
            

        else:
            print("Žádný volný termín. ", aktualni_cas.strftime("%H:%M:%S"))

    finally:
        driver.quit()  # Ukončení prohlížeče
        
# Nekonečná smyčka pro opakovanou kontrolu každých 31 minut
while True:
    volna_mista = kontrolovat_terminy()
    
    time.sleep(32 * 60)  # Počkej 31 minut
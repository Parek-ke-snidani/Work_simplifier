from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import time
# Nastavení webového prohlížeče (např. Chrome)
driver = webdriver.Chrome()

# Otevření cílové stránky
url = "https://metrics.torproject.org/rs.html#advanced"  # Změňte na URL, kterou potřebujete
driver.get(url)

time.sleep(4)
try:
    
    # Najití všech elementů s třídou "form-control"
    elements = driver.find_elements(By.ID, "advanced-search-country")
    print(len(elements))  # Zjistí, kolik elementů bylo nalezeno
    
    # Vytvoření nového Excel souboru
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Data z formuláře"

    # Iterace přes elementy a zapisování hodnot do Excelu
    for index, element in enumerate(elements, start=1):
        text = element.get_attribute("value") or element.text
        sheet.cell(row=index, column=1, value=text)  # Zápis do Excelu

    # Uložení Excelu
    workbook.save("data_form_control.xlsx")
    print("Data byla úspěšně zkopírována a uložena do 'data_form_control.xlsx'.")
    
finally:
    # Zavření prohlížeče
    driver.quit()

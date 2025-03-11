from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import requests
from PIL import Image
from io import BytesIO
import keyboard
import pyautogui
import pandas as pd
import pyperclip
from openpyxl import load_workbook
from selenium.webdriver.support.ui import WebDriverWait
import re

# Cesta k geckodriveru (zadejte správnou cestu k vašemu geckodriveru)
geckodriver_path = "Path//to//geckodriver.exe"

# Nastavení pro Firefox (Geckodriver) a Tor proxy
tor_proxy = "127.0.0.1:9050"  # Tor běží na localhostu na portu 9050

# Nastavení pro Firefox
firefox_options = Options()
#firefox_options.set_headless(False)  # Pokud chcete spustit Firefox v GUI, nastavte na False

# Nastavení proxy pro Tor (SOCKS5)
firefox_options.set_preference("network.proxy.type", 1)
firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
firefox_options.set_preference("network.proxy.socks_port", 9150)
firefox_options.set_preference("network.proxy.socks_remote_dns", True)

# Spuštění Firefoxu s Tor proxy
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)

def wait_for_page_load(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

def sanitize_filename(filename):
    # Odstranit neplatné znaky podle pravidel Windows (např. \ / : * ? " < > |)
    filename = re.sub(r'[\/:*?"<>|]', '_', filename)
    return filename
## Otevření webové stránky a přihláseí se

# Otevření URL (např. stránky pro kontrolu Tor připojení)
driver.get("https://klient.napojse.cz/admin/sign/in")  # Stránka pro ověření, že používáte Tor

wait = WebDriverWait(driver, 10)

# Počkejte chvíli pro kontrolu výsledku
wait_for_page_load(driver)

email_input = driver.find_element(By.ID, "frm-signInForm-signInForm-email") #Vložení emailu do input políčka na heslo na stránce napojse/signin
email_input.send_keys("Example@email.com") #Example@email.com

email_input = driver.find_element(By.ID, "frm-signInForm-signInForm-password") #Vložení hesla do input políčka na heslo na stránce napojse/signin
email_input.send_keys("Heslo") # Heslo

button = driver.find_element(By.NAME, "_submit")
button.click()
#pyautogui.moveTo("signin.png")
#pyautogui.leftClick()

time.sleep(5)

## Načítání excelu a hledání kol na stránce a stahování obrázků

excel_file = 'excel.xlsx'  # Zadej cestu k tvému Excel souboru
df = pd.read_excel(excel_file)

# Načteme Excel soubor pomocí openpyxl pro zápis
wb = load_workbook(excel_file)
ws = wb.active  # Vybereme aktivní list (první list v souboru)
save_interval = 10  # Uložení po každých 10 cyklech
### Přidělat loop na procházení další položky v řádku, když není nalezena položka photo (fotka)

for index, row in df.iterrows():
    number = row.iloc[0]  

    number_without_decimals = int(number)
    # Zkopírování textu do clipboardu
    pyperclip.copy(number_without_decimals)
    
    #pyautogui.moveTo("search.png") # Najití hledajícího pole
    #pyautogui.leftClick() # Zakliknutí pole

    searchconsole = driver.find_element(By.ID, "frm-searchForm-q")
    searchconsole.click()

    keyboard.press_and_release("ctrl+v")  # Vložení zkopírovaného textu
    keyboard.press_and_release("enter") # Spuštění Hledání
    time.sleep(5)

    found_photo = False  # Příznak pro nalezení 'photo' class
    
    try:
        wait_for_page_load(driver)
        # Hledání divu s fotkou na stránce
        photo_div = driver.find_element(By.CLASS_NAME, "photo")  # Najděte div s třídou 'photo'
        
        # Pokud je fotka nalezena, stáhněte obrázek
        img_url = photo_div.find_element(By.TAG_NAME, "img").get_attribute("src")  # Získání URL obrázku
        response = requests.get(img_url)  # Stažení obrázku
        img = Image.open(BytesIO(response.content))  # Otevření obrázku
        
        # Najděte div s třídou 'info'
        info_div = driver.find_element(By.CLASS_NAME, "info")

        # Poté hledejte element s třídou 'underline-hover' uvnitř tohoto divu
        name_element = info_div.find_element(By.CLASS_NAME, "underline-hover")

        # Získání textu jako názvu souboru
        img_name = name_element.text.strip()
        img_name = sanitize_filename(img_name)  # Sanitize názvu souboru
        
        # Uložení obrázku na disk
        img.save(f"{img_name}.png")
        found_photo = True

    except Exception as e:
        print(f"Foto nebylo nalezeno pro číslo {number_without_decimals}: {e}")
    
    if not found_photo:
        # Pokud nebyla fotka nalezena, zapište "Not found" do sloupce "I"
        df.at[index, 'I'] = 'Not found'
        continue

     # Uložení souboru po každých 10 cyklech
    if (index + 1) % save_interval == 0:
        df.to_excel('vase_upraveny_soubor.xlsx', index=False)
        print(f"Data uložena po {index + 1} cyklech")

    # Pauza mezi operacemi
    time.sleep(1)

# Uložení upraveného DataFrame zpět do Excelu
df.to_excel('vase_upraveny_soubor.xlsx', index=False)
print("Uloženo")
# Ukončení driveru
driver.quit()

while True:
    if keyboard.is_pressed('esc'):
        print("ESC stisknuto, program končí.")
        break  # Ukončí program


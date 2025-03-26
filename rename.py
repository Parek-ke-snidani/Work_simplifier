import os
import pandas as pd

# Cesta k Excel souboru a složce se soubory
excel_soubor = "01seznam_souboru.xlsx"
slozka = "C://Users//BIKEMAX//GIT-Work//images//flags"

# Načtení Excelového souboru
data = pd.read_excel(excel_soubor)



# Iterace přes řádky v Excelu
for stary, novy in zip(data["A"], data["B"]):
    # Starý a nový název včetně přípony
    stary_soubor = f"{stary}.png"
    novy_soubor = f"{novy}.png"

    # Cesty ke starému a novému souboru
    stara_cesta = os.path.join(slozka, stary_soubor)
    nova_cesta = os.path.join(slozka, novy_soubor)

    # Přejmenování souboru
    if os.path.exists(stara_cesta):
        os.rename(stara_cesta, nova_cesta)
        print(f"Přejmenováno: {stary_soubor} -> {novy_soubor}")
    else:
        print(f"Soubor {stary_soubor} nenalezen, přeskočeno.")
       

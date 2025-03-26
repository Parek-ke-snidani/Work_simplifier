import pandas as pd
import requests

def check_url_status(file_path):
    # Načtení Excel souboru
    df = pd.read_excel(file_path)

    # Procházení URL ve sloupci B (od druhé řádky)
    for index, url in enumerate(df['Product URL'][1:], start=1):  # Skip first row (header)
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            if response.status_code < 400:
                df.loc[index, 'C'] = "Dostupná"
            else:
                df.loc[index, 'C'] = f"Nedostupná (Status code: {response.status_code})"
        except requests.RequestException as e:
            df.loc[index, 'C'] = f"Chyba ({e})"

    # Uložení výsledků zpět do Excelu
    df.to_excel(file_path, index=False)

# Cesta k Excel souboru
file_path = 'shoptet_product.xlsx'

# Zavolání funkce
check_url_status(file_path)

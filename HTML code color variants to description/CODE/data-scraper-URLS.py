import requests
from bs4 import BeautifulSoup
import pandas as pd

# Seznam kategorií k procházení
CATEGORY_URLS = [
    "https://www.bikemax.cz/kvalitni-helmy-na-kolo-woom-pro-deti/",
    "https://www.bikemax.cz/kvalitni-helmy-na-detske-kolo-rascal/"
]

def get_max_pages(category_url):
    """Zjistí maximální počet stránek v kategorii."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(category_url, headers=headers)
    response.encoding = response.apparent_encoding  

    if response.status_code != 200:
        print(f"❌ Nelze načíst {category_url}")
        return 1  

    soup = BeautifulSoup(response.text, "html.parser")
    last_page_link = soup.find("a", {"data-testid": "linkLastPage"})
    if last_page_link:
        try:
            return int(last_page_link.get("href").split("-")[-1].replace("/", ""))
        except ValueError:
            return 1

    return 1

def get_products(category_url):
    """Scrapuje produkty z jedné stránky."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(category_url, headers=headers)
    response.encoding = response.apparent_encoding  

    if response.status_code != 200:
        print(f"❌ Chyba při načítání {category_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []
    
    for product in soup.find_all("div", {"data-micro": "product"}):
        name_tag = product.find("span", {"data-micro": "name"})
        name = name_tag.text.strip() if name_tag else "N/A"

        url_tag = product.find("a", {"data-micro": "url"})
        url = "N/A"
        if url_tag:
            url = url_tag.get("href")
            if url.startswith("/"):
                url = "https://www.bikemax.cz" + url

        products.append((name, url))  # Už neukládáme sloupec Category

    return products

# Scrapování více kategorií s automatickou detekcí stránek
all_products = []
for category in CATEGORY_URLS:
    max_pages = get_max_pages(category)
    print(f"🔍 Kategorie: {category} (Max {max_pages} stránek)")
    
    for page in range(1, max_pages + 1):
        url = f"{category}strana-{page}/"
        print(f"📄 Načítám: {url}")
        all_products.extend(get_products(url))

# Uložení výsledků do Excel souboru
df = pd.DataFrame(all_products, columns=["Product Name", "Product URL"])
df = df.drop_duplicates()  # Odstranění duplicit
df.to_excel("shoptet_product.xlsx", index=False, engine="openpyxl")

print("✅ Hotovo! Data uložena do 'shoptet_products.xlsx'")

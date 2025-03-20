import requests
from bs4 import BeautifulSoup
import pandas as pd

# Seznam kategorií k procházení
CATEGORY_URLS = [
    "https://www.bikemax.cz/helmy-na-kolo/",
    "https://www.bikemax.cz/kvalitni-helmy-na-kolo-woom-pro-deti/",
    "https://www.bikemax.cz/kvalitni-helmy-na-detske-kolo-rascal/",
    "https://www.bikemax.cz/helmy-na-kolo-pro-dospele/",
    "https://www.bikemax.cz/enduro-a-trailove-helmy-na-kolo/",
    "https://www.bikemax.cz/helmy-na-elektrokolo/",
    "https://www.bikemax.cz/damske-helmy-na-kolo/",
    "https://www.bikemax.cz/silnicni-helmy-na-kolo/",
    "https://www.bikemax.cz/helmy-na-kolo-detske/",
    "https://www.bikemax.cz/mips-helmy-na-kolo/"
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
    
    # Najdeme poslední stránku pomocí `data-testid="linkLastPage"`
    last_page_link = soup.find("a", {"data-testid": "linkLastPage"})
    if last_page_link:
        try:
            return int(last_page_link.get("href").split("-")[-1].replace("/", ""))
        except ValueError:
            return 1

    return 1  # Pokud se nenajde, vrátíme 1

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

        products.append((name, url, category_url))  

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

# Uložení výsledků
df = pd.DataFrame(all_products, columns=["Product Name", "Product URL", "Category"])
df.to_csv("shoptet_products.csv", index=False, encoding="utf-8-sig")

print("✅ Hotovo! Data uložena do 'shoptet_products.csv'")
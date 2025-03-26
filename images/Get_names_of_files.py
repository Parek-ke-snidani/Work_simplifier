import os
from openpyxl import Workbook

# Cesta k vaší složce
slozka = "C://Users//BIKEMAX//GIT-Work//images//flags"

# Vytvoření nového Excelového sešitu
wb = Workbook()
ws = wb.active
ws.title = "Seznam souborů"

# Získání seznamu názvů souborů a přidání do Excelu
for idx, soubor in enumerate(os.listdir(slozka), start=1):
    ws.cell(row=idx, column=1, value=soubor)

# Uložení Excelového souboru
wb.save("01seznam_souboru.xlsx")

print("Seznam souborů byl uložen do 'seznam_souboru.xlsx'")

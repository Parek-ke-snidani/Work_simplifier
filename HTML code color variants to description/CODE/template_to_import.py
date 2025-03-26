import tkinter as tk
from tkinter import filedialog
import pandas as pd

exported_file_path = ""
template_file_path = ""

def select_exported_file():
    global exported_file_path
    exported_file_path = filedialog.askopenfilename(title="Vyberte exported file")
    exported_label.config(text=f"Exported file: {exported_file_path}")

def select_template_file():
    global template_file_path
    template_file_path = filedialog.askopenfilename(title="Vyberte Template file")
    template_label.config(text=f"Template file: {template_file_path}")

def process_files():
    if not exported_file_path or not template_file_path:
        output_label.config(text="Prosím, vyberte oba soubory.")
        return

    # Načtení Excel souborů do pandas DataFrame
    exported_df = pd.read_excel(exported_file_path)
    template_df = pd.read_excel(template_file_path)

    # Zpracování dat na základě sloupců "name" a "HTML code"
    for index, row in exported_df.iterrows():
        name_value = row["name"]
        description = row["description"]

        # Pokud je description NaN, nahradíme ho prázdným textem
        if pd.isna(description):
            description = ""

        # Hledání odpovídající hodnoty "HTML code" v Template file
        html_code_row = template_df[template_df["name"] == name_value]
        if not html_code_row.empty:
            html_code = html_code_row.iloc[0]["HTML code"]

            # Kontrola obsahu description
            if "<div id=\"colour_variants\">" not in description:
                exported_df.at[index, "description"] = description + html_code

    # Automatické uložení upraveného souboru pod názvem "for_import.xlsx"
    output_file_path = "for_import.xlsx"
    exported_df.to_excel(output_file_path, index=False)
    output_label.config(text=f"Soubor byl uložen jako '{output_file_path}'!")

# Vytvoření GUI pomocí tkinter
root = tk.Tk()
root.title("Excel Processor")


intro_label = tk.Label(root, text="Vyberte exported file a Template file:")
intro_label.pack()

exported_label = tk.Label(root, text="Exported file: [nevybrán]")
exported_label.pack()

exported_button = tk.Button(root, text="Vyberte Exported file", command=select_exported_file)
exported_button.pack()

template_label = tk.Label(root, text="Template file: [nevybrán]")
template_label.pack()

template_button = tk.Button(root, text="Vyberte Template file", command=select_template_file)
template_button.pack()

process_button = tk.Button(root, text="Spustit zpracování", command=process_files)
process_button.pack()

output_label = tk.Label(root, text="")
output_label.pack()

root.mainloop()

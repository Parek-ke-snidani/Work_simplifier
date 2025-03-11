import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox, simpledialog
import os
import json


# Slovník pro mapování názvů zemí na jejich kódy
country_mapping = {
    "Andorra": "ad",
    "United Arab Emirates": "ae",
    "Afghanistan": "af",
    "Antigua and Barbuda": "ag",
    "Anguilla": "ai",
    "Albania": "al",
    "Armenia": "am",
    "Netherlands Antilles": "an",
    "Angola": "ao",
    "Antarctica": "aq",
    "Argentina": "ar",
    "American Samoa": "as",
    "Austria": "at",
    "Australia": "au",
    "Aruba": "aw",
    "Aland Islands": "ax",
    "Azerbaijan": "az",
    "Bosnia and Herzegovina": "ba",
    "Barbados": "bb",
    "Bangladesh": "bd",
    "Belgium": "be",
    "Burkina Faso": "bf",
    "Bulgaria": "bg",
    "Bahrain": "bh",
    "Burundi": "bi",
    "Benin": "bj",
    "Saint Bartelemey": "bl",
    "Bermuda": "bm",
    "Brunei": "bn",
    "Bolivia": "bo",
    "Brazil": "br",
    "Bahamas": "bs",
    "Bhutan": "bt",
    "Bouvet Island": "bv",
    "Botswana": "bw",
    "Belarus": "by",
    "Belize": "bz",
    "Canada": "ca",
    "Cocos (Keeling) Islands": "cc",
    "Democratic Republic of the Congo": "cd",
    "Central African Republic": "cf",
    "Congo": "cg",
    "Switzerland": "ch",
    "Côte d'Ivoire": "ci",
    "Cook Islands": "ck",
    "Chile": "cl",
    "Cameroon": "cm",
    "China": "cn",
    "Colombia": "co",
    "Costa Rica": "cr",
    "Cuba": "cu",
    "Cape Verde": "cv",
    "Christmas Island": "cx",
    "Cyprus": "cy",
    "Czech Republic": "cz",
    "Germany": "de",
    "Djibouti": "dj",
    "Denmark": "dk",
    "Dominica": "dm",
    "Dominican Republic": "do",
    "Algeria": "dz",
    "Ecuador": "ec",
    "Estonia": "ee",
    "Egypt": "eg",
    "Western Sahara": "eh",
    "Eritrea": "er",
    "Spain": "es",
    "Ethiopia": "et",
    "Finland": "fi",
    "Fiji": "fj",
    "Falkland Islands (Malvinas)": "fk",
    "Federated States of Micronesia": "fm",
    "Faroe Islands": "fo",
    "France": "fr",
    "Metropolitan France": "fx",
    "Gabon": "ga",
    "United Kingdom": "gb",
    "Grenada": "gd",
    "Georgia": "ge",
    "French Guiana": "gf",
    "Guernsey": "gg",
    "Ghana": "gh",
    "Gibraltar": "gi",
    "Greenland": "gl",
    "Gambia": "gm",
    "Guinea": "gn",
    "Guadeloupe": "gp",
    "Equatorial Guinea": "gq",
    "Greece": "gr",
    "South Georgia and the South Sandwich Islands": "gs",
    "Guatemala": "gt",
    "Guam": "gu",
    "Guinea": "gw",
    "Guyana": "gy",
    "Hong Kong": "hk",
    "Heard Island and McDonald Islands": "hm",
    "Honduras": "hn",
    "Croatia": "hr",
    "Haiti": "ht",
    "Hungary": "hu",
    "Indonesia": "id",
    "Ireland": "ie",
    "Israel": "il",
    "Isle of Man": "im",
    "India": "in",
    "British Indian Ocean Territory": "io",
    "Iraq": "iq",
    "Iran": "ir",
    "Iceland": "is",
    "Italy": "it",
    "Jersey": "je",
    "Jamaica": "jm",
    "Jordan": "jo",
    "Japan": "jp",
    "Kenya": "ke",
    "Kyrgyzstan": "kg",
    "Cambodia": "kh",
    "Kiribati": "ki",
    "Comoros": "km",
    "Saint Kitts and Nevis": "kn",
    "North Korea": "kp",
    "Republic of Korea": "kr",
    "Kuwait": "kw",
    "Cayman Islands": "ky",
    "Kazakhstan": "kz",
    "Laos": "la",
    "Lebanon": "lb",
    "Saint Lucia": "lc",
    "Liechtenstein": "li",
    "Sri Lanka": "lk",
    "Liberia": "lr",
    "Lesotho": "ls",
    "Lithuania": "lt",
    "Luxembourg": "lu",
    "Latvia": "lv",
    "Libya": "ly",
    "Morocco": "ma",
    "Monaco": "mc",
    "Republic of Moldova": "md",
    "Montenegro": "me",
    "Saint Martin": "mf",
    "Madagascar": "mg",
    "Marshall Islands": "mh",
    "Macedonia": "mk",
    "Mali": "ml",
    "Myanmar": "mm",
    "Mongolia": "mn",
    "Macau": "mo",
    "Northern Mariana Islands": "mp",
    "Martinique": "mq",
    "Mauritania": "mr",
    "Montserrat": "ms",
    "Malta": "mt",
    "Mauritius": "mu",
    "Maldives": "mv",
    "Malawi": "mw",
    "Mexico": "mx",
    "Malaysia": "my",
    "Mozambique": "mz",
    "Namibia": "na",
    "New Caledonia": "nc",
    "Niger": "ne",
    "Norfolk Island": "nf",
    "Nigeria": "ng",
    "Nicaragua": "ni",
    "Netherlands": "nl",
    "Norway": "no",
    "Nepal": "np",
    "Nauru": "nr",
    "Niue": "nu",
    "New Zealand": "nz",
    "Oman": "om",
    "Panama": "pa",
    "Peru": "pe",
    "French Polynesia": "pf",
    "Papua New Guinea": "pg",
    "Philippines": "ph",
    "Pakistan": "pk",
    "Poland": "pl",
    "Saint Pierre and Miquelon": "pm",
    "Pitcairn Islands": "pn",
    "Puerto Rico": "pr",
    "Palestinian Territory": "ps",
    "Portugal": "pt",
    "Palau": "pw",
    "Paraguay": "py",
    "Qatar": "qa",
    "Reunion": "re",
    "Romania": "ro",
    "Serbia": "rs",
    "Russia": "ru",
    "Rwanda": "rw",
    "Saudi Arabia": "sa",
    "Solomon Islands": "sb",
    "Seychelles": "sc",
    "Sudan": "sd",
    "Sweden": "se",
    "Singapore": "sg",
    "Saint Helena": "sh",
    "Slovenia": "si",
    "Svalbard and Jan Mayen": "sj",
    "Slovakia": "sk",
    "Sierra Leone": "sl",
    "San Marino": "sm",
    "Senegal": "sn",
    "Somalia": "so",
    "Suriname": "sr",
    "South Sudan": "ss",
    "São Tomé and Príncipe": "st",
    "El Salvador": "sv",
    "Syrian Arab Republic": "sy",
    "Swaziland": "sz",
    "Turks and Caicos Islands": "tc",
    "Chad": "td",
    "French Southern Territories": "tf",
    "Togo": "tg",
    "Thailand": "th",
    "Tajikistan": "tj",
    "Tokelau": "tk",
    "East Timor": "tl",
    "Turkmenistan": "tm",
    "Tunisia": "tn",
    "Tonga": "to",
    "Turkey": "tr",
    "Trinidad and Tobago": "tt",
    "Tuvalu": "tv",
    "Taiwan": "tw",
    "United Republic of Tanzania": "tz",
    "Ukraine": "ua",
    "Uganda": "ug",
    "United States Minor Outlying Islands": "um",
    "United States": "us",
    "Uruguay": "uy",
    "Uzbekistan": "uz",
    "Vatican City": "va",
    "Saint Vincent and the Grenadines": "vc",
    "Venezuela": "ve",
    "British Virgin Islands": "vg",
    "United States Virgin Islands": "vi",
    "Vietnam": "vn",
    "Vanuatu": "vu",
    "Wallis and Futuna": "wf",
    "Samoa": "ws",
    "Unknown": "xz",
    "Yemen": "ye",
    "Mayotte": "yt",
    "South Africa": "za",
    "Zambia": "zm",
    "Zimbabwe": "zw"
}



# Funkce pro aktualizaci torrc
# File to store the filepath
CONFIG_FILE = "config.json"

# Default filepath
DEFAULT_FILEPATH = "Browser//TorBrowser//Data//Tor//torrc"

# Function to load the filepath from config file
def load_filepath():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get("filepath", DEFAULT_FILEPATH)
    return DEFAULT_FILEPATH

# Function to save the filepath to config file
def save_filepath(new_filepath):
    with open(CONFIG_FILE, "w") as file:
        json.dump({"filepath": new_filepath}, file)

# Function to update the torrc file
def update_torrc():
    filepath = load_filepath()  # Load the filepath from the config file
    
    try:
        # Check if the file exists
        if not os.path.exists(filepath):
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            messagebox.showerror("Error", f"File 'torrc' not found at path: {filepath}")
            
            # Ask the user to input a new path
            new_filepath = simpledialog.askstring(
                "New Path", "File 'torrc' not found. Enter the correct path:\n"
                "Example: Browser//TorBrowser//Data//Tor//torrc \t\t\t"
            )
            
            if not new_filepath:
                messagebox.showwarning("Warning", "No path was added. Action terminated.")
                return
            
            # Save the new filepath to the config file
            save_filepath(new_filepath)
            messagebox.showinfo("Success", "Filepath updated!")
            filepath = new_filepath  # Update the variable for further use

        # Update the torrc file content
        countries_str = ",".join(f"{{{country}}}" for country in selected_countries)
        new_exit_nodes_line = f"ExitNodes {countries_str} StrictNodes 1\n"
        
        # Read the existing content of torrc
        with open(filepath, "r") as file:
            lines = file.readlines()
        
        # Update or add the ExitNodes line
        found_exit_nodes = False
        for i in range(len(lines)):
            if lines[i].startswith("ExitNodes"):
                lines[i] = new_exit_nodes_line
                found_exit_nodes = True
                break
        
        if not found_exit_nodes:
            lines.append(new_exit_nodes_line)  # Append new line if not found
        
        # Save the updated content back to the file
        with open(filepath, "w") as file:
            file.writelines(lines)
        
        messagebox.showinfo("Success", f"File 'torrc' updated: {new_exit_nodes_line.strip()}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Funkce pro přidání země
def add_country(country_display_name):
    if country_display_name == "Any":
        # Přidáme Any země
        for country_code in country_mapping.values():
            if country_code not in selected_countries:
                selected_countries.append(country_code)
    else:
        selected_country = country_mapping[country_display_name]
        if selected_country not in selected_countries:
            selected_countries.append(selected_country)
    
    update_selected_countries_display()

# Funkce pro odebrání země
def remove_country(country):
    if country in selected_countries:
        selected_countries.remove(country)
        update_selected_countries_display()

# Funkce pro vymazání aktuálního výběru
def clear_selection():
    selected_countries.clear()
    update_selected_countries_display()

# Funkce pro aktualizaci zobrazení vybraných zemí
def update_selected_countries_display():
    for widget in selected_countries_frame.winfo_children():
        widget.destroy()
    
    for country in selected_countries:
        display_name = [k for k, v in country_mapping.items() if v == country][0]
        btn = tk.Button(selected_countries_frame, text=display_name,
                        command=lambda c=country: remove_country(c))
        btn.pack(side="left", padx=5)

# Funkce pro filtrování zemí podle vstupu uživatele
def filter_countries(*args):
    search_term = search_var.get().lower()
    filtered_countries = [name for name in country_mapping.keys() if name.lower().startswith(search_term)]
    if "Any".startswith(search_term):  # Přidáme možnost "Any" do filtru
        filtered_countries.insert(0, "Any")

    listbox.delete(0, tk.END)  # Vymazat staré možnosti
    for country in filtered_countries:
        listbox.insert(tk.END, country)  # Přidat nové filtrované možnosti

# Funkce pro výběr země ze seznamu
def select_country(event):
    selected_country = listbox.get(listbox.curselection())
    add_country(selected_country)

# GUI
root = tk.Tk()
root.title("Torrc Editor")
root.maxsize(800, 600)  # Maximální šířka a výška
root.minsize(300, 300)  # Minimální šířka a výška

# Vyhledávací pole
tk.Label(root, text="Find countries:").pack(pady=10)
search_var = tk.StringVar()
search_var.trace("w", filter_countries)
entry = tk.Entry(root, textvariable=search_var, width=30)
entry.pack()

# Listbox s přidaným scrollbar
listbox_frame = tk.Frame(root)
listbox_frame.pack()
listbox_scrollbar = tk.Scrollbar(listbox_frame)
listbox_scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(listbox_frame, height=6, yscrollcommand=listbox_scrollbar.set, width=30)
listbox.pack(side="left")
listbox_scrollbar.config(command=listbox.yview)

listbox.bind("<<ListboxSelect>>", select_country)

# Naplnění listboxu všemi zeměmi při spuštění
listbox.insert(tk.END, "Any")  # Přidáme možnost "Any"
for country in country_mapping.keys():
    listbox.insert(tk.END, country)

# Rámeček pro zobrazení vybraných zemí
selected_countries_frame = tk.Frame(root)
selected_countries_frame.pack(pady=10)
selected_countries = []

# Tlačítka pro "Uložit" a "Vymazat"
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)
tk.Button(btn_frame, text="Save", command=update_torrc).pack(side="left", padx=10)
tk.Button(btn_frame, text="Delete all countries", command=clear_selection).pack(side="left", padx=10)

# Hlavní smyčka
root.mainloop()



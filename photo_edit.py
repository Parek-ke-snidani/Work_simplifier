import cv2
import numpy as np
import os
from realesrgan import RealESRGAN
from sklearn.cluster import KMeans

# --- Složky ---
input_folder = "fotky"
output_folder = "upravené"
os.makedirs(output_folder, exist_ok=True)

# --- Inicializace Real-ESRGAN ---
device = 'cuda'  # nebo 'cpu'
model = RealESRGAN(device, scale=2)
model.load_weights('RealESRGAN_x2.pth')

# --- Funkce pro odhad typu scény podle dominantní barvy ---
def detect_scene(image):
    # Zmenšení fotky pro rychlejší výpočet
    img_small = cv2.resize(image, (100, 100))
    img_rgb = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
    pixels = img_rgb.reshape(-1, 3)

    # KMeans pro dominantní barvu
    kmeans = KMeans(n_clusters=3, random_state=42).fit(pixels)
    colors = kmeans.cluster_centers_

    # jednoduché pravidlo podle dominantní barvy
    avg_color = np.mean(colors, axis=0)
    r, g, b = avg_color

    if b > 150 and g > 150:  # jasné modré a zelené → pláž / moře
        return "beach"
    elif r > 150 and g < 120 and b < 120:  # červené tóny → západ slunce
        return "sunset"
    elif g > 120 and b < 120:  # hodně zelené → hory / příroda
        return "nature"
    else:
        return "indoor"

# --- Automatická úprava fotky podle scény ---
def auto_adjust(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    # --- Redukce šumu pro tmavé fotky ---
    if brightness < 100:
        image = cv2.fastNlMeansDenoisingColored(image, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)

    # --- Úprava kontrastu a jasu ---
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)

    # --- Typ scény ---
    scene = detect_scene(image)

    # Nastavení parametrů podle scény
    if scene == "beach":
        l = cv2.convertScaleAbs(l, alpha=1.1, beta=10)
        s_scale = 1.2
    elif scene == "sunset":
        l = cv2.convertScaleAbs(l, alpha=1.2, beta=20)
        s_scale = 1.3
    elif scene == "nature":
        l = cv2.convertScaleAbs(l, alpha=1.1, beta=15)
        s_scale = 1.2
    else:  # indoor
        l = cv2.convertScaleAbs(l, alpha=1.05, beta=10)
        s_scale = 1.1

    # Globální úprava jasu pro extrémně tmavé nebo světlé fotky
    if brightness < 80:
        l = cv2.convertScaleAbs(l, alpha=1.2, beta=30)
    elif brightness > 200:
        l = cv2.convertScaleAbs(l, alpha=0.9, beta=-20)

    lab = cv2.merge((l, a, b))
    adjusted = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # --- Doostření pokud je rozmazaná ---
    laplacian_var = cv2.Laplacian(cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
    if laplacian_var < 100:
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        adjusted = cv2.filter2D(adjusted, -1, kernel)

    # --- Zvýšení saturace podle scény ---
    hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.multiply(s, s_scale)
    hsv = cv2.merge([h, s, v])
    adjusted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return adjusted

# --- Zpracování všech fotek ---
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(input_folder, filename)
        img = cv2.imread(path)

        # Automatická úprava
        img_adjusted = auto_adjust(img)

        # Real-ESRGAN jen pro nízké rozlišení
        h, w = img_adjusted.shape[:2]
        if h < 1000 or w < 1000:
            img_final = model.predict(img_adjusted)
        else:
            img_final = img_adjusted

        # Uložení výsledku
        out_path = os.path.join(output_folder, filename)
        cv2.imwrite(out_path, img_final)

        print(f"Upraveno ({detect_scene(img)}): {filename}")

print("Hotovo! Všechny fotky byly automaticky optimalizovány podle typu scény.")

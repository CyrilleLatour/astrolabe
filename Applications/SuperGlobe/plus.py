import json
import os

# === 1️⃣ Localisation du fichier source ===
path = os.path.join(os.path.dirname(__file__), "countries.json")

if not os.path.exists(path):
    print("❌ Fichier 'countries.json' introuvable :", path)
    exit()

# === 2️⃣ Lecture sécurisée du fichier JSON ===
with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read().strip()
    if not content:
        print("❌ Le fichier 'countries.json' est vide.")
        exit()
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print("❌ Erreur JSON :", e)
        exit()

# === 3️⃣ Extraction des pays, capitales et coordonnées ===
capitals = []
for country in data:
    try:
        name = country["name"]["common"]
        capital_list = country.get("capital", [])
        capital = capital_list[0] if capital_list else None
        latlng = country.get("latlng", [None, None])
        lat, lon = latlng if len(latlng) == 2 else (None, None)

        if capital and lat is not None and lon is not None:
            capitals.append({
                "country": name,
                "capital": capital,
                "lat": lat,
                "lon": lon
            })

    except Exception as e:
        print(f"⚠️  Erreur sur {country.get('name', {}).get('common', '?')} : {e}")

# === 4️⃣ Tri alphabétique des pays ===
capitals.sort(key=lambda x: x["country"].lower())

# === 5️⃣ Sauvegarde du fichier résultant ===
output_path = os.path.join(os.path.dirname(__file__), "countries_OK.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(capitals, f, ensure_ascii=False, indent=2)

print(f"✅ Fichier '{os.path.basename(output_path)}' généré avec succès "
      f"({len(capitals)} capitales enregistrées, triées par ordre alphabétique).")

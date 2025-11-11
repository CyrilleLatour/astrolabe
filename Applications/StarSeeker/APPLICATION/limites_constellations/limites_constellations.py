import json
import os

# Obtenir le chemin absolu vers ce script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin absolu vers le GeoJSON
geojson_path = os.path.join(script_dir, 'constellations_bounds.geojson')

with open(geojson_path, 'r', encoding='utf-8') as f:
    geojson = json.load(f)

result = []

for feature in geojson['features']:
    nom = feature['properties'].get('name', 'Inconnue')
    geometry = feature['geometry']
    polygons = []

    if geometry['type'] == 'Polygon':
        polygons.append(geometry['coordinates'])
    elif geometry['type'] == 'MultiPolygon':
        polygons.extend(geometry['coordinates'])
    else:
        continue

    result.append({
        'nom': nom,
        'polygones': polygons
    })

# Chemin absolu pour la sortie
output_path = os.path.join(script_dir, 'constellations_polygons.json')

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Extraction terminée. Fichier créé : {output_path}")

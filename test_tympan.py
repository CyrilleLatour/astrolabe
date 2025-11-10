from tympan.almucantarats.almucantarats import Almucantarats

rayon = 7
latitude = 45

alm = Almucantarats(rayon, latitude)
data = alm.get_data()

print(f"Nombre d'almucantarats : {len(data['almucantarats'])}")
for cercle in data['almucantarats'][:5]:
    print(f"Z={cercle['Z']} | rayon={cercle['rayon']:.4f} | cy={cercle['cy']:.4f}")
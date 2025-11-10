import math
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
from tympan.almucantarats.almucantarats import Almucantarats


# ================================================================
# 🟨 CLASSE CREPUSCULES – calculs des cercles extrapolés et solstices
# ================================================================

class Crepuscules:
    def __init__(self, rayon_equateur, latitude, facteur=1):
        self.rayon_equateur = float(rayon_equateur)
        self.latitude = float(latitude)
        self.latitude_rad = math.radians(latitude)
        self.S = self.rayon_equateur / 2
        self.facteur = facteur
        self.obliquite = 23.44
        self.obliquite_rad = math.radians(self.obliquite)

        print(f"[INIT] Crépuscules → rayon={self.rayon_equateur}, latitude={self.latitude}°")

    # ----------------------------------------------------------------
    # 🔹 CALCUL DES AZIMUTS DU SOLEIL AUX SOLSTICES
    # ----------------------------------------------------------------
    def calculer_azimut_solstice(self, declinaison):
        declinaison_rad = math.radians(declinaison)
        try:
            cos_azimut = math.sin(declinaison_rad) / math.cos(self.latitude_rad)
            if not -1 <= cos_azimut <= 1:
                print("⚠️ Soleil circumpolaire, pas d'azimut")
                return None
            azimut_rad = math.acos(cos_azimut)
            azimut_deg = math.degrees(azimut_rad)
            azimut_lever = 360 - azimut_deg
            print(f"[AZIMUT] Déclinaison {declinaison:+.2f}° → {azimut_lever:.2f}°")
            return azimut_lever
        except ZeroDivisionError:
            if abs(self.latitude) < 0.001:
                return 360 - (90 + declinaison)
            return None

    # ----------------------------------------------------------------
    # 🔹 CALCUL DES CERCLES AUX SOLSTICES
    # ----------------------------------------------------------------
    def calculer_cercle_solstice(self, declinaison, couleur):
        azimut = self.calculer_azimut_solstice(declinaison)
        if azimut is None:
            return None

        L = self.latitude_rad
        S = self.S
        NP = 2 * S * math.tan(math.radians((90 - math.degrees(L)) / 2))
        NK = 2 * S / math.cos(L)
        ycentre = NP - NK
        alpha_rad = math.radians(azimut)
        try:
            xcentre = 2 * S / (math.cos(L) * math.tan(alpha_rad))
            rayon = 2 * S / (math.cos(L) * math.sin(alpha_rad))

            print(f"[SOLSTICE] Decl={declinaison:+.2f}° centre=({xcentre:.3f},{ycentre:.3f}) r={rayon:.3f}")
            points = []
            for theta in range(0, 361):
                theta_rad = math.radians(theta)
                x = xcentre + rayon * math.cos(theta_rad)
                y = ycentre + rayon * math.sin(theta_rad)
                points.append((x, y))
            return {
                'declinaison': declinaison,
                'points': points,
                'centre_x': xcentre,
                'centre_y': ycentre,
                'rayon': rayon,
                'color': couleur,
                'stroke_width': 2.5
            }
        except ZeroDivisionError:
            return None

    def get_cercles_solstices(self):
        """Retourne les deux cercles des solstices (été et hiver)"""
        cercles = []
        cercle_hiver = self.calculer_cercle_solstice(-self.obliquite, "black")
        cercle_ete = self.calculer_cercle_solstice(+self.obliquite, "orange")
        if cercle_hiver:
            cercles.append(cercle_hiver)
        if cercle_ete:
            cercles.append(cercle_ete)
        return cercles

    # ----------------------------------------------------------------
    # 🔹 CALCUL DES CERCLES DE CRÉPUSCULES
    # ----------------------------------------------------------------
    def extrapoler_crepuscules(self):
        alm = Almucantarats(self.rayon_equateur, self.latitude)
        resultats = []
        cercles_crepuscules = []

        print("\n===== CALCUL DES CRÉPUSCULES =====")

        Z_crepuscules = [-6, -12, -18]

        # Étape 1 : vérifier quels cercles sont calculables
        cercles_calcules = {}
        for Z in Z_crepuscules:
            cercle = alm.calculer_almucantarat(Z)
            if cercle and cercle.get("type") != "ligne_horizontale":
                cercles_calcules[Z] = True
                print(f"✅ Cercle Z={Z}° est calculable directement")
            else:
                print(f"🔴 Cercle Z={Z}° doit être extrapolé")

        # Étape 2 : extrapolation polynomiale UNIQUEMENT pour les cercles NON calculables
        Z_a_extrapoler = [z for z in Z_crepuscules if z not in cercles_calcules]
        
        if Z_a_extrapoler:
            print(f"📊 Cercles à extrapoler: {Z_a_extrapoler}")
            
            for Z in range(0, 71):
                cercle = alm.calculer_almucantarat(Z)
                if cercle and cercle.get("type") != "ligne_horizontale":
                    y_cartesien = cercle["cy"] - cercle["rayon"]
                    resultats.append((Z, y_cartesien))

            if len(resultats) >= 5:
                df = pd.DataFrame(resultats, columns=["Z", "y_cartesien"])
                X = df[["Z"]]
                y = df["y_cartesien"]

                meilleur_modele = None
                for deg in range(1, min(15, len(resultats))):
                    model = make_pipeline(PolynomialFeatures(deg), LinearRegression())
                    model.fit(X, y)
                    y_pred = model.predict(X)
                    r2 = r2_score(y, y_pred)
                    if r2 >= 0.999999:
                        meilleur_modele = model
                        print(f"🎯 Modèle polynomial degré {deg} → R²={r2:.6f}")
                        break
                if meilleur_modele is None:
                    deg = min(6, len(resultats) - 1)
                    meilleur_modele = make_pipeline(PolynomialFeatures(deg), LinearRegression())
                    meilleur_modele.fit(X, y)
                    print(f"ℹ️ Modèle degré {deg} (R² < 1) retenu")

                for Z in Z_a_extrapoler:
                    y_ext = meilleur_modele.predict(pd.DataFrame({"Z": [Z]}))[0]
                    S = self.rayon_equateur / 2
                    L = math.radians(self.latitude)
                    A_B = math.radians((180 - self.latitude - Z) / 2)
                    A_C = math.radians((Z - self.latitude) / 2)
                    B = 2 * S * math.tan(A_B)
                    C = 2 * S * math.tan(A_C)
                    R_alm = (B - C) / 2
                    y_centre_alm = B - R_alm
                    y_calc = y_centre_alm - R_alm
                    if abs(y_calc - y_ext) > 0.001:
                        R_alm = y_centre_alm - y_ext

                    # Vérifier si le rayon est extrêmement grand (cercle → droite)
                    if abs(R_alm) > 1000:
                        # Droite horizontale rouge
                        cercles_crepuscules.append({
                            'type': 'ligne_horizontale',
                            'y_offset': y_ext,
                            'hauteur': Z,
                            'style': {
                                'stroke': 'red',
                                'stroke_width': 1,
                                'stroke_opacity': 0.7
                            }
                        })
                        print(f"🔴 Extrapolé Z={Z}° → DROITE HORIZONTALE à y={y_ext:.3f}")
                    else:
                        cercles_crepuscules.append({
                            'cx': 0,
                            'cy': y_centre_alm,
                            'rayon': abs(R_alm),
                            'hauteur': Z,
                            'style': {'fill': 'none', 'stroke': 'red', 'stroke_width': 1, 'stroke_opacity': 0.7}
                        })
                        print(f"🔴 Extrapolé Z={Z}° → cy={y_centre_alm:.3f}, r={abs(R_alm):.3f}")
        else:
            print("✅ Tous les cercles crépusculaires sont calculables directement (gérés dans views.py)")

        if cercles_crepuscules:
            print(f"\n>>> CRÉPUSCULES EXTRAPOLÉS À {self.latitude}° :")
            for c in cercles_crepuscules:
                if c.get('type') == 'ligne_horizontale':
                    print(f"   Z={c['hauteur']}° | DROITE y={c['y_offset']:.3f} | {c['style']['stroke']}")
                else:
                    print(f"   Z={c['hauteur']}° | cy={c['cy']:.3f} | r={c['rayon']:.3f} | {c['style']['stroke']}")
            print("====================================\n")
        else:
            print(f"\n>>> Aucun cercle crépusculaire à extrapoler à {self.latitude}°\n")

        return cercles_crepuscules

    # ----------------------------------------------------------------
    # 🔹 COMBINAISON TOTALE – solstices + crépuscules
    # ----------------------------------------------------------------
    def get_data(self):
        cercles_solstices = self.get_cercles_solstices()
        cercles_crepuscules = self.extrapoler_crepuscules()

        print(f"[DATA] Total cercles solstices: {len(cercles_solstices)}, crépuscules extrapolés: {len(cercles_crepuscules)}")

        return {
            "cercles_solstices": cercles_solstices,
            "cercles_crepuscules": cercles_crepuscules
        }
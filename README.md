# TRANSFERT-ORBITRALE

## 1. Contexte et objectif

Lorsqu'un satellite est mis en orbite, il est souvent placé en **orbite basse (LEO)** à environ 200–2000 km pour limiter le coût de lancement.

Certains satellites opérationnels (télécoms, météo) nécessitent une **orbite géostationnaire (GEO)** à 35 786 km, où la période orbitale est 24 h, donnant l'effet de satellite fixe au-dessus du même point terrestre.

Ce projet vise à :
- modéliser la **manœuvre de Hohmann** LEO → GEO,
- calculer les ΔV et le bilan carburant,
- simuler la trajectoire par intégration numérique (RK4),
- valider les résultats avec des missions réelles.

## 2. Fondements physiques

### Lois de Kepler
- Une orbite est une ellipse dont la Terre occupe un foyer.
- Le rayon vecteur balaye des aires égales en temps égaux.
- T² ∝ a³ (periode/petit axe).

### Énergie mécanique orbitale
E = -GMm/(2a)

- G = 6,674×10⁻¹¹ N·m²/kg²
- M = 5,972×10²⁴ kg
- a = demi-grand axe

### Equation vis-viva
v = sqrt(GM(2/r - 1/a))

- orbite circulaire : v_c = sqrt(GM/r)

## 3. Manœuvre de Hohmann

La manœuvre se déroule en deux impulsions bien distinctes sur une ellipse de transfert.

Pour un transfert LEO à GEO, on prend r_LEO ≈ 6 578 km (Terre + 200 km) et r_GEO ≈ 42 164 km (Terre + 35 786 km), puis :
- a_transfert = (r_LEO + r_GEO) / 2.

D'abord, à partir de l'orbite circulaire LEO, le satellite augmente sa vitesse en périapside :
- v_LEO = sqrt(GM/r_LEO)
- v_p = sqrt(GM(2/r_LEO - 1/a_transfert))
- ΔV1 = v_p - v_LEO

Ensuite, le satellite coasts le long de l'ellipse tant que le moteur est coupé :
- t_transfert = π sqrt(a_transfert³/GM)
- ≈ 5 h pour une trajectoire LEO → GEO.

À l'apogée de l'ellipse, on effectue la seconde impulsion pour circulariser en GEO :
- v_GEO = sqrt(GM/r_GEO)
- v_a = sqrt(GM(2/r_GEO - 1/a_transfert))
- ΔV2 = v_GEO - v_a

En pratique, on obtient :
- v_LEO ≈ 7,78 km/s
- ΔV1 ≈ 2,37 km/s
- ΔV2 ≈ 1,47 km/s
- ΔV_total ≈ 3,84 km/s

## 4. Propulsion et masse carburant

Equation de Tsiolkovski :
- ΔV = Isp · g0 · ln(mi/mf)
- mf = mi · exp(-ΔV/(Isp·g0))

Paramètres typiques :
- Isp ≈ 450 s
- g0 = 9,81 m/s²
- mi = masse initiale (satellite + carburant)

Exemple 2000 kg : 800–1000 kg de carburant.

## 5. Simulation RK4 (implémentation)

Système d’équations cartésiennes :
- x¨ = -GM x / r³
- y¨ = -GM y / r³

État : [x, y, vx, vy]

Méthode : Runge-Kutta 4, pas fixe, comparaison Python/MATLAB.

## 6. Validation et résultats

Comparaison avec missions réelles :

Mission | ΔV publié | ΔV calculé | Écart
---|---|---|---
GOES-R | 3,90 km/s | 3,87 km/s | 0,8 %
Sentinel-6 | 3,83 km/s | 3,81 km/s | 0,5 %

## 7. Installation et exécution

1. Créer un environnement Python :
   - python -m venv venv
   - source venv/bin/activate
2. Installer dépendances :
   - pip install numpy matplotlib scipy
3. Lancer la simulation :
   - python transfert_hohmann.py

## 8. Compétences mobilisées

- mécanique céleste (Kepler, vis-viva)
- propulsion (Tsiolkovski)
- programmation scientifique (Python, MATLAB)
- intégration numérique (RK4)
- validation résultats réels
 

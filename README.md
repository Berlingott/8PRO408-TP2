8PRO408 - Outils programmation pour la science des données
Second travail pratique: Séries temporelles

Réalisé par:
    CLAUS Simon CLAS13020304
    DUCHESNE Simon DUCS20069507
    DUFOUR Vincent DUFV12080004
    DU PAUL Véronique DUPV05518306
    LAPRISE David LAPD17050101
    MONARQUE Vincent MONV15099405
    MORIN Gilles-Philippe MORG27109707
    PLOURDE Louis-Gabriel PLOL24110001

Voici les étapes à réaliser en ordre.

Dans le dossier de téléchargement:
    1.  a) Exécuter scraper.py (le téléchargement peut être long)
        b) Extraire toutes les archives. Par exemple, avec 7zip:
            7zip.exe x *.tgz
            7zip.exe x *.tar
            del *.tgz
            del *.tar
    2. Exécuter counter.py
        a) Rouler le premier Monte-Carlo pour déterminer le nombre minimal de phrases à extraire
        b) Avec ce nombre comme variable 'number_of_sentences', trouver le meilleur sous-ensemble
        c) Copier les dossiers des personnes faisant partie de ce sous-ensemble

Dans le dossier du projet:
    3. Coller les dossiers précédents dans RawData
    4. Exécuter csvGeneration.py
    5. Exécuter main.py et conséquemment featureExtraction.py
        - Changer la fenêtre et le chevauchement au besoin
    6. Exécuter dimentionalityReduction.py

Si on veut tester des données de façon isolée, le premier dossier de CleanData (/CleanData/a0007/) contient:
    - graph.py, pour afficher les pressions acoustiques d'un fichier audio donné.
    - fourier.py, pour afficher le spectre de fréquences d'un fichier audio donné.
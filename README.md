8PRO408 - Outils programmation pour la science des données
Second travail pratique: Séries temporelles

# Projet de fin de session
## Programme d'analyse et de reconnaissance vocal
<p align="center">

![uqac](./readmedata/uqac527x316_transparent.png)

</p>

### Réaliser par

<p align="center">

Claus, Simon  
Duchesne, Simon   
Dufour, Vincent  
Du Paul, Véronique  
Laprise, David   
Monarque, Vincent  
Morin, Gilles-Philippe  
Plourde, Louis-Gabriel

</p>


## Guide d'utilisation
### Dans le dossier de téléchargement:  
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

### Dans le dossier du projet:  
    3. Coller les dossiers précédents dans RawData  
    4. Exécuter csvGeneration.py  
    5. Exécuter main.py et conséquemment featureExtraction.py  
        - Changer la fenêtre et le chevauchement au besoin  
    6. Exécuter dimentionalityReduction.py  

Si on veut tester des données de façon isolée, le premier dossier de CleanData (/CleanData/a0007/) contient:  
    - graph.py, pour afficher les pressions acoustiques d'un fichier audio donné.  
    - fourier.py, pour afficher le spectre de fréquences d'un fichier audio donné.  
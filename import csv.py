import csv
from datetime import datetime, timedelta

# Liste fictive d'équipes de championnat
equipes = ["Équipe A", "Équipe B", "Équipe C", "Équipe D", "Équipe E", "Équipe F"]

# Création d'un fichier CSV pour enregistrer les matchs
with open('calendrier_championnat.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Écriture de l'en-tête CSV
    writer.writerow(['Date', 'Équipe à domicile', 'Équipe à l\'extérieur'])

    # Définition de la date de début du championnat
    date_debut = datetime(2023, 9, 1)  # Par exemple, le 1er septembre 2023

    # Durée du championnat en jours (par exemple, 40 jours)
    duree_championnat = timedelta(days=40)

    # Fréquence des matchs (un match chaque samedi et dimanche)
    frequence_matchs = timedelta(days=1)

    # Initialisation du compteur de matchs
    compteur_matchs = 1

    # Boucle pour générer les matchs
    while date_debut < (datetime(2023, 9, 1) + duree_championnat):
        # Assurez-vous que le jour est un samedi ou un dimanche (pour les matchs de week-end)
        if date_debut.weekday() in [5, 6]:  # 5 correspond à samedi, 6 correspond à dimanche
            equipe_domicile, equipe_exterieur = equipes[compteur_matchs % len(equipes)], \
                                                 equipes[(compteur_matchs + 1) % len(equipes)]

            # Écrire la date et les équipes dans le fichier CSV
            writer.writerow([date_debut.strftime('%Y-%m-%d'), equipe_domicile, equipe_exterieur])

            # Incrémenter le compteur de matchs
            compteur_matchs += 2  # Chaque week-end, deux équipes jouent deux matchs différents

        # Passage au jour suivant
        date_debut += frequence_matchs

print("Calendrier du championnat généré avec succès dans le fichier 'calendrier_championnat.csv'.")

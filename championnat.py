from team import generate_team
import pandas as pd
import numpy as np
import random
import itertools
from match import simulate_match
from datetime import datetime, timedelta

# Liste des noms d'équipes
team_names = [
    "Arsenal FC", "Aston Villa", "AFC Bournemouth", "Brentford FC", "Brighton & Hove Albion",
    "Burnley FC", "Chelsea FC", "Crystal Palace", "Everton FC", "Fulham FC",
    "Liverpool FC", "Luton Town FC", "Manchester City", "Manchester United", "Newcastle United",
    "Nottingham Forest", "Sheffield United FC", "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers"
]

teams = []
# Création des équipes
for name in team_names:
    generate_team(name)

# Création du calendrier de la Premier League
fixtures = []
rounds = range(1, 39)
matches_per_round = len(team_names) // 2

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
            equipe_domicile, equipe_exterieur = team_names[compteur_matchs % len(equipes)], \
                                                 team_names[(compteur_matchs + 1) % len(equipes)]

            # Écrire la date et les équipes dans le fichier CSV
            writer.writerow([date_debut.strftime('%Y-%m-%d'), equipe_domicile, equipe_exterieur])

            # Incrémenter le compteur de matchs
            compteur_matchs += 2  # Chaque week-end, deux équipes jouent deux matchs différents

        # Passage au jour suivant
        date_debut += frequence_matchs

print("Calendrier du championnat généré avec succès dans le fichier 'calendrier_championnat.csv'.")

for round_num in rounds:
    matches = []
    for i in range(matches_per_round):
        home_team = team_names[i]
        away_team = team_names[-(i+1)]
        matches.append((home_team, away_team))
    fixtures.append(matches)
    team_names.insert(1, team_names.pop())

# Création du DataFrame pour le calendrier
matchday = []
home_teams = []
away_teams = []

for i, match_round in enumerate(fixtures, start=1):
    for match in match_round:
        matchday.append(i)
        home_teams.append(match[0])
        away_teams.append(match[1])

calendar_df = pd.DataFrame({"Matchday": matchday, "Home Team": home_teams, "Away Team": away_teams})
calendar_df.to_csv(r"C:\Users\pierr\PycharmProjects\Mercato\data\calendar.csv", index=False)

standings = pd.DataFrame({"Team": team_names,
                          "Points": 0,
                          "Wins": 0,
                          "Draws": 0,
                          "Losses": 0,
                          "Goals For": 0,
                          "Goals Against": 0,
                          "Goal Difference": 0,
                          "Défenseurs":0,
                          "Milieux":0,
                          "Attaquants":0})


for matchday in range(1, 39):
    matches = fixtures[matchday - 1]
    for home_team, away_team in matches:
        goals_home, goals_away = simulate_match(home_team, away_team)
        home_goals_for = standings.loc[standings["Team"] == home_team, "Goals For"].item()
        home_goals_against = standings.loc[standings["Team"] == home_team, "Goals Against"].item()
        home_goals_for += goals_home
        home_goals_against += goals_away
        
        away_goals_for = standings.loc[standings["Team"] == away_team, "Goals For"].item()
        away_goals_against = standings.loc[standings["Team"] == away_team, "Goals Against"].item()
        away_goals_for += goals_away
        away_goals_against += goals_home
        
        standings.loc[standings["Team"] == home_team, "Goals For"] = home_goals_for
        standings.loc[standings["Team"] == home_team, "Goals Against"] = home_goals_against
        standings.loc[standings["Team"] == away_team, "Goals For"] = away_goals_for
        standings.loc[standings["Team"] == away_team, "Goals Against"] = away_goals_against
        
        if goals_home > goals_away:
            standings.loc[standings["Team"] == home_team, "Points"] += 3
            standings.loc[standings["Team"] == home_team, "Wins"] += 1
            standings.loc[standings["Team"] == away_team, "Losses"] += 1
        elif goals_home < goals_away:
            standings.loc[standings["Team"] == away_team, "Points"] += 3
            standings.loc[standings["Team"] == away_team, "Wins"] += 1
            standings.loc[standings["Team"] == home_team, "Losses"] += 1
        else:
            standings.loc[standings["Team"] == home_team, "Points"] += 1
            standings.loc[standings["Team"] == home_team, "Draws"] += 1
            standings.loc[standings["Team"] == away_team, "Points"] += 1
            standings.loc[standings["Team"] == away_team, "Draws"] += 1
    
    standings = standings.sort_values(by=["Points", "Goal Difference", "Goals For"], ascending=False)
    
    # Enregistrement du classement après chaque journée dans le fichier classement.csv
    standings_df = standings.reset_index(drop=True)
    standings_df.index += 1
    standings_df.to_csv(r"C:\Users\pierr\PycharmProjects\Mercato\data\calendar.csv", index_label="Position")

print(standings)
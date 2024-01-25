import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import cvxpy as cp
import numpy as np
import csv
import os
from scipy.stats import truncnorm
from math import trunc
import math

# Liste des pays disponibles
countries = ['belgium', 'france', 'germany', 'italy', 'spain']
data = {}
number_of_players = 20

def get_random_forename(url, csv_file):
    if not os.path.exists(csv_file):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url, headers=headers).text
        doc = BeautifulSoup(response, "html.parser")
        my_table = doc.find("table", class_="forename-table")
        td_tags = my_table.find_all('tr')
        names = []
        for elem in td_tags:
            div_element = elem.find("div", class_="m full")
            a_links = elem.find_all("a")
            if div_element is not None and div_element.text == "100%":
                for i in a_links:
                    names.append(i.string)
        
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for i in names:
                writer.writerow([i])

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        names = [row[0] for row in reader]

    return random.choice(names)

def get_random_surname(url, csv_file):
    if not os.path.exists(csv_file):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url, headers=headers).text
        doc = BeautifulSoup(response, "html.parser")
        my_table = doc.find("table", class_="forename-table")
        td_tags = my_table.find_all('tr')
        names = []
        for elem in td_tags:
            a_links = elem.find_all("a")
            for i in a_links:
                names.append(i.string)
        
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in names:
                writer.writerow([i])
    # Lecture des noms de famille à partir du fichier CSV
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file) 
        names = [row[0] for row in reader]
    return random.choice(names)

# Fonction pour générer une statistique aléatoire en respectant les contraintes
def generate_statistic(age):
    mean = 75
    std_dev = 10
    min_value = 55
    max_value = 95

    # Génération de la note selon une distribution gaussienne
    note = random.gauss(mean, std_dev)

    # Limiter la note dans la plage [min_value, max_value]
    note = max(min_value, min(max_value, note))

    # Facteur de pondération basé sur l'âge
    weight = math.exp(-0.125 * ((age - 24) / 4) ** 2) 

    # Appliquer le facteur de pondération
    weighted_note = note * weight

    return round(weighted_note)

def generate_sec(primary_stat):
    std_dev = 10
    max_diff = 20

    # Génération de la différence selon une distribution gaussienne semi-tronquée
    diff = random.gauss(10, std_dev)
    diff = max(0, min(max_diff, diff))  # Tronquer les valeurs négatives à 0 et les valeurs supérieures à max_diff

    # Calcul de la statistique secondaire de manière logarithmique
    secondary_stat = max(0, primary_stat - diff)

    return round(secondary_stat)

# Fonction pour générer un joueur
def generate_player():
    # Choix aléatoire de la nationalité
    nationality = random.choice(countries)

    # Obtention du nom et prénom aléatoires
    forename_url = f"https://forebears.io/{nationality}/forenames"
    surname_url = f"https://forebears.io/{nationality}/surnames"
    forename = get_random_forename(forename_url, r"c:\Users\pierr\PycharmProjects\Mercato\forenames\{}_forenames.csv".format(nationality))
    surname = get_random_surname(surname_url,r"c:\Users\pierr\PycharmProjects\Mercato\surnames\{}_surnames.csv".format(nationality))

    # Génération de l'âge selon une distribution gaussienne
    age = int(truncnorm.rvs(-4, 4, loc=24, scale=2))
    #age = random.randint(17,34)
    # Génération des statistiques selon le poste
    positions = ['Gardien', 'Défenseur', 'Milieu', 'Attaquant']

    primary_position = random.choice(positions)
    goal_stat = 0

    if primary_position == 'Attaquant':
        atk_stat = generate_statistic(age)
        mid_stat = generate_sec(atk_stat)
        def_stat = generate_sec(mid_stat)

    elif primary_position == 'Milieu':
        mid_stat = generate_statistic(age)
        secondary_position = random.choice(['Attaquant', 'Défenseur'])
        if secondary_position == 'Attaquant':
            atk_stat = generate_sec(mid_stat)
            def_stat = generate_sec(atk_stat)
        else:
            def_stat = generate_sec(mid_stat)
            atk_stat = generate_sec(def_stat)

    elif primary_position == 'Défenseur':
        def_stat = generate_statistic(age)
        mid_stat = generate_sec(def_stat)
        atk_stat = generate_sec(mid_stat)
    
    elif primary_position == 'Gardien':
        goal_stat = generate_statistic(age)
        atk_stat = 0
        def_stat = 0
        mid_stat = 0

    # Création du joueur
    player = {
        'Numéro': '',
        'Nom': surname.capitalize(),
        'Prénom': forename.capitalize(),
        'Âge': age,
        'Nationalité': nationality.capitalize(),
        'Position': primary_position,
        'GD': goal_stat,
        'DEF': def_stat,
        'MID': mid_stat,
        'ATK': atk_stat,
    }
    return player


players = []

for i in range(number_of_players):
    player = generate_player()
    player['Numéro'] = i + 1
    players.append(player)

# Écriture des joueurs dans le fichier CSV
csv_file = r"C:\Users\pierr\PycharmProjects\Mercato\data\players.csv"

if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=players[0].keys())
        writer.writeheader()
        writer.writerows(players)

# Création du DataFrame à partir du fichier CSV
df = pd.read_csv(csv_file)

# Remplissage de la liste S à partir du DataFrame
S = df[['GD', 'DEF', 'MID', 'ATK']].values.flatten().tolist()
print(len (S))
# Affichage du DataFrame
print(df)

# Affichage de la liste S
print(S)

#génération d'équipe idéale
x = cp.Variable(4*number_of_players, boolean=True, integer=True)  # Variables entières et binaires
objective = cp.Maximize (cp.sum(S @ x))
# Définition des contraintes
constraints = []

# Calcul des équations et ajout des contraintes
eq_1 = cp.sum(x[::4])
eq_2 = cp.sum(x[1::4])
eq_3 = cp.sum(x[3::4])
for i in range(number_of_players):
    eq_4 = x[0+i*4]+x[1+i*4]+x[2+i*4]+x[3+i*4]
    constraints += [eq_4 <= 1]

constraint_1 = eq_1 == 1
constraint_2 = eq_2 >= 1
constraint_3 = eq_2 <= 6
constraint_4 = eq_2 >= 1
constraint_5 = eq_3 <= 4
constraint_sum = cp.sum(x) == 11

constraints += [constraint_1, constraint_2, constraint_3, constraint_4, constraint_5, constraint_sum]
#constraints += [constraint_1]
# Résolution du problème d'optimisation
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.SCIPY, verbose=False)

# Affichage des résultats
print("Statut du problème:", problem.status)
print("Valeur optimale de la fonction objectif:", problem.value)
print("Valeurs optimales des variables:", x.value)


# Lire les données des joueurs à partir du fichier players.csv
players_df = pd.read_csv(r"C:\Users\pierr\PycharmProjects\Mercato\data\players.csv")

# Créer un dictionnaire pour stocker les joueurs utilisés par poste
used_players = {
    'Gardien': [],
    'Défenseur': [],
    'Milieu': [],
    'Attaquant': []
}

# Parcourir les variables optimales pour classer les joueurs utilisés par poste
for i in range(number_of_players):
    for j, position in enumerate(['Gardien', 'Défenseur', 'Milieu', 'Attaquant']):
        if x[j + i * 4].value == 1:
            player_data = players_df.iloc[i]  # Récupérer les données du joueur depuis le DataFrame
            used_players[position].append(player_data)


# Chemin du fichier équipe type
equipe_type_file = r"C:\Users\pierr\PycharmProjects\Mercato\data\equipe_type.csv"

with open(equipe_type_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Numéro','Nom', 'Prénom', 'Âge', 'Nationalité','Position', 'GD',
                     'DEF', 'MID', 'ATK'])
    for position, players_list in used_players.items():
        for player in players_list:
            writer.writerow(player.tolist())

print("Les joueurs utilisés par poste ont été enregistrés dans le fichier equipe_type.csv.")

# Dictionnaire pour stocker les statistiques par poste
stats_par_poste = {
    'Gardien': {'GD': 0, 'DEF': 0, 'MID': 0, 'ATK': 0},
    'Défenseur': {'GD': 0, 'DEF': 0, 'MID': 0, 'ATK': 0},
    'Milieu': {'GD': 0, 'DEF': 0, 'MID': 0, 'ATK': 0},
    'Attaquant': {'GD': 0, 'DEF': 0, 'MID': 0, 'ATK': 0}
}

# Variables pour calculer la somme pondérée des statistiques
total_defense = 0
total_milieu = 0
total_attaque = 0

# Variables pour le calcul de l'âge moyen et de la nationalité dominante
age_total = 0
nombre_joueurs = 0
nationalites = {}

# Lecture du fichier équipe type
with open(equipe_type_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        poste = row['Position']
        stat_gardien = int(row['GD'])
        stat_defense = int(row['DEF'])
        stat_milieu = int(row['MID'])
        stat_attaque = int(row['ATK'])
        age = int(row['Âge'])
        nationalite = row['Nationalité']

        # Calcul de la somme pondérée des statistiques par poste
        stats_par_poste[poste]['GD'] += stat_gardien
        stats_par_poste[poste]['DEF'] += stat_defense
        stats_par_poste[poste]['MID'] += stat_milieu
        stats_par_poste[poste]['ATK'] += stat_attaque

        # Calcul de l'âge total et du nombre de joueurs
        age_total += age
        nombre_joueurs += 1

        # Comptage des nationalités
        if nationalite in nationalites:
            nationalites[nationalite] += 1
        else:
            nationalites[nationalite] = 1

# Calcul des statistiques totales de l'équipe
total_defense = (
    stats_par_poste['Défenseur']['DEF'] +
    3/8 * stats_par_poste['Milieu']['DEF'] +
    1/4 * stats_par_poste['Attaquant']['DEF']
)
total_milieu = (
    stats_par_poste['Milieu']['MID'] +
    3/8 * (stats_par_poste['Attaquant']['MID'] + stats_par_poste['Défenseur']['MID'])
)
total_attaque = (
    stats_par_poste['Attaquant']['ATK'] +
    3/8 * stats_par_poste['Milieu']['ATK'] +
    1/4 * stats_par_poste['Défenseur']['ATK']
)

# Calcul de l'âge moyen
age_moyen = age_total / nombre_joueurs

# Recherche de la nationalité dominante
nationalite_dominante = max(nationalites, key=nationalites.get)

# Écriture des résultats dans un fichier
output_file = r"C:\Users\pierr\PycharmProjects\Mercato\data\equipe_stats.csv"

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Statistique', 'Valeur'])
    writer.writerow(['Total Défense', total_defense])
    writer.writerow(['Total Milieu', total_milieu])
    writer.writerow(['Total Attaque', total_attaque])
    writer.writerow(['Âge Moyen', age_moyen])
    writer.writerow(['Nationalité Dominante', nationalite_dominante])

print("Les statistiques de l'équipe ont été enregistrées dans le fichier equipe_stats.csv.")

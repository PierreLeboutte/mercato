import pandas as pd
import numpy as np

def simulate_match(team_0, team_1):

    df_team_0 = pd.read_csv(r"C:\Users\pierr\PycharmProjects\Mercato\data\teams\{}_stats.csv".format(team_0), encoding='latin-1')
    df_team_1 = pd.read_csv(r"C:\Users\pierr\PycharmProjects\Mercato\data\teams\{}_stats.csv".format(team_1), encoding='latin-1')

    ATK_A = float(df_team_0[df_team_0['Statistique'] == 'Total Attaque']['Valeur'].values[0])
    DEF_A = float(df_team_0[df_team_0['Statistique'] == 'Total Défense']['Valeur'].values[0])
    MD_A = float(df_team_0[df_team_0['Statistique'] == 'Total Milieu']['Valeur'].values[0])
    GD_A = 450.0  # Modifier en fonction de vos données

    ATK_B = float(df_team_1[df_team_1['Statistique'] == 'Total Attaque']['Valeur'].values[0])
    DEF_B = float(df_team_1[df_team_1['Statistique'] == 'Total Défense']['Valeur'].values[0])
    MD_B = float(df_team_1[df_team_1['Statistique'] == 'Total Milieu']['Valeur'].values[0])
    GD_B = 450.0  # Modifier en fonction de vos données

    OFF_A = ATK_A**2 + 0.5 * MD_A**2
    STA_A = (DEF_A**2 + 0.5 * MD_A**2 + GD_A**2.5)/50
    OFF_B = ATK_B**2 + 0.5 * MD_B**2
    STA_B = (DEF_B**2 + 0.5 * MD_B**2 + GD_B ** 2.5)/50

    print(STA_A)
    print(OFF_A)

    # Calcul des buts avec une loi de Poisson
    goals_A = (np.random.poisson(OFF_A/STA_A))//2
    goals_B = (np.random.poisson(OFF_B/STA_B))//2
    print(team_0+ "-"+team_1+ ":"+ str(goals_A) + "-" + str(goals_B))
    return goals_A, goals_B




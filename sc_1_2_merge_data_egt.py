# -*- coding: utf-8 -*-


# Create several database : at the level of menages, personnes, deplacements, or trajets.
# These may include or not weekends

from __future__ import division


import pandas as pd


from sc_1_1_read_data_egt import load_data_menages, load_data_personnes, load_data_deplacements, \
    load_data_trajets


def load_data_menages_personnes(weekend):
    # Données table ménages :
    df_menages = load_data_menages(weekend)

    
    # Données table personnes :
    df_personnes = load_data_personnes(weekend)
    
    # Données ménages - personnes
    df_menages_personnes = df_personnes.merge(df_menages, on = 'nquest')
    assert(len(df_menages_personnes) == len(df_personnes))
    assert(len(df_menages_personnes.columns) == len(df_menages.columns) + len(df_personnes.columns) - 1)
    
    df_menages_personnes['np'] = df_menages_personnes['np'].astype(str, inplace = True)
    df_menages_personnes['id_personne'] = df_menages_personnes['nquest'] + '_' + df_menages_personnes['np']
    
    return df_menages_personnes



def load_data_menages_personnes_deplacements(weekend):
    # Données table ménages - personnes :
    df_menages_personnes = load_data_menages_personnes(weekend)
    
    # Données table déplacements :
    df_deplacements = load_data_deplacements(weekend)
    df_deplacements['np'] = df_deplacements['np'].astype(str, inplace = True)
    df_deplacements['id_personne'] = df_deplacements['nquest'] + '_' + df_deplacements['np']
    df_deplacements = df_deplacements.drop(columns=['nquest', 'np', 'nd'])

    df_menages_personnes_deplacements = df_menages_personnes.merge(df_deplacements, on = 'id_personne')

    return df_menages_personnes_deplacements


def load_data_menages_personnes_deplacements_paris(weekend):
    # Données table ménages - personnes :
    df_menages_personnes = load_data_menages_personnes(weekend)
    
    # Données table déplacements :
    df_deplacements = load_data_deplacements(weekend)
    
    # Passe par Paris
    df_deplacements['traverse_paris'] = 1 * (df_deplacements['trp'] == '1')
    df_deplacements['traverse_pas_paris'] = 1 * (df_deplacements['trp'] == '2')
    df_deplacements['part_de_paris'] = 1 * (df_deplacements['orcour'] == '1')
    df_deplacements['arrive_a_paris'] = 1 * (df_deplacements['destcour'] == '1')
    df_deplacements['passe_par_paris'] = df_deplacements['part_de_paris'] + df_deplacements['arrive_a_paris'] + df_deplacements['traverse_paris']

    df_deplacements['np'] = df_deplacements['np'].astype(str, inplace = True)
    df_deplacements['id_personne'] = df_deplacements['nquest'] + '_' + df_deplacements['np']
    df_deplacements = df_deplacements.drop(columns=['nquest', 'np', 'nd'])

    # Ceux qui disent être passé par Paris
    df_deplacements_paris = df_deplacements.query('passe_par_paris > 0')
    # Ceux qui ne disent pas ne pas être passé par Paris
    df_deplacements_paris_bis = df_deplacements.query('traverse_pas_paris == 0')
    
    df_menages_personnes_deplacements_paris = df_menages_personnes.merge(df_deplacements_paris, on = 'id_personne')
    df_menages_personnes_deplacements_paris_bis = df_menages_personnes.merge(df_deplacements_paris_bis, on = 'id_personne')

    return df_menages_personnes_deplacements_paris, df_menages_personnes_deplacements_paris_bis


def select_best_trip(data): # On note les déplacements d'après le motif puis d'après leur durée
    data['best_trip'] = 0
    data.best_trip[data.motif_combine == '1'] = 10 # domicile-travail
    data.best_trip[data.motif_combine == '2'] = 9 # domicile-études
    data.best_trip[data.motif_combine == '8'] = 8 # secondaire lié au travail
    data.best_trip[data.motif_combine == '6'] = 7 # domicile-loisirs/visites
    data.best_trip[data.motif_combine == '4'] = 6 # domicile-affaires perso
    data.best_trip[data.motif_combine == '3'] = 5 # domicile-achats
    data.best_trip[data.motif_combine == '5'] = 4 # domicile-accompagnement
    data.best_trip[data.motif_combine == '7'] = 3 # domicile-autres
    data.best_trip[data.motif_combine == '9'] = 2 # secondaire non lié au travail
    data.best_trip[data.motif_combine == ''] = 1 # inconnu
    del data['motif_combine']
    
    data.duree = data.duree.fillna(0)
    data.best_trip = data.best_trip + (data.duree / 1000)

    data = data.sort_values('best_trip', ascending=False)
    data = data.drop_duplicates(subset=['id_personne'], keep='first')
    data = data.sort_values('id_personne', ascending = True)

    return data


def load_data_personnes_paris_domicile_travail(weekend, selection):
    df_deplacements_paris = load_data_menages_personnes_deplacements_paris(weekend)[selection]
    df_personne_paris = df_deplacements_paris.drop_duplicates(subset=['id_personne'], keep='first')

    return df_personne_paris


def load_data_egt(weekend):
    # Données table ménages - personnes :
    df_menages_personnes = load_data_menages_personnes(weekend)

    # Données table déplacements :
    df_deplacements = load_data_deplacements(weekend)
   
    # Données table trajets :
    df_trajets = load_data_trajets(weekend)
       
    # Données déplacements - trajets
    df_trajets['np'] = df_trajets['np'].astype(str, inplace = True)
    df_trajets['nd'] = df_trajets['nd'].astype(str, inplace = True)
    df_trajets['id_deplacement'] = df_trajets['nquest'] + '_' + df_trajets['np'] + '_' + df_trajets['nd']
    df_trajets = df_trajets.drop(['nquest', 'np', 'nd'], axis=1)
    
    
    df_deplacements['np'] = df_deplacements['np'].astype(str, inplace = True)
    df_deplacements['nd'] = df_deplacements['nd'].astype(str, inplace = True)
    df_deplacements['id_deplacement'] = df_deplacements['nquest'] + '_' + df_deplacements['np'] + '_' + df_deplacements['nd']
    df_deplacements['id_personne'] = df_deplacements['nquest'] + '_' + df_deplacements['np']
    df_deplacements = df_deplacements.drop(columns=['nquest', 'np', 'nd'])
    
    df_deplacements_trajets = df_deplacements.merge(df_trajets, on = 'id_deplacement')
    assert(len(df_deplacements_trajets) == len(df_trajets))
    assert(len(df_deplacements_trajets.columns) == len(df_deplacements.columns) + len(df_trajets.columns) - 1)
    
    # Base finale
    df_finale = df_menages_personnes.merge(df_deplacements_trajets, on = 'id_personne')
    assert(len(df_finale) == len(df_deplacements_trajets))
    assert(len(df_finale.columns) == len(df_deplacements_trajets.columns) + len(df_menages_personnes.columns) - 1)

    return df_finale


if __name__ == "__main__":
    weekend = False
    data = load_data_egt(weekend)

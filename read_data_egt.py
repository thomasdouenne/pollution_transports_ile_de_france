# -*- coding: utf-8 -*-

# Pour le moment rien ne fonctionne, à part la concaténation des différents jours de la semaine
# A partir de la doc, faire le tri dans les variables et surtout éviter de les cumuler lors du merge




from __future__ import division


import pandas as pd


# Données table ménages :
df_menages_semaine = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\menages_semaine.dta')
df_menages_samedi = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\menages_samedi.dta')
df_menages_dimanche = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\menages_dimanche.dta')

df_menages = pd.concat([df_menages_semaine, df_menages_samedi, df_menages_dimanche])
df_menages = df_menages.drop_duplicates(subset=['nquest'], keep=False)

# Selection des variables ménages
variables_menages = [
    'nquest',
    ]

df_menages = df_menages[variables_menages]


# Données table personnes :
df_personnes_semaine = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\personnes_semaine.dta')
df_personnes_samedi = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\personnes_samedi.dta')
df_personnes_dimanche = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\personnes_dimanche.dta')

df_personnes = pd.concat([df_personnes_semaine, df_personnes_samedi, df_personnes_dimanche])

# Selection des variables personnes
variables_personnes = [
    'nquest',
    'np'
    ]

df_personnes = df_personnes[variables_personnes]


# Données table déplacements :
df_deplacements_semaine = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\deplacements_semaine.dta')
df_deplacements_samedi = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\deplacements_samedi.dta')
df_deplacements_dimanche = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\deplacements_dimanche.dta')

df_deplacements = pd.concat([df_deplacements_semaine, df_deplacements_samedi, df_deplacements_dimanche], sort = False)

# Selection des variables déplacements
variables_deplacements = [
    'nquest',
    'np',
    'nd'
    ]

df_deplacements = df_deplacements[variables_deplacements]


# Données table trajets :
df_trajets_semaine = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\trajets_semaine.dta')
df_trajets_samedi = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\trajets_samedi.dta')
df_trajets_dimanche = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\trajets_dimanche.dta')

df_trajets = pd.concat([df_trajets_semaine, df_trajets_samedi, df_trajets_dimanche])

# Selection des variables trajets
variables_trajets = [
    'nquest',
    'np',
    'nd'
    ]

df_trajets = df_trajets[variables_trajets]


# Revoir tout ce qui suit...

# Données ménages - personnes
df_menages_personnes = df_personnes.merge(df_menages, on = 'nquest')

df_trajets['np'] = str(df_trajets['np'])
df_deplacements['np'] = str(df_deplacements['np'])
df_trajets['nd'] = str(df_trajets['nd'])
df_deplacements['nd'] = str(df_deplacements['nd'])
df_trajets['id_deplacement'] = df_trajets['nquest'] + '_' + df_trajets['np'] + '_' + df_trajets['nd']
df_trajets = df_trajets.drop(columns=['nquest', 'np', 'nd'])
df_deplacements['id_deplacement'] = df_deplacements['nquest'] + '_' + df_deplacements['np'] + '_' + df_deplacements['nd']
df_deplacements = df_deplacements.drop(columns=['nquest', 'np', 'nd'])

df_deplacements_trajets = df_deplacements.merge(df_trajets, on = 'id_deplacements')

df_menages_personnes['np'] = str(df_menages_personnes['np'])
df_menages_personnes['id_personne'] = df_menages_personnes['nquest'] + '_' + df_menages_personnes['np']
df_deplacements_trajets['id_personne'] = df_deplacements_trajets['id_deplacement'].str[:-2]

df_finale = df_menages_personnes.merge(df_deplacements_trajets, on = 'id_personne')

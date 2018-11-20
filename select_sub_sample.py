# -*- coding: utf-8 -*-

# L'objectif de ce script est d'identifier le sous échantillon des ménages qui nous intéresse
# En particulier, on cherchera à identifier les ménages ne se rendant jamais à Paris


from __future__ import division

from read_data_egt import load_data_menages, load_data_personnes, load_data_deplacements, \
    load_data_trajets, load_data_menages_personnes, load_data_menages_personnes_deplacements, load_data_egt, \
    load_data_menages_personnes_deplacements_paris

#data_menages = load_data_menages(weekend = False)
#data_personnes = load_data_personnes(weekend = True)
#data_menages_personnes_deplacements = load_data_menages_personnes_deplacements(weekend = True)
#data_trajets = load_data_trajets(weekend = True)
#data_finale = load_data_egt(weekend = True)
#data_paris_personnes = data_paris.drop_duplicates(subset=['nquest'], keep='first')

df_deplacements = load_data_menages_personnes_deplacements_paris(weekend = False)[0]
df_deplacements_bis = load_data_menages_personnes_deplacements_paris(weekend = False)[1]


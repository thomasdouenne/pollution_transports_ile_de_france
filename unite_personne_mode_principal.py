# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division

from read_data_egt_1 import load_data_menages, load_data_personnes, load_data_deplacements, \
    load_data_trajets
from build_samples_2 import load_data_menages_personnes_deplacements_paris, load_data_personnes_paris


df_deplacements_paris = load_data_menages_personnes_deplacements_paris(weekend = False)[0]
print df_deplacements_paris['motif_combine']
df_deplacements_paris['domicile_travail'] = 1 * (df_deplacements_paris['motif_combine'] == '1')
print df_deplacements_paris['domicile_travail'].mean()
df_deplacements_paris['domicile_etudes'] = 1 * (df_deplacements_paris['motif_combine'] == '2')
print df_deplacements_paris['domicile_etudes'].mean()
df_deplacements_paris['secondaire_travail'] = 1 * (df_deplacements_paris['motif_combine'] == '8')
print df_deplacements_paris['secondaire_travail'].mean()


df_deplacements_paris.motif_combine[df_deplacements_paris.motif_combine == ''] = 10
df_deplacements_paris['motif_combine'] = df_deplacements_paris['motif_combine'].astype(int)

df_deplacements_paris['duree'].mean()

for i in range(1,11):
    data = df_deplacements_paris.query('motif_combine == {}'.format(i))
    data.duree = data.duree.fillna(0)
    print i, data['duree'].mean(), float(len(data)) / len(df_deplacements_paris) * 100



data = load_data_menages_personnes_deplacements_paris(weekend = False)[0]
data = data.sort_values('best_trip', ascending=False)
data_bis = data.drop_duplicates(subset=['id_personne'], keep='first')
data_bis = data_bis.sort_values('id_personne', ascending = True)


bibi = load_data_personnes_paris(weekend = False, selection = 0)

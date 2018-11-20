# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est le mode principal.


from __future__ import division

from read_data_egt import load_data_menages, load_data_personnes, load_data_deplacements, \
    load_data_trajets, load_data_menages_personnes, load_data_egt

#data_menages = load_data_menages(weekend = True)
#data_personnes = load_data_personnes(weekend = True)
#data_deplacements = load_data_deplacements(weekend = True)
#data_trajets = load_data_trajets(weekend = True)
#data_finale = load_data_egt(weekend = True)


data = load_data_menages_personnes(weekend = False)
data['centre_ville'] = 1 * (data['rescour'] == '1')
print data['centre_ville'].mean() # 13% habitent à Paris (avant pondération)

data['se_deplace'] = 1 * (data['nbdepl'] > 0)
print data['se_deplace'].mean() # 86% se déplacent

data['utilise_vp'] = 1 * (data['nbdeplvp'] > 0)
print data['utilise_vp'].mean() # 42% utilisent leur VP

data['utilise_tc'] = 1 * (data['nbdepltc'] > 0)
print data['utilise_tc'].mean() # 30% utilisent les TC

data['utilise_vp_tc'] = data['utilise_vp'] + data['utilise_tc'] - data['utilise_vp'] * data['utilise_tc']
print data['utilise_vp_tc'].mean() # 66% utilisent au moins un des deux (VP ou TC)
print (data['utilise_vp'] * data['utilise_tc']).mean() # 6% utilisent les deux (VP et TC)
print 1 - data['utilise_vp_tc'].mean() # 34% n'utilisent aucun des deux (VP ou TC)

data['utilise_velo'] = 1 * (data['nbdeplvelo'] > 0)
print data['utilise_velo'].mean() # 2% utilisent leur vélo

data['utilise_2rm'] = 1 * (data['nbdepl2rm'] > 0)
print data['utilise_2rm'].mean() # 42% utilisent leur VP





data['option_downton'] = data['centre_ville']
data['option_private_trans'] = data['utilise_vp'] - data['utilise_vp'] * data['centre_ville']
data['option_public_trans'] = (
    data['utilise_tc']
    - data['utilise_tc'] * data['centre_ville']
    - data['utilise_tc'] * data['utilise_vp']
    + data['utilise_tc'] * data['centre_ville'] * data['utilise_vp']
    )

print data['option_downton'].mean()
print data['option_private_trans'].mean()
print data['option_public_trans'].mean()
# En restreignant comme on l'a fait, on garde 70% du sample / ensuite il faut virer ceux qui ne vont jamais à Paris





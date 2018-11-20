# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division

from read_data_egt import load_data_menages, load_data_personnes, load_data_deplacements, \
    load_data_trajets, load_data_menages_personnes, load_data_egt, load_data_personnes_paris


def define_option_unite_personne(weekend):
    data = load_data_personnes_paris(weekend, selection = 0)
    data = data.query('age > 18')
    data['centre_ville'] = 1 * (data['rescour'] == '1')
    data['utilise_vp'] = 1 * (data['nbdeplvp'] > 0)
    data['utilise_tc'] = 1 * (data['nbdepltc'] > 0)

    data['option_downton'] = data['centre_ville']
    data['option_private_trans'] = data['utilise_vp'] - data['utilise_vp'] * data['centre_ville']
    data['option_public_trans'] = (
        data['utilise_tc']
        - data['utilise_tc'] * data['centre_ville']
        - data['utilise_tc'] * data['utilise_vp']
        + data['utilise_tc'] * data['centre_ville'] * data['utilise_vp']
        )

    return data


if __name__ == "__main__":
    data = define_option_unite_personne(weekend = False)

    print data['option_downton'].mean()
    print data['option_private_trans'].mean()
    print data['option_public_trans'].mean()
    print data['option_downton'].mean() + data['option_private_trans'].mean() + data['option_public_trans'].mean()
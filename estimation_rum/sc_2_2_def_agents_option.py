# -*- coding: utf-8 -*-

# Define agents chosen option between downtown, private transports and public ones

from __future__ import division


from sc_2_1_select_sub_samples import load_data_personnes_paris_best_trip


def define_option(data):
    # On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
    # Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois
    data = data.query('age > 18')
    data['live_downtown'] = 1 * (data['rescour'] == '1')
    data['use_vp'] = 1 * (data['nbdeplvp'] > 0)
    data['use_tc'] = 1 * (data['nbdepltc'] > 0)

    data['option_dt'] = data['live_downtown']
    data['option_vp'] = data['use_vp'] - data['use_vp'] * data['live_downtown']
    data['option_tc'] = (
        data['use_tc']
        - data['use_tc'] * data['live_downtown']
        - data['use_tc'] * data['use_vp']
        + data['use_tc'] * data['live_downtown'] * data['use_vp']
        )

    return data


if __name__ == "__main__":
    weekend = False
    selection = 0
    data = load_data_personnes_paris_best_trip(weekend, selection)
    data = define_option(data)

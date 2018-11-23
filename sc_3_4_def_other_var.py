# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division

import random

from sc_2_1_select_sub_samples import load_data_personnes_paris_best_trip
from sc_2_2_def_agents_option import define_option


def define_housing_rent(data): # Impute housing excess rent downtown. The imputation is homogenous and perfectly arbitrary
    #data['rent_downtown'] = data['loy_hc'] * (data['option_downtown'] == 1)
    data['excess_rent_downtown'] = 200 # On suppose le loyer 200€ plus cher en centre-ville, identique pour tous
    # Monthly rent

    return data


def define_pollution_exposure(data): # Impute pollution levels for the three options

    data['hourly_wage'] = data['income'] / 155 # On suppose 155h travaillées par mois
    constant = 0.001 # To be defined !
    data['wtp_pollution'] = constant * data['hourly_wage']
    data['pollution_exposure'] = (
        0 * data['option_downtown']
        + 0 * data['option_private_trans']
        + 0 * data['option_public_trans']
        ) # On fixe par défaut le niveau de pollution à 0 partout

    return data


def add_other_variables(data):
    data = define_option(data)
    data = define_housing_rent(data)
    data = define_pollution_exposure(data)
    
    return data


if __name__ == "__main__":
    weekend = False
    selection = 0
    data = load_data_personnes_paris_best_trip(weekend, selection)
    data = add_other_variables(data)

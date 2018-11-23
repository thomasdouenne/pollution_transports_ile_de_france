# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division

import random

from sc_2_1_select_sub_samples import load_data_personnes_paris_best_trip
from sc_2_2_def_agents_option import define_option


def define_income_random_uniform(data): # Impute income : take random number in income intervals
    # Ideally, we would like to know the exact conditional distribution
    data['income_hh'] = (
        800 * (data['revenu'] == '1') # On fixe un minimum à 800
        + random.uniform(800, 1200) * (data['revenu'] == '2')
        + random.uniform(1200, 1600) * (data['revenu'] == '3')
        + random.uniform(1600, 2000) * (data['revenu'] == '4')
        + random.uniform(2000, 2400) * (data['revenu'] == '5')
        + random.uniform(2400, 3000) * (data['revenu'] == '6')
        + random.uniform(3000, 3500) * (data['revenu'] == '7')
        + random.uniform(3500, 4500) * (data['revenu'] == '8')
        + random.uniform(4500, 5500) * (data['revenu'] == '9')
        + random.uniform(5500, 10000) * (data['revenu'] == '10') # On fixe un maximum à 10,000
        + random.uniform(1200, 2000) * (data['revenu'] == '11') # On impute pour ceux qui refusent de répondre
        + random.uniform(1200, 2000) * (data['revenu'] == '12') # On impute pour ceux qui ne savent pas
        )
    
    data['income'] = data['income_hh'] # On pourrait diviser le revenu du ménage par le nombre d'actifs ou de majeurs ou par uc
    
    return data


def define_income(data): # Impute income from the discrete variable: take the average of each bin
    data['income_hh'] = (
        800 * (data['revenu'] == '1') # On fixe un minimum à 800
        + (800 + 1200)/2 * (data['revenu'] == '2')
        + (1200 + 1600)/2 * (data['revenu'] == '3')
        + (1600 + 2000)/2 * (data['revenu'] == '4')
        + (2000 + 2400)/2 * (data['revenu'] == '5')
        + (2400 + 3000)/2 * (data['revenu'] == '6')
        + (3000 + 3500)/2 * (data['revenu'] == '7')
        + (3500 + 4500)/2 * (data['revenu'] == '8')
        + (4500 + 5500)/2 * (data['revenu'] == '9')
        + (5500 + 10000)/2 * (data['revenu'] == '10') # On fixe un maximum à 10,000
        + 1600 * (data['revenu'] == '11') # On impute pour ceux qui refusent de répondre
        + 1600 * (data['revenu'] == '12') # On impute pour ceux qui ne savent pas
        )
    
    data['income'] = data['income_hh'] # On pourrait diviser le revenu du ménage par le nombre d'actifs ou de majeurs ou par uc
    
    return data


if __name__ == "__main__":
    weekend = False
    selection = 0
    data = load_data_personnes_paris_best_trip(weekend, selection)
    data = define_option(data)
    data = define_income_random_uniform(data)
    
    print data['income']()

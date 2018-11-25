# -*- coding: utf-8 -*-

# Define agents income using alternative procedures: impute average of income category
# or select randomly from this category (using a uniform distribution, see if there are better alternatives)


from __future__ import division

import numpy

from sc_2_1_select_sub_samples import load_data_personnes_paris_best_trip
from sc_2_2_def_agents_option import define_option


def define_income_random_uniform(data): # Impute income : take random number in income intervals
    # Ideally, we would like to know the exact conditional distribution
    data['income_hh'] = (
        (600 + (800 - 600) * numpy.random.rand(len(data))) * (data['revenu'] == '1') # On fixe un minimum à 600
        + (800 + (1200 - 800) * numpy.random.rand(len(data))) * (data['revenu'] == '2')
        + (1200 + (1600 - 1200) * numpy.random.rand(len(data))) * (data['revenu'] == '3')
        + (1600 + (2000 - 1600) * numpy.random.rand(len(data))) * (data['revenu'] == '4')
        + (2000 + (2400 - 2000) * numpy.random.rand(len(data))) * (data['revenu'] == '5')
        + (2400 + (3000 - 2400) * numpy.random.rand(len(data))) * (data['revenu'] == '6')
        + (3000 + (3500 - 3000) * numpy.random.rand(len(data))) * (data['revenu'] == '7')
        + (3500 + (4500 - 3500) * numpy.random.rand(len(data))) * (data['revenu'] == '8')
        + (4500 + (5500 - 4500) * numpy.random.rand(len(data))) * (data['revenu'] == '9')
        + (5500 + (10000 - 5500) * numpy.random.rand(len(data))) * (data['revenu'] == '10') # On fixe un maximum à 10,000
        + (1200 + (2000 - 1200) * numpy.random.rand(len(data))) * (data['revenu'] == '11') # On impute pour ceux qui refusent de répondre
        + (1200 + (2000 - 1200) * numpy.random.rand(len(data))) * (data['revenu'] == '12') # On impute pour ceux qui ne savent pas
        + (1200 + (2000 - 1200) * numpy.random.rand(len(data))) * (data['revenu'] == '') # On impute pour ceux qui ne savent pas
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
    
    print data['income'].min()

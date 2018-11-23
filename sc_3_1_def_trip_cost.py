# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division

import random

from build_samples_2 import load_data_personnes_paris_best_trip


def define_fuel_cost(data):
    # An alternative way to compute trip distance is to focus on distance for the job/housing trip based on variable "ddomtrav"
    data['essence'] = 1 * ((data['energv1'] == '1') + (data['energv1'] == '2'))
    data['diesel'] = 1 * (data['energv1'] == '3')

    # Look at fuel prices at the time of the survey to be more precise
    data['fuel_cost_per_liter'] = 1.4 * (data['essence']) + 1.2 * (data['diesel']) # Imputation
    # du prix du carburant selon l'énergie utilisée par le premier véhicule du ménage
    # Att : revoir les prix imputés arbitrairement
 
    data.puissv1[data.puissv1 == ''] = 0
    data['puissv1'] = data['puissv1'].astype(int)
    data['fuel_consumption_100_km'] = (0.06) * (data['puissv1'] < 5) + (0.12) * (1 - 1 * (data['puissv1'] < 5))
    # conso fixée totalement arbitrairement en fonction des chevaux fiscaux, à revoir
    data['fuel_cost'] = (
        data['option_private_trans'] * (data['dportee'] * data['fuel_consumption_100_km'] * data['fuel_cost_per_liter'])
        ) + (1 - data['option_private_trans']) * 2.44 # We impute average fuel cost of VP users for those who do not take their VP

    # Add other sources of costs such as car maintenance or insurance

    data['fuel_cost'] = data['fuel_cost'] * 10 * 4.5 # Go from one trip cost to monthly one


    
def define_insurance_cost_vehicle_random_uniform(data): # Impute cost vehicle : take random number in income intervals
    # Ideally, we would like to know the exact conditional distribution
    data['insurance_cost_hh'] = (
        0 * (data['asscout'] == '7') # On fixe un minimum à 0
        + random.uniform(0, 400) * (data['asscout'] == '1')
        + random.uniform(400, 800) * (data['asscout'] == '2')
        + random.uniform(800, 1200) * (data['asscout'] == '3')
        + random.uniform(1200, 1600) * (data['asscout'] == '4')
        + random.uniform(1600, 2000) * (data['asscout'] == '5')
        + random.uniform(2000, 5000) * (data['asscout'] == '6') # On fixe un maximum à 5,000
        + random.uniform(0, 1000) * (data['asscout'] == '8') # We set between 0 and 1,000 for those who don't know
        ) / 12 # We divide to get monthly cost from annual one

    data['insurance_cost'] = data['insurance_cost_hh'] # On pourrait diviser le asscout du ménage par le nombre d'actifs ou de majeurs ou par uc
    
    return data


def define_maintenance_cost_vehicle_random_uniform(data): # Impute cost vehicle : take random number in income intervals
    # Ideally, we would like to know the exact conditional distribution
    data['maintenance_cost_hh'] = (
        0 * (data['ancout'] == '7') # On fixe un minimum à 0
        + random.uniform(0, 400) * (data['ancout'] == '1')
        + random.uniform(400, 800) * (data['ancout'] == '2')
        + random.uniform(800, 1200) * (data['ancout'] == '3')
        + random.uniform(1200, 1600) * (data['ancout'] == '4')
        + random.uniform(1600, 2000) * (data['ancout'] == '5')
        + random.uniform(2000, 5000) * (data['ancout'] == '6') # On fixe un maximum à 5,000
        + random.uniform(0, 1000) * (data['ancout'] == '8') # We set between 0 and 1,000 for those who don't know
        ) / 12 # We divide to get monthly cost from annual one

    data['maintenance_cost'] = data['maintenance_cost_hh'] # On pourrait diviser le ancout du ménage par le nombre d'actifs ou de majeurs ou par uc
    
    return data


def price_public_transport_card(data):
    # Use zones and type of membership to define price based on historical rates
    # Normalize to a monthly price
    return data


def define_share_public_transport_card_paid(data):
    data['share_tc_card_paid'] = (
        0 * (data['rembtc'] == '1') # On fixe un minimum à 0
        + random.uniform(0, 0.25) * (data['rembtc'] == '2')
        + 0.25 * (data['rembtc'] == '3')
        + random.uniform(0.26, 0.5) * (data['rembtc'] == '4')
        + 0.5 * (data['rembtc'] == '5')
        + random.uniform(0.51, 0.75) * (data['rembtc'] == '6')
        + 0.75 * (data['rembtc'] == '7')
        + random.uniform(0.76, 1) * (data['rembtc'] == '8')
        + 1 * (data['rembtc'] == '9')
        + random.uniform(0, 1) * (data['rembtc'] == '10') # We set between 0 and 1,000 for those who don't know
        )

    return data



if __name__ == "__main__":
    weekend = False
    selection = 0
    data = load_data_personnes_paris_best_trip(weekend, selection)
    
    data = define_fuel_cost(data)
    data = define_insurance_cost_vehicle_random_uniform(data)
    data = define_maintenance_cost_vehicle_random_uniform(data)

    print data['fuel_cost'].mean()
    print data['maintenance_cost'].mean()
    print data['insurance_cost'].mean()












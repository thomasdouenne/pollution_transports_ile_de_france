# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division

import random

from build_samples_2 import load_data_personnes_paris_best_trip


def define_option(weekend, selection):
    data = load_data_personnes_paris_best_trip(weekend, selection)
    data = data.query('age > 18')
    data['centre_ville'] = 1 * (data['rescour'] == '1')
    data['utilise_vp'] = 1 * (data['nbdeplvp'] > 0)
    data['utilise_tc'] = 1 * (data['nbdepltc'] > 0)

    data['option_downtown'] = data['centre_ville']
    data['option_private_trans'] = data['utilise_vp'] - data['utilise_vp'] * data['centre_ville']
    data['option_public_trans'] = (
        data['utilise_tc']
        - data['utilise_tc'] * data['centre_ville']
        - data['utilise_tc'] * data['utilise_vp']
        + data['utilise_tc'] * data['centre_ville'] * data['utilise_vp']
        )

    return data

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


def define_housing_rent(data): # Impute housing excess rent downtown. The imputation is homogenous and perfectly arbitrary
    #data['rent_downtown'] = data['loy_hc'] * (data['option_downtown'] == 1)
    data['excess_rent_downtown'] = 200 # On suppose le loyer 200€ plus cher en centre-ville, identique pour tous
    # Monthly rent

    return data


def define_private_transport_cost(data): # Impute private transport cost (vehicle size, distance, insurance, etc.)
    data['dportee'] = data['dportee'].fillna(0)
    
    # Look at fuel prices at the time of the survey to be more precise
    data['essence'] = 1 * ((data['energv1'] == '1') + (data['energv1'] == '2'))
    data['diesel'] = 1 * (data['energv1'] == '3')
    
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

    data['p_v'] = data['fuel_cost'] * 10 * 4.5

    return data


def define_public_transport_cost(data): # Impute public transport cost (price of fares)
    # Look at fare prices depending on zones at the time of the survey
    # Impute a price per trip / per day
    data['p_t'] = 500 / 12 # On suppose l'abonnement coûte 500€/an, et on se ramène à un mois    
    
    # More difficult : impute it for those who live downtown when these costs are heterogeneous
    return data


def define_downtown_transport_non_monetary_costs(data): # Impute non-monetary costs of taking transports when living downtown
    data['hourly_wage'] = data['income'] / 155 # On suppose 155h travaillées par mois
    data['vtt'] = data['hourly_wage'] * 0.3 # On suppose la VTT égale à 30% du salaire < à la VTT pour les trajets en VP
    data['d_d'] = data['vtt'] * (36 / 60) # On normalise à 36 min les temps de trajet sur la base du temps moyen pour les downtown
    del data['hourly_wage'], data['vtt']

    # Pour passer du coût par trajet au coût par mois, on suppose 10 trajets / semaine et 4.5 semaines / mois :
    data['d_d'] = 10 * 4.5 * data['d_d']

    return data


def define_private_transport_non_monetary_costs(data): # Impute private transport non-monetary costs depending on time loss
    # One should use the time of the trip (which one???)
    # Then, multiply by the VTT
    data['hourly_wage'] = data['income'] / 155 # On suppose 155h travaillées par mois
    data['vtt'] = data['hourly_wage'] * 0.5 # On suppose la VTT égale à 50% du salaire
    data['vp_trip_duration'] = (
        data['duree'] * data['option_private_trans']
        + (1-data['option_private_trans']) * 66
        ) # Pour ceux qui ne prennent pas leur VP, on leur impute comme contrefactuel la durée moyenne du groupe VP
    data['d_v'] = data['vtt'] * (data['vp_trip_duration'] / 60)
    del data['hourly_wage'], data['vtt']

    # Pour passer du coût par trajet au coût par mois, on suppose 10 trajets / semaine et 4.5 semaines / mois :
    data['d_v'] = 10* 4.5 * data['d_v']

    return data


def define_public_transport_non_monetary_costs(data): # Impute public transport non-monetary costs depending on time loss and comfort
    # One should use the time of the trip (which one???)
    # Then, multiply by the VTT
    data['hourly_wage'] = data['income'] / 155 # On suppose 155h travaillées par mois
    data['vtt'] = data['hourly_wage'] * 0.75 # On suppose la VTT égale à 75% du salaire > aux VP à cause du confort moindre
    data['tc_trip_duration'] = (
        data['duree'] * data['option_public_trans']
        + (1 - data['option_public_trans']) * 73.5
        ) # Pour ceux qui ne prennent pas les TC, on leur impute comme contrefactuel la durée moyenne du groupe TC

    data['d_t'] = data['vtt'] * (data['tc_trip_duration'] / 60)
    del data['hourly_wage'], data['vtt']
    
    # Pour passer du coût par trajet au coût par mois, on suppose 10 trajets / semaine et 4.5 semaines / mois :
    data['d_t'] = 10* 4.5 * data['d_t']

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


def get_variables(weekend, selection):
    data = define_option(weekend, selection)
    data = define_income(data)
    data = define_housing_rent(data)
    data = define_private_transport_cost(data)
    data = define_public_transport_cost(data)
    data = define_downtown_transport_non_monetary_costs(data)
    data = define_private_transport_non_monetary_costs(data)
    data = define_public_transport_non_monetary_costs(data)
    data = define_pollution_exposure(data)

    return data


def select_variables_final_dataset(weekend, selection):
    data = get_variables(weekend, selection)
    data = data[
        ['option_downtown'] + ['option_private_trans'] + ['option_public_trans']
        + ['income'] + ['excess_rent_downtown'] + ['p_v'] + ['p_t']
        + ['d_d'] + ['d_v'] + ['d_t'] + ['pollution_exposure'] + ['mnp']
        + ['duree'] + ['dportee'] + ['loy_hc'] + ['surf']
        ]
    # On ajoute 'mnp', le nombre de personnes du ménage comme variable de contrôle pour l'aménité résidentielle
    
    return data


if __name__ == "__main__":
    weekend = False
    selection = 0
    data = select_variables_final_dataset(weekend, selection)

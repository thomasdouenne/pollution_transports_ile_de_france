# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division

from read_data_egt import load_data_personnes_paris


def define_option(weekend):
    data = load_data_personnes_paris(weekend, selection = 0)
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


def define_income(data): # Impute income from the discrete variable
    data['income'] = (
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
    
    return data


def define_housing_rent(data): # Impute housing rent with suburb/downtown counterfactual
    data['rent_downtown'] = data['loy_hc'] * (data['option_downtown'] == 1)
    # Trouver un moyen d'imputer un loyer aux propriétaires
    
    return data


def define_private_transport_cost(data): # Impute private transport cost (vehicle size, distance, insurance, etc.)
    # Impute a distance
    # Determine vehicle consumption by trip
    # Look at fuel prices at the time of the survey
    
    # More difficult : impute it for those who live downtown
    return data


def define_public_transport_cost(data): # Impute public transport cost (price of fares)
    # Look at fare prices depending on zones at the time of the survey
    # Impute a price per trip / per day
    
    # More difficult : impute it for those who live downtown
    return data


def define_private_transport_non_monetary_costs(data): # Impute private transport non-monetary costs depending on time loss
    # One should use the time of the trip (which one???)
    # Then, multiply by the VTT
    data['hourly_wage'] = data['income'] / 155 # On suppose 155h travaillées par mois
    data['vtt'] = data['hourly_wage'] * 0.8 # On suppose la VTT égale à 80% du salaire
    data['d_v'] = data['vtt'] * (data['duree'] / 60)

    # Il faudrait aussi imputer une durée de déplacements pour ceux vivant en centre ville

    return data


def define_public_transport_non_monetary_costs(data): # Impute public transport non-monetary costs depending on time loss and comfort
    # One should use the time of the trip (which one???)
    # Then, multiply by the VTT
    data['hourly_wage'] = data['income'] / 155 # On suppose 155h travaillées par mois
    data['vtt'] = data['hourly_wage'] * 0.8 # On suppose la VTT égale à 80% du salaire
    data['d_t'] = data['vtt'] * (data['duree'] / 60)

    # And add lack of comfort based on whether he took it during peak hours
    # This lack of comfort could be sort of a markup on VTT

    # Il faudrait aussi imputer une durée de déplacements pour ceux vivant en centre ville
    return data


def define_pollution_exposure(data): # Impute pollution levels for the three options

    return data


if __name__ == "__main__":
    data = define_option(weekend = False)

    print data['option_downtown'].mean()
    print data['option_private_trans'].mean()
    print data['option_public_trans'].mean()
    print data['option_downtown'].mean() + data['option_private_trans'].mean() + data['option_public_trans'].mean()
    
    print data['rent_downtown']
    print data['occuplog']
    
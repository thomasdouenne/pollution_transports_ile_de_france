# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division


from sc_2_1_select_sub_samples import load_data_personnes_paris_best_trip
from sc_2_2_def_agents_option import define_option
from sc_3_1_def_income import define_income


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


def add_trip_non_mon_costs_variables(data):
    return data


if __name__ == "__main__":
    weekend = False
    selection = 0
    data = load_data_personnes_paris_best_trip(weekend, selection)
    data = define_option(data)
    data = define_income(data)
    data = add_trip_non_mon_costs_variables(data)

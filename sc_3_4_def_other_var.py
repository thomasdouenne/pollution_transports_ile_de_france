# -*- coding: utf-8 -*-

# Define other important variables

from __future__ import division

from sc_2_1_select_sub_samples import load_data_personnes_paris_best_trip
from sc_2_2_def_agents_option import define_option


def define_housing_rent(data): # Impute housing excess rent downtown. The imputation is homogenous and perfectly arbitrary
    #data['rent_downtown'] = data['loy_hc'] * (data['option_downtown'] == 1)
    data.surf = data.surf.fillna(70) #C we arbitrary set housing size to 70m2 when information is not given (18 agents)
    avg_rent_downtown = (data.query('option_dt == 1').query('loy_hc > 0')['loy_hc']).mean() / (data.query('option_dt == 1').query('surf > 0')['surf']).mean() * 66
    avg_rent_vp = (data.query('option_vp == 1').query('loy_hc > 0')['loy_hc']).mean() / (data.query('option_vp == 1').query('surf > 0')['surf']).mean() * 66
    avg_rent_tc = (data.query('option_tc == 1').query('loy_hc > 0')['loy_hc']).mean() / (data.query('option_tc == 1').query('surf > 0')['surf']).mean() * 66

    data['excess_rent_downtown'] = avg_rent_downtown - (avg_rent_vp + avg_rent_tc)/2 # On suppose le loyer 200€ plus cher en centre-ville, identique pour tous
    data['q_d'] = data['excess_rent_downtown']
    return data


def define_pollution_exposure(data): # Impute pollution levels for the three options

    data['hourly_wage'] = data['income'] / 155 # On suppose 155h travaillées par mois
    constant = 0.001 # To be defined !
    data['wtp_pollution'] = constant * data['hourly_wage']
    data['pollution_exposure'] = (
        0 * data['option_dt']
        + 0 * data['option_vp']
        + 0 * data['option_tc']
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

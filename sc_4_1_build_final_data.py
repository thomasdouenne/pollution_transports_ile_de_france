# -*- coding: utf-8 -*-

# On étudie séparément toutes les personnes en supposant qu’elles peuvent déménager indépendamment.
# Le mode de transport retenu est la voiture lorsque les personnes l'utilisent au moins une fois


from __future__ import division


from sc_2_1_select_sub_samples import load_data_personnes_paris_best_trip
from sc_2_2_def_agents_option import define_option
from sc_3_1_def_income import define_income
from sc_3_2_def_trip_cost import add_trip_costs_variables
from sc_3_3_def_trip_non_mon_cost import add_trip_non_mon_costs_variables
from sc_3_4_def_other_var import add_other_variables


def get_variables(weekend, selection):
    data = load_data_personnes_paris_best_trip(weekend, selection)
    data = define_option(data)
    data = define_income(data)
    data = add_trip_costs_variables(data)
    data = add_trip_non_mon_costs_variables(data)
    data = add_other_variables(data)

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

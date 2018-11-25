# -*- coding: utf-8 -*-

# Build the final database by putting together all the relevant variables created
# and selecting the ones that we want to keep


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


def compute_total_option_cost(weekend, selection):
    data = get_variables(weekend, selection)
    data['cost_dt'] = data['q_d'] + data['d_d']
    data['cost_vp'] = data['p_v'] + data['d_v']
    data['cost_tc'] = data['p_t'] + data['d_t']

    return data


def select_variables_final_dataset(weekend, selection):
    data = compute_total_option_cost(weekend, selection)
    data = data[
        ['option_dt'] + ['option_vp'] + ['option_tc']
        + ['income'] + ['p_v'] + ['p_t']
        + ['d_d'] + ['d_v'] + ['d_t'] + ['q_d'] + ['pollution_exposure']
        + ['mnp'] + ['duree'] + ['dportee'] + ['surf']
        + ['cost_dt'] + ['cost_vp']+ ['cost_tc']
        ]
    # On ajoute 'mnp', le nombre de personnes du ménage comme variable de contrôle pour l'aménité résidentielle
    
    return data


if __name__ == "__main__":
    weekend = False
    selection = 0
    data = select_variables_final_dataset(weekend, selection)
    
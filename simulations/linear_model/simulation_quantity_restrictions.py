# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import seaborn

seaborn.set_palette(seaborn.color_palette("Set2", 12))

"""
WIP
"""


columns = ['r_']
N = 10000
df_sim = pd.DataFrame(index=range(1,N+1), columns=columns)

"""
Set agent index
"""

df_sim = df_sim.reset_index()

"""
Set parameters values:
"""

nu = (1.0 / 155) * 40 * (20.0 / 60) * 0.4 # People spend 20min in their car without traffic, they work 150h a month
# they do the trip 40 times a month, their vtt is 0.4 their income
theta = (1.0 / 155) * 40 * (22.0 / 60) * 0.5 # People spend 25min in their car without traffic, they work 150h a month
# they do the trip 40 times a month, their vtt is 0.5 their income
mu = 3.5 # sensitivity of time travel to congestion
gamma = 3 # sensitivity of time travel to congestion
epsilon = 0.025
a = -100 # amenity value in euro per month
p_v = 4.5 * 40 # price of the trip in PV, for a month
p_t = 1 * 40 # Price of the trip in TC, for a month
alpha = 1
lower_r = 500
n_d = 0.38
psi = (1.0 / 155) * 40 * (15.0 / 60) * 0.4 # used to normalize the non-monetary costs
# of transports in the suburb as being the excess value relative to the city

"""
Find n_v and n_t at equilibrium without policy
"""

n_t = 0
t_is_pref = 1
while t_is_pref == 1:
    n_t = n_t + 0.00001
    left = p_v + nu * (lower_r + alpha * N * n_t) * (1 + mu * (1 - n_d - n_t))
    right = p_t + theta * (lower_r + alpha * N * n_t) * (1 + gamma * n_t)
    q_d = a - psi * (lower_r + alpha * N*(1 - n_d)) + p_v + nu * (lower_r + alpha * N*(1 - n_d)) * (1 + mu*(1 - n_d - n_t))

    t_is_pref = 1 * ((left - right) > 0)

n_v = 1 - n_d - n_t


df_sim['r_'] = lower_r + df_sim['index'] # Check that the distributon is consistent with the value of alpha

x = 1
new_n_v_users = n_v
new_nb_veh = n_v
for cible in range(1,100): # These are percentage of reduction of traffic flow relative to the no policy scenario
    nb_veh_cible = n_v - (n_v * float(cible) / 100)
    while np.abs(new_nb_veh - nb_veh_cible) > 1e-03:
        new_n_t = 1 - n_d - new_n_v_users
        x = nb_veh_cible / new_n_v_users
        df_sim['b_t'] = (
            df_sim['r_'] - p_t
            - theta * (1 + gamma * (new_n_t + (1-x) * new_n_v_users)) * df_sim['r_']
            - epsilon * x * new_n_v_users * df_sim['r_']
            )
        df_sim['b_v'] = x * (
            df_sim['r_'] - p_v
            - nu * (1 + mu * new_n_v_users * x) * df_sim['r_']
            - epsilon * x * new_n_v_users * df_sim['r_']
            ) + (1-x)* df_sim['b_t']

        q_d = (
            a - psi * (lower_r + alpha * N*(1 - n_d))
            + x * (p_v + nu * (lower_r + alpha * N*(1 - n_d)) * (1 + mu * new_n_v_users * x))
            + (1-x) * (p_t + theta * (lower_r + alpha * N*(1 - n_d)) * (1 + gamma * (new_n_t + (1-x) * new_n_v_users)))
            )

        df_sim['b_d'] = (
            df_sim['r_'] - q_d
            + a - psi * df_sim['r_']
            - epsilon * x * new_n_v_users * df_sim['r_']
            )

        df_sim['b_option'] = (
            df_sim['b_d'] * (df_sim['b_d'] > df_sim['b_v'] + 1e-06) * (df_sim['b_d'] > df_sim['b_t'])
            + df_sim['b_v'] * (df_sim['b_v'] + 1e-06 > df_sim['b_d']) * (df_sim['b_v'] + 1e-06 > df_sim['b_t'])
            + df_sim['b_t'] * (df_sim['b_t'] > df_sim['b_d']) * (df_sim['b_t'] > df_sim['b_v'] + 1e-06)
            )
        df_sim['option_v'] = (
            1 * (df_sim['b_v'] + 1e-06 > df_sim['b_d']) * (df_sim['b_v'] + 1e-06 > df_sim['b_t'] + 2e-06)
            )
        new_n_v_users = df_sim['option_v'].mean()
        new_nb_veh = new_n_v_users * x

    print df_sim['option_v'].mean(), x, new_nb_veh, q_d

# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn

seaborn.set_palette(seaborn.color_palette("Set2", 12))


"""
In this script, we compute the optimal toll in the linear model with revenue-recycling
An important assumption is that agents own their homes so that the aggregate welfare impact of rents is null
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
Find n_v and n_t at equilibrium for toll
"""

df_toll = pd.DataFrame(index = range(0,101),
    columns = ['toll', 'n_v_toll', 'n_t_toll', 'q_d_toll', 'transfer']
    )
for toll in range(0,101):
    
    monthly_toll = float(toll) / 10 * 40
    n_t = 0
    t_is_pref = 1
    while t_is_pref == 1:
        n_t = n_t + 0.00001
        toll_revenue = monthly_toll * (1 - n_d - n_t)
        left = p_v + monthly_toll + nu * (lower_r + toll_revenue + alpha * N * n_t) * (1 + mu * (1 - n_d - n_t))
        right = p_t + theta * (lower_r + toll_revenue + alpha * N * n_t) * (1 + gamma * n_t)
        q_d = a - psi * (lower_r + toll_revenue + alpha * N*(1 - n_d)) + p_v + monthly_toll + nu * (lower_r + toll_revenue + alpha * N*(1 - n_d)) * (1 + mu*(1 - n_d - n_t))

        t_is_pref = 1 * ((left - right) > 0)

    df_toll['toll'][toll] = toll
    df_toll['n_v_toll'][toll] = 100 * (1 - n_d - n_t)
    df_toll['n_t_toll'][toll] = 100 * n_t
    df_toll['q_d_toll'][toll] = q_d
    df_toll['transfer'][toll] = toll_revenue


"""
Compute welfare gains / losses
"""

df_sim['r_'] = lower_r + df_sim['index'] # Check that the distributon is consistent with the value of alpha


df_optimal = pd.DataFrame(index = range(0,101),
    columns = ['toll', 'aggregate_surplus']
    )
max_aggregate = 0
for toll in range(0,101):
    monthly_toll = float(toll) / 10 * 40
    df_sim['r_after_toll'] = df_sim['r_'] + df_toll['transfer'][toll]
    df_sim['b_d'] = (
        df_sim['r_after_toll'] #- df_toll['q_d_toll'][toll]
        + a - psi * df_sim['r_after_toll']
        - epsilon * (df_toll['n_v_toll'][toll]/100) * df_sim['r_after_toll']
        )
    df_sim['b_v'] = (
        df_sim['r_after_toll'] - p_v - monthly_toll
        - nu * (1 + mu * (df_toll['n_v_toll'][toll]/100)) * df_sim['r_after_toll']
        - epsilon * (df_toll['n_v_toll'][toll]/100) * df_sim['r_after_toll']
        )
    df_sim['b_t'] = (
        df_sim['r_after_toll'] - p_t
        - theta * (1 + gamma * (df_toll['n_t_toll'][toll]/100)) * df_sim['r_after_toll']
        - epsilon * (df_toll['n_v_toll'][toll]/100) * df_sim['r_after_toll']
        )

    df_sim['b_option'] = (
        df_sim['b_d'] * (df_sim['b_d'] > df_sim['b_v'] + 1e-06) * (df_sim['b_d'] > df_sim['b_t'])
        + df_sim['b_v'] * (df_sim['b_v'] + 1e-06 > df_sim['b_d']) * (df_sim['b_v'] + 1e-06 > df_sim['b_t'])
        + df_sim['b_t'] * (df_sim['b_t'] > df_sim['b_d']) * (df_sim['b_t'] > df_sim['b_v'] + 1e-06)
        )
    if toll == 0:
        df_sim['b_option_default'] = df_sim['b_option']
        df_optimal['aggregate_surplus'][toll] = 0
    else:
        df_sim['gain_surplus'] = (
            (df_sim['b_option'] - df_sim['b_option_default']) / df_sim['b_option_default']  
            ) * 100
        df_optimal['aggregate_surplus'][toll] = float(df_sim['gain_surplus'].sum()) / len(df_sim)

    df_optimal['toll'][toll] = toll
    aggregate_surplus = df_optimal['aggregate_surplus'][toll]
    if aggregate_surplus > max_aggregate:
        optimal_tax = toll
    max_aggregate = max(aggregate_surplus, max_aggregate)

print "The optimal toll is {} euros per trip".format(float(optimal_tax) / 10)

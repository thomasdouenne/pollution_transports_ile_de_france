# -*- coding: utf-8 -*-

# In this script we do not consider agents heterogeneity with other respects than income
# We first look at the equilibrium level of people using private vs public vehicles
# We then turn to the equilibrium rent price and payoffs

# This algorithm is not working properly

import pandas as pd
import numpy as np

columns = ['r_', 'q_d', 'p_v', 'p_t', 'd_d', 'd_v', 'd_t']
df_sim = pd.DataFrame(index=range(1,1000001), columns=columns)

# Agent index
df_sim = df_sim.reset_index()

# Agent income
df_sim['r_'] = 500 + (5000 - 500) * (df_sim['index'] / len(df_sim))

# Transport prices
# df_sim['distance'] = 5 + (15 - 5) * np.random.rand(len(df_sim))
df_sim['distance'] = 10
df_sim['p_v'] = 10 * df_sim['distance']
df_sim['p_t'] = 50
df_sim['toll'] = 100
df_sim['subsidy'] = 50

df_sim['duree_v'] = df_sim['distance'] / 60
df_sim['duree_t'] = df_sim['distance'] / 60

df_sim['vtt_v'] = df_sim['r_'] * 0.45
df_sim['vtt_t'] = df_sim['r_'] * 0.6

df_sim['b_v'] = 0
df_sim['b_t'] = 0

n_d = 35 # Exogenous number of people downtown
marginal_agent = len(df_sim) * 0.65
current_n_v = 35
new_n_v = 0

while np.abs(new_n_v - current_n_v) > 0.001 :
    current_n_v = (9 * current_n_v + new_n_v) / 10
    current_n_t = 100 - n_d - current_n_v
    
    congestion_v = 1 + 10 * ((float(current_n_v)/100)**(2))
    congestion_t = 1 + 10 * ((float(current_n_t)/100)**(2))
    
    df_sim['duree_v'] = df_sim['distance'] / 60 * congestion_v
    df_sim['duree_t'] = df_sim['distance'] / 60 * congestion_t

    df_sim['d_v'] = df_sim['duree_v'] * df_sim['vtt_v']
    df_sim['d_t'] = df_sim['duree_t'] * df_sim['vtt_t']

    df_sim['q_d'] = df_sim['p_v'] + df_sim['d_v'][marginal_agent] + df_sim['toll'] - 0.001

    df_sim['b_d'] = df_sim['r_'] - df_sim['q_d']
    df_sim['b_v'] = df_sim['r_'] - df_sim['p_v'] - df_sim['d_v'] - df_sim['toll']
    df_sim['b_t'] = df_sim['r_'] - df_sim['p_t'] - df_sim['d_t'] + df_sim['subsidy']

    df_sim['option_d'] = 1 * (df_sim['b_d'] > df_sim['b_v']) * (df_sim['b_d'] > df_sim['b_t'])
    df_sim['option_v'] = 1 * (df_sim['b_v'] > df_sim['b_d']) * (df_sim['b_v'] > df_sim['b_t'])
    df_sim['option_t'] = 1 * (df_sim['b_t'] > df_sim['b_v']) * (df_sim['b_t'] > df_sim['b_d'])

    new_n_v = df_sim['option_v'].mean() * 100

print new_n_v

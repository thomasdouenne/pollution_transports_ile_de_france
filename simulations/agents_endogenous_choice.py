# -*- coding: utf-8 -*-

# In this script we do not consider agents heterogeneity with other respects than income
# We first look at the equilibrium level of people using private vs public vehicles
# We then turn to the equilibrium rent price and payoffs


import pandas as pd
#import numpy as np

columns = ['r_', 'q_d', 'p_v', 'p_t', 'd_d', 'd_v', 'd_t']
df_sim = pd.DataFrame(index=range(1,1001), columns=columns)

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

# Transport non-monetary costs
congestion_v = 1
congestion_t = 1

marginal_agent = len(df_sim) - 350
i = marginal_agent

# Find equilibrium number
keep_going = 1
while keep_going == 1:
    i = i - 1
    congestion_v = 1 + 10 * ((float(650 - i)/1000)**(2))
    congestion_t = 1 + 10 * ((float(i)/1000)**(2))

    df_sim['duree_v'][i] = float(df_sim['distance'][i]) / 60 * congestion_v
    df_sim['duree_t'][i] = float(df_sim['distance'][i]) / 60 * congestion_t

    df_sim['d_v'][i] = df_sim['duree_v'][i] * df_sim['vtt_v'][i]
    df_sim['d_t'][i] = df_sim['duree_t'][i] * df_sim['vtt_t'][i]

    df_sim['b_v'][i] = df_sim['r_'][i] - df_sim['p_v'][i] - df_sim['d_v'][i] - df_sim['toll'][i]
    df_sim['b_t'][i] = df_sim['r_'][i] - df_sim['p_t'][i] - df_sim['d_t'][i] + df_sim['subsidy'][i]

    keep_going = 1 * (df_sim['b_v'][i] > df_sim['b_t'][i])

# Compute payoffs
df_sim['duree_v'] = df_sim['distance'] / 60 * congestion_v
df_sim['duree_t'] = df_sim['distance'] / 60 * congestion_t

df_sim['d_v'] = df_sim['duree_v'] * df_sim['vtt_v']
df_sim['d_t'] = df_sim['duree_t'] * df_sim['vtt_t']
df_sim['q_d'] = df_sim['p_v'] + df_sim['toll'] + df_sim['d_v'][marginal_agent] - 0.001

df_sim['b_d'] = df_sim['r_'] - df_sim['q_d']
df_sim['b_v'] = df_sim['r_'] - df_sim['p_v'] - df_sim['d_v'] - df_sim['toll']
df_sim['b_t'] = df_sim['r_'] - df_sim['p_t'] - df_sim['d_t'] + df_sim['subsidy']

df_sim['option_d'] = 1 * (df_sim['b_d'] > df_sim['b_v']) * (df_sim['b_d'] > df_sim['b_t'])
df_sim['option_v'] = 1 * (df_sim['b_v'] > df_sim['b_d']) * (df_sim['b_v'] > df_sim['b_t'])
df_sim['option_t'] = 1 * (df_sim['b_t'] > df_sim['b_v']) * (df_sim['b_t'] > df_sim['b_d'])

print "Q_d", df_sim['q_d'].mean()

print "N_d", df_sim['option_d'].mean() * 100
print "N_v", df_sim['option_v'].mean() * 100
print "N_t", df_sim['option_t'].mean() * 100



"""

n_d = 35 # Exogenous number of people downtown
marginal_agent = len(df_sim) - 350
current_n_v = 33
new_n_v = 32


while np.abs(new_n_v - current_n_v) > 0.1 :
    current_n_v = new_n_v
    current_n_t = 100 - n_d - current_n_v
    
    congestion_v = 1 + 0.2 * np.log(current_n_v)
    congestion_t = 1 + 0.2 * np.log(current_n_t)
    
    df_sim['duree_v'] = df_sim['distance'] / 60 * congestion_v
    df_sim['duree_t'] = df_sim['distance'] / 60 * congestion_t

    df_sim['d_v'] = df_sim['duree_v'] * df_sim['vtt_v']
    df_sim['d_t'] = df_sim['duree_t'] * df_sim['vtt_t']

    df_sim['q_d'] = df_sim['p_v'] + df_sim['d_v'][marginal_agent] - 0.001

    df_sim['b_d'] = df_sim['r_'] - df_sim['q_d']
    df_sim['b_v'] = df_sim['r_'] - df_sim['p_v'] - df_sim['d_v']
    df_sim['b_t'] = df_sim['r_'] - df_sim['p_t'] - df_sim['d_t']

    df_sim['option_d'] = 1 * (df_sim['b_d'] > df_sim['b_v']) * (df_sim['b_d'] > df_sim['b_t'])
    df_sim['option_v'] = 1 * (df_sim['b_v'] > df_sim['b_d']) * (df_sim['b_v'] > df_sim['b_t'])
    df_sim['option_t'] = 1 * (df_sim['b_t'] > df_sim['b_v']) * (df_sim['b_t'] > df_sim['b_d'])

    new_n_v = df_sim['option_v'].mean() * 100

"""

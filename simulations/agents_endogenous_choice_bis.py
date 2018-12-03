# -*- coding: utf-8 -*-

# In this script we do not consider agents heterogeneity with other respects than income
# We first look at the equilibrium level of people using private vs public vehicles
# We then turn to the equilibrium rent price and payoffs

# This algorithm is not working properly : create new colmun for N_v for subsidies

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

columns = ['r_', 'q_d', 'p_v', 'p_t', 'd_d', 'd_v', 'd_t']
df_sim = pd.DataFrame(index=range(1,100001), columns=columns)

# Agent index
df_sim = df_sim.reset_index()

# Agent income
df_sim['r_'] = 500 + (5000 - 500) * (df_sim['index'] / len(df_sim))

# Transport prices
# df_sim['distance'] = 5 + (15 - 5) * np.random.rand(len(df_sim))
df_sim['distance'] = 10
df_sim['p_v'] = 10 * df_sim['distance']
df_sim['p_t'] = 50

df_sim['duree_v'] = df_sim['distance'] / 60
df_sim['duree_t'] = df_sim['distance'] / 60

df_sim['vtt_v'] = df_sim['r_'] * 0.45
df_sim['vtt_t'] = df_sim['r_'] * 0.6

df_sim['b_v'] = 0
df_sim['b_t'] = 0

n_d = 30 # Exogenous number of people downtown
marginal_agent = len(df_sim) * (1 - (float(n_d)/100))

# Find the equilibrium allocation
df_to_plot = pd.DataFrame(index = range(0,11),
    columns = ['toll', 'subsidy', 'n_v_toll', 'n_v_subsidy', 'q_d_toll', 'q_d_subsidy']
    )
df_welfare = pd.DataFrame(index = range(0,11),
    columns = ['toll', 'subsidy', 'share_winners_toll', 'share_winners_subsidy']
    )

for policy in ['toll', 'subsidy']:
    for i in range(0,11):
        if policy == 'toll':
            df_sim['toll'] = i * 10
            df_sim['subsidy'] = 0
        else:
            df_sim['toll'] = 0
            df_sim['subsidy'] = i * 10
            
        current_n_v = 35
        new_n_v = 0
        
        while np.abs(new_n_v - current_n_v) > 0.001 :
            current_n_v = (9 * current_n_v + new_n_v) / 10
            current_n_t = 100 - n_d - current_n_v
            
            congestion_v = 1 + 5 * ((float(current_n_v)/100)**(2))
            congestion_t = 1 + 5 * ((float(current_n_t)/100)**(2))
            
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
            q_d = df_sim['q_d'].mean()
        
        df_to_plot['n_v_{}'.format(policy)][i] = new_n_v
        df_to_plot['q_d_{}'.format(policy)][i] = q_d
        df_to_plot[policy][i] = i * 10
        
        if i == 0:
            df_sim['b_option_default'] = (
                    df_sim['b_d'] * df_sim['option_d']
                    + df_sim['b_v'] * df_sim['option_v']
                    + df_sim['b_t'] * df_sim['option_t']
                    )
        else:
            df_sim['b_option_{}_{}'.format(policy, i)] = 0
            df_sim['b_option_{}_{}'.format(policy, i)] = (
                    df_sim['b_d'] * df_sim['option_d']
                    + df_sim['b_v'] * df_sim['option_v']
                    + df_sim['b_t'] * df_sim['option_t']
                    ) - df_sim['b_option_default']
            df_welfare['share_winners_{}'.format(policy)][i] = (df_sim['b_option_{}_{}'.format(policy, i)] > 0).mean() * 100
            df_welfare[policy][i] = i * 10

    
# Create graphs - equilibrium N_v
plt.title("PV users as a function of toll price")
plt.plot(df_to_plot['toll'], df_to_plot['n_v_toll'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Share of people using Private Vehicules')
plt.show()

plt.title("PV users as a function of subsidy price")
plt.plot(df_to_plot['subsidy'], df_to_plot['n_v_subsidy'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Share of people using Private Vehicules')
plt.show()

# Create graphs - equilibrium Q_d
plt.plot(df_to_plot['toll'], df_to_plot['q_d_toll'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Excess monthly rent downtown')
plt.show()

plt.plot(df_to_plot['subsidy'], df_to_plot['q_d_subsidy'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Excess monthly rent downtown')
plt.show()


# Look at welfare impact
plt.plot(df_welfare['toll'], df_welfare['share_winners_toll'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Share of winners as a function of tolls')
plt.show()

plt.plot(df_welfare['subsidy'], df_welfare['share_winners_subsidy'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Share of winners as a function of subsidies')
plt.show()


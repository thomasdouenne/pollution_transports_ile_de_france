# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn

seaborn.set_palette(seaborn.color_palette("Set2", 12))

# In this script, we calibrate the linear model for which we can get analytic solutions

columns = ['r_', 'q_d', 'p_v', 'p_t', 'd_d', 'd_v', 'd_t', 'x_']
N = 10000
df_sim = pd.DataFrame(index=range(1,N+1), columns=columns)

# Agent index
df_sim = df_sim.reset_index()

# Set parameters values:
nu = (1.0 / 155) * 40 * (20.0 / 60) * 0.4 # People spend 20min in their car without traffic, they work 150h a month
# they do the trip 40 times a month, their vtt is 0.4 their income
theta = (1.0 / 155) * 40 * (22.0 / 60) * 0.5 # People spend 25min in their car without traffic, they work 150h a month
# they do the trip 40 times a month, their vtt is 0.5 their income
mu = 3.5 # sensitivity of time travel to congestion
gamma = 3 # sensitivity of time travel to congestion
epsilon = 1
a = -100 # amenity value in euro per month
p_v = 4.5 * 40 # price of the trip in PV, for a month
p_t = 1 * 40 # Price of the trip in TC, for a month
alpha = 1
n_d = 0.38
psi = (1.0 / 155) * 40 * (15.0 / 60) * 0.4 # used to normalize the non-monetary costs
# of transports in the suburb as being the excess value relative to the city

# Find n_v and n_t at equilibrium
df_to_plot = pd.DataFrame(index = range(0,101),
    columns = ['toll', 'n_v_toll', 'n_t_toll', 'q_d_toll']
    )
for policy in ['toll']:
    for toll in range(0,101):
        
        monthly_toll = float(toll) / 10 * 40
        n_t = 0
        t_is_pref = 1
        while t_is_pref == 1:
            n_t = n_t + 0.00001
            left = p_v + monthly_toll + nu * (p_t + alpha * N * n_t) * (1 + mu * (1 - n_d - n_t))
            right = p_t + theta * (p_t + alpha * N * n_t) * (1 + gamma * n_t)
            q_d = a - psi * (p_t + alpha * N*(1 - n_d)) + p_v + nu * (p_t + alpha * N*(1 - n_d)) * (1 + mu*(1 - n_d - n_t))

            t_is_pref = 1 * ((left - right) > 0)

        df_to_plot['toll'][toll] = toll
        df_to_plot['n_v_toll'][toll] = 100 * (1 - n_d - n_t)
        df_to_plot['n_t_toll'][toll] = 100 * n_t
        df_to_plot['q_d_toll'][toll] = q_d

# Create graph - equilibrium N_v
plt.title("PV users as a function of toll price")
plt.plot(df_to_plot['toll'], df_to_plot['n_v_toll'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Share of people using Private Vehicules')
plt.grid(True)
plt.show()

# Create graphs - equilibrium Q_d
plt.plot(df_to_plot['toll'], df_to_plot['q_d_toll'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Excess monthly rent downtown')
plt.grid(True)
plt.show()

# Plot share of each option
df_to_plot['n_d_toll'] = 35
df_to_plot[['n_t_toll', 'n_v_toll', 'n_d_toll']].plot.bar(stacked=True, width=1) 

# Compute functions for welfare
df_sim['r_'] = 500 + (10000) * (df_sim['index'] / len(df_sim)) # Check that the distributon is consistent with the value of alpha


#df_sim['d_v'] = nu * df_sim['r_'] * (1 + mu * n_v)
#df_sim['d_t'] = theta * df_sim['r_'] * (1 + gamma * n_t)
#df_sim['x_'] = epsilon * n_v * df_sim['r_']

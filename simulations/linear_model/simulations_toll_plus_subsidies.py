# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
import seaborn

seaborn.set_palette(seaborn.color_palette("hls", 12))

"""
In this script, we calibrate the linear model for which we can get analytic solutions
The revenue of the tax is recycled through public transport subsidies
We assume homes are owned by people living outside the region
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
    columns = ['toll', 'n_v_toll', 'n_t_toll', 'q_d_toll']
    )
for toll in range(0,101):
    
    monthly_toll = float(toll) / 10 * 40
    n_t = 0
    t_is_pref = 1
    while t_is_pref == 1:
        n_t = n_t + 0.00001
        monthly_subsidy = monthly_toll * (1 - n_d - n_t) / n_t
        left = p_v + monthly_toll + nu * (p_t + alpha * N * n_t) * (1 + mu * (1 - n_d - n_t))
        right = p_t - monthly_subsidy + theta * (p_t + alpha * N * n_t) * (1 + gamma * n_t)
        q_d = a - psi * (p_t + alpha * N*(1 - n_d)) + p_v + monthly_toll + nu * (p_t + alpha * N*(1 - n_d)) * (1 + mu*(1 - n_d - n_t))

        t_is_pref = 1 * ((left - right) > 0)

    df_toll['toll'][toll] = toll
    df_toll['n_v_toll'][toll] = 100 * (1 - n_d - n_t)
    df_toll['n_t_toll'][toll] = 100 * n_t
    df_toll['q_d_toll'][toll] = q_d



"""
Compute welfare gains / losses
"""

df_sim['r_'] = lower_r + df_sim['index'] # Check that the distributon is consistent with the value of alpha

for toll in [0,10,30,50,100]:
    monthly_toll = float(toll) / 10 * 40
    monthly_subsidy = monthly_toll * float(df_toll['n_v_toll'][toll]) / df_toll['n_t_toll'][toll]
    df_sim['b_d_{}'.format(toll)] = (
        df_sim['r_'] - df_toll['q_d_toll'][toll] + a - psi * df_sim['r_']
        )
    df_sim['b_v_{}'.format(toll)] = (
        df_sim['r_'] - p_v - monthly_toll - nu * (1 + mu * (df_toll['n_v_toll'][toll]/100)) * df_sim['r_']
        )
    df_sim['b_t_{}'.format(toll)] = (
        df_sim['r_'] - p_t + monthly_subsidy - theta * (1 + gamma * (df_toll['n_t_toll'][toll]/100)) * df_sim['r_']
        )

    df_sim['b_option_{}'.format(toll)] = (
        df_sim['b_d_{}'.format(toll)] * (df_sim['b_d_{}'.format(toll)] > df_sim['b_v_{}'.format(toll)] + 1e-06) * (df_sim['b_d_{}'.format(toll)] > df_sim['b_t_{}'.format(toll)])
        + df_sim['b_v_{}'.format(toll)] * (df_sim['b_v_{}'.format(toll)] + 1e-06 > df_sim['b_d_{}'.format(toll)]) * (df_sim['b_v_{}'.format(toll)] + 1e-06 > df_sim['b_t_{}'.format(toll)])
        + df_sim['b_t_{}'.format(toll)] * (df_sim['b_t_{}'.format(toll)] > df_sim['b_d_{}'.format(toll)]) * (df_sim['b_t_{}'.format(toll)] > df_sim['b_v_{}'.format(toll)] + 1e-06)
        )

    if toll != 0:
        df_sim['gain_{}'.format(toll)] = (
            (df_sim['b_option_{}'.format(toll)] - df_sim['b_option_0']) / df_sim['b_option_0']  
            )
        df_sim['gain_level_{}'.format(toll)] = (
            (df_sim['b_option_{}'.format(toll)] - df_sim['b_option_0'])
            )
    df_sim['option_{}'.format(toll)] = (
        1 * (df_sim['b_d_{}'.format(toll)] > df_sim['b_v_{}'.format(toll)] + 1e-06) * (df_sim['b_d_{}'.format(toll)] > df_sim['b_t_{}'.format(toll)] + 2e-06)
        + 2 * (df_sim['b_v_{}'.format(toll)] + 1e-06 > df_sim['b_d_{}'.format(toll)]) * (df_sim['b_v_{}'.format(toll)] + 1e-06 > df_sim['b_t_{}'.format(toll)] + 2e-06)
        + 3 * (df_sim['b_t_{}'.format(toll)] + 2e-06 > df_sim['b_d_{}'.format(toll)]) * (df_sim['b_t_{}'.format(toll)] + 2e-06 > df_sim['b_v_{}'.format(toll)] + 1e-06)
        )


"""
Create graphics
"""

# Create graphs - equilibrium Q_d - tolls
plt.plot(df_toll['toll'], df_toll['q_d_toll'])
plt.xlabel('Policy value in euros per month')
plt.ylabel('Excess monthly rent downtown')
plt.grid(True)
plt.show()

# Create graphs - loss from toll in euro equivalent
plt.plot(df_sim['r_'], df_sim[['gain_level_10'] + ['gain_level_30'] + ['gain_level_50'] + ['gain_level_100']])
plt.xlabel('Agents income')
plt.ylabel('Gains / losses')
plt.grid(True)
plt.show()

# Create graphs - loss from toll as a share of income
df_sim = df_sim.rename(columns = {'gain_10': '1 € toll', 'gain_30': '3 € toll', 'gain_50': '5 € toll', 'gain_100': '10 € toll'})
axes = df_sim[['1 € toll'] + ['3 € toll'] + ['5 € toll'] + ['10 € toll']].plot()
axes.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
plt.xlabel('Agents income')
plt.ylabel('Welfare gains relative to no toll')
axes.legend(
    bbox_to_anchor = (1, 1),
        )
plt.grid(True)
plt.show()

# Plot share of each option - tolls
df_toll['n_d_toll'] = 100 * n_d
to_plot = df_toll[['n_t_toll', 'n_v_toll', 'n_d_toll']].plot.bar(stacked=True, width=1) 
to_plot.legend(
    bbox_to_anchor = (0.75, 0.928),
        )

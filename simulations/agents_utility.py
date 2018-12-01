# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

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

# Transport non-monetary costs
df_sim['d_v'] = df_sim['r_'] * 0.45 * df_sim['distance'] / 60
df_sim['d_t'] = df_sim['r_'] * 0.6 * df_sim['distance'] / 60
del df_sim['distance']

df_sim['q_d'] = 400

df_sim['b_d'] = df_sim['r_'] - df_sim['q_d']
df_sim['b_v'] = df_sim['r_'] - df_sim['p_v'] - df_sim['d_v']
df_sim['b_t'] = df_sim['r_'] - df_sim['p_t'] - df_sim['d_t']


df_sim['option_d'] = 1 * (df_sim['b_d'] > df_sim['b_v']) * (df_sim['b_d'] > df_sim['b_t'])
df_sim['option_v'] = 1 * (df_sim['b_v'] > df_sim['b_d']) * (df_sim['b_v'] > df_sim['b_t'])
df_sim['option_t'] = 1 * (df_sim['b_t'] > df_sim['b_v']) * (df_sim['b_t'] > df_sim['b_d'])

print df_sim['option_d'].mean() * 100
print df_sim['option_v'].mean() * 100
print df_sim['option_t'].mean() * 100

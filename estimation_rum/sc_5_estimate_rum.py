# -*- coding: utf-8 -*-

# Estimate a standard random utility model

# Descrition

from __future__ import division

import statsmodels.formula.api as smf


from sc_4_1_build_final_data import select_variables_final_dataset


data = select_variables_final_dataset(weekend = False, selection = 0)

data_suburb = data.query('option_dt == 0')
data_suburb['excess_cost_vp'] = data_suburb['cost_vp'] - data_suburb['cost_tc']
data_suburb['excess_consumption_vp'] = data_suburb['income'] - data_suburb['excess_cost_vp']

variables = ['excess_consumption_vp']

logit = smf.Logit(data_suburb['option_vp'], data_suburb[variables]).fit()
print logit.summary()
params = logit.params

print logit.get_margeff().summary()

#probit = smf.Probit(data['option_downtown'], data[variables]).fit()
#print probit.summary()

# Bosser sur un logit imbriqué (banlieue vs centre ville, puis vp vs tc)

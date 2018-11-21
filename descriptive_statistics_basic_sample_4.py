# -*- coding: utf-8 -*-

from __future__ import division


from build_data_wip_3 import select_variables_final_dataset


data = select_variables_final_dataset(weekend = False, selection = 0)


# Descriptive statics on options :
data_downtown = data.query('option_downtown == 1')
data_private = data.query('option_private_trans == 1')
data_public = data.query('option_public_trans == 1')

print "Share for each option :"
print "downtown", (float(len(data_downtown)) / len(data)) * 100
print "private", (float(len(data_private)) / len(data)) * 100
print "public", (float(len(data_public)) / len(data)) * 100
print "total", (float((len(data_downtown) + len(data_private) + len(data_public))) / len(data)) * 100



# Descriptive statics on income
print "Average income for each option"
print data_downtown['income'].mean()
print data_private['income'].mean()
print data_public['income'].mean()

# Descriptive statics on family size
print "Average family size for each option"
print data_downtown['mnp'].mean()
print data_private['mnp'].mean()
print data_public['mnp'].mean()



# Descriptive statics on trip duration
print "Average trip duration for each option"
print data_downtown['duree'].mean()
print data_private['duree'].mean()
print data_public['duree'].mean()

# Descriptive statics on trip distance
print "Average trip distance for each option"
print data_downtown['dportee'].mean()
print data_private['dportee'].mean()
print data_public['dportee'].mean()



# Descriptive statics on private trip price
print "Average cost private trip for each option"
print data_downtown['p_v'].mean()
print data_private['p_v'].mean()
print data_public['p_v'].mean()

# Descriptive statics on public trip price
print "Average cost public trip for each option"
print data_downtown['p_t'].mean()
print data_private['p_t'].mean()
print data_public['p_t'].mean()

# Distribution of private trip costs
print "Distribution per quantile of private trip cost"
quantiles = [.05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95]
for i in quantiles:
    print i, data_private['p_v'].quantile(i)



# Descriptive statics on private trip non-monetary costs
print "Average non-monetary costs for private trip for each option"
print data_downtown['d_v'].mean()
print data_private['d_v'].mean()
print data_public['d_v'].mean()

# Descriptive statics on public trip non-monetary costs
print "Average non-monetary costs for public trip for each option"
print data_downtown['d_t'].mean()
print data_private['d_t'].mean()
print data_public['d_t'].mean()

# Distribution of private trip non-monetary costs
print "Distribution per quantile of private trip non-monetary costs"
quantiles = [.05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95]
for i in quantiles:
    print i, data_private['d_v'].quantile(i)

# Distribution of public trip non-monetary costs
print "Distribution per quantile of public trip non-monetary costs"
quantiles = [.05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95]
for i in quantiles:
    print i, data_public['d_t'].quantile(i)

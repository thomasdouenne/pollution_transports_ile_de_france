# -*- coding: utf-8 -*-

# Run some descriptive statictis to better understand our final database

from __future__ import division


from sc_4_1_build_final_data import select_variables_final_dataset


data = select_variables_final_dataset(weekend = False, selection = 0)


# Descriptive statics on options :
data_downtown = data.query('option_dt == 1')
data_private = data.query('option_vp == 1')
data_public = data.query('option_tc == 1')

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


# Descriptive statics housing rents : average rent for a 66m² accomodation (average size downtown)
# Note that this should be taken per individual to be closer to what we actually want to get
print data_downtown['q_d'].mean()
print data_private['q_d'].mean()
print data_public['q_d'].mean()
# Interestingly, m² prices are the same for both categories in the suburb, but significantly higher downtown.
# people taking PV have simply larger accomodations, but same price per m².
# Need to update excess price on this basis

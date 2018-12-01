# -*- coding: utf-8 -*-


# Start working on ERFS to better impute income

from __future__ import division


import pandas as pd

data_erfs = pd.read_csv(r'C:\Users\thoma\Documents\Github\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\matching\matching_erfs\data_matching_erfs.csv', sep = ',')

raw_data_erfs = pd.read_stata(r'C:\Users\thoma\Documents\Data\data_erfs\erfs_2012\Stata\fpr_menage_2012_retropole.dta')
variables = raw_data_erfs.columns.tolist()

raw_data_erfs_bis = pd.read_stata(r'C:\Users\thoma\Documents\Data\data_erfs\erfs_2012\Stata\fpr_mrf12e12t4.dta')
variables_bis = raw_data_erfs_bis.columns.tolist()

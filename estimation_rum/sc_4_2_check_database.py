# -*- coding: utf-8 -*-

# Check that everything is correct in the dataframe (nan, duplicates, etc.)

from __future__ import division


from sc_4_1_build_final_data import select_variables_final_dataset


data = select_variables_final_dataset(weekend = False, selection = 0)


# Check that the database does not contain any Nan value
assert(len(data) - len(data.dropna()) == 0)

# Check that the database does not contain any duplicated index
check_duplicates = data.copy()
check_duplicates = check_duplicates.reset_index()
check_duplicates['compare'] = 0
check_duplicates = check_duplicates[['index'] + ['compare']]
for i in range(0, len(check_duplicates)-1):
    check_duplicates['compare'][i+1] = check_duplicates['index'][i+1] - check_duplicates['index'][i]
assert(len(check_duplicates.query('compare == 0')) == 1)

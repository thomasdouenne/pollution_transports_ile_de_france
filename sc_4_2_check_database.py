# -*- coding: utf-8 -*-

# Check that everything is correct in the dataframe (nan, duplicates, etc.)

from __future__ import division


from sc_4_1_build_final_data import select_variables_final_dataset


data = select_variables_final_dataset(weekend = False, selection = 0)


# Check that the database does not contain any Nan value
assert(len(data) - len(data.dropna()) == 0)

# Check that the database does not contain any duplicate
assert(len(data) == len(data.drop_duplicates()))

bibi = data.drop_duplicates()
liste_bibi = bibi.index.tolist()
liste_data = data.index.tolist()
liste_bobo = [element in liste_data if element not in liste_bibi]
# ...

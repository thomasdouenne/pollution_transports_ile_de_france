# -*- coding: utf-8 -*-

from __future__ import division


from math import sqrt
from scipy.stats import norm
import pandas as pd
import numpy as np
from numpy import arange
from pylab import plot, show, grid, xlabel, ylabel

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


# Données table ménages :
df_cergy = pd.read_csv(r'C:\Users\t.douenne\Documents\Data\data_airparif\cergy.csv', sep=';')
df_nogent = pd.read_csv(r'C:\Users\t.douenne\Documents\Data\data_airparif\nogent.csv', sep=';')
df_paris_1 = pd.read_csv(r'C:\Users\t.douenne\Documents\Data\data_airparif\paris_1.csv', sep=';')
df_saint_denis = pd.read_csv(r'C:\Users\t.douenne\Documents\Data\data_airparif\saint_denis.csv', sep=';')
df_versailles = pd.read_csv(r'C:\Users\t.douenne\Documents\Data\data_airparif\versailles.csv', sep=';')


# Cergy
df_cergy = df_cergy.drop(df_cergy.index[0])

df_cergy['annee'] = df_cergy['date'].str[6:]
df_cergy['mois'] = df_cergy['date'].str[3:5]
df_cergy['jour'] = df_cergy['date'].str[0:2]
del df_cergy['date']

df_cergy['indice_temps'] = (
        df_cergy['annee'] + '_' + df_cergy['mois'] + '_'
        + df_cergy['jour'] + '_' + str(df_cergy['heure'])
        )

# Nogent
df_nogent = df_nogent.drop(df_nogent.index[0])

df_nogent['annee'] = df_nogent['date'].str[6:]
df_nogent['mois'] = df_nogent['date'].str[3:5]
df_nogent['jour'] = df_nogent['date'].str[0:2]
del df_nogent['date']

df_nogent['indice_temps'] = (
        df_nogent['annee'] + '_' + df_nogent['mois'] + '_'
        + df_nogent['jour'] + '_' + str(df_nogent['heure'])
        )


# Paris
df_paris_1 = df_paris_1.drop(df_paris_1.index[0])

df_paris_1['annee'] = df_paris_1['date'].str[6:]
df_paris_1['mois'] = df_paris_1['date'].str[3:5]
df_paris_1['jour'] = df_paris_1['date'].str[0:2]
del df_paris_1['date']

df_paris_1['indice_temps'] = (
        df_paris_1['annee'] + '_' + df_paris_1['mois'] + '_'
        + df_paris_1['jour'] + '_' + str(df_paris_1['heure'])
        )


# Paris
df_saint_denis = df_saint_denis.drop(df_saint_denis.index[0])

df_saint_denis['annee'] = df_saint_denis['date'].str[6:]
df_saint_denis['mois'] = df_saint_denis['date'].str[3:5]
df_saint_denis['jour'] = df_saint_denis['date'].str[0:2]
del df_saint_denis['date']

df_saint_denis['indice_temps'] = (
        df_saint_denis['annee'] + '_' + df_saint_denis['mois'] + '_'
        + df_saint_denis['jour'] + '_' + str(df_saint_denis['heure'])
        )


# Paris
df_versailles = df_versailles.drop(df_versailles.index[0])

df_versailles['annee'] = df_versailles['date'].str[6:]
df_versailles['mois'] = df_versailles['date'].str[3:5]
df_versailles['jour'] = df_versailles['date'].str[0:2]
del df_versailles['date']

df_versailles['indice_temps'] = (
        df_versailles['annee'] + '_' + df_versailles['mois'] + '_'
        + df_versailles['jour'] + '_' + str(df_versailles['heure'])
        )



# Faire des moyennes mensuelles pour le NO2
# Faire des moyennes par heure de la journée en semaine, et le weekend
# Comparer
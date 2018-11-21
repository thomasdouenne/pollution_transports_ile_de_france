# -*- coding: utf-8 -*-


# Create several database : at the level of menages, personnes, deplacements, or trajets.
# These may include or not weekends

from __future__ import division


import pandas as pd



def load_data_menages(weekend):
    df_menages_semaine = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\menages_semaine.dta')
    df_menages_samedi = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\menages_samedi.dta')
    df_menages_dimanche = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\menages_dimanche.dta')
    
    if weekend == True:
        df_menages = pd.concat([df_menages_semaine, df_menages_samedi, df_menages_dimanche])
    else:
        df_menages = df_menages_semaine
    assert(len(df_menages) == len(df_menages.drop_duplicates(subset=['nquest'], keep=False)))
    del df_menages_semaine, df_menages_samedi, df_menages_dimanche
    
    
    # Selection des variables ménages (on passe de 101 à 89...)
    variables_menages = [
        'nquest', # id_menage
        'sem', # semaine enquête
        'poidsm', # poids ménage
        'rescour', # couronne de résidence
        'resdep',# département de résidence
        'ressect', # secteur de résidence
        'rescomm', # commune de résidence
        'resc', # carreau de résidence
        'jdep', # jour des déplacements
        'mnp', # nombre personnes ménage
        'mnp5', # nombre 5 ans et plus
        'mnpmob', # nombre qui se sont déplacés
        'mnpact', # nombre actifs
        'typelog', # type de logement
        'occuplog', # occupation du logement
        'loy_hc', # montant du loyer hors charge
        'alloc', # allocations
        'chg', # montant des charges mensuelles
        'loy_park', # montant des loyers de parking
        'nbpi', # nombre de pièces
        'surf', # superficie totale logement
        'nb_velo', # nb vélos en état de marche
        'nb_vae', # nombre de vae ????
        'nb_vd', # nombre de voitures à disposition
        'typev1', # type du véhicule 1
        'energv1', # énergie du véhicule
        'apmcv1', # année de première mise en circulation
        'puissv1', # puissance fiscale
        'ankmv1', # kilométrage moyen annuel
        'cptkmv1', # kilométrage au compteur
        'possv1', # possession du véh 1
        'statv1', # stationnement la nuit véh 1
        'typev2',
        'energv2',
        'apmcv2',
        'puissv2',
        'ankmv2',
        'cptkmv2',
        'possv2',
        'statv2',
        'typev3',
        'energv3',
        'apmcv3',
        'puissv3',
        'ankmv3',
        'cptkmv3',
        'possv3',
        'statv3',
        'typev4',
        'energv4',
        'apmcv4',
        'puissv4',
        'ankmv4',
        'cptkmv4',
        'possv4',
        'statv4',
        'nb_2rm', # nb de 2rm ou 3rm à disposition
        'nb_veh', # nb veh motorisés à disposition
        'typerm1', # type du 2rm/3rm 1
        'motrm1', # type de moteur
        'enerm1', # type d'énergie
        'apmcrm1', # année mise en circulation
        'cylrm1', # cylindrée
        'ankmrm1', # km moyen annuel
        'statrm1', # stationnement la nuit
        'typerm2',
        'motrm2',
        'enerm2',
        'apmcrm2',
        'cylrm2',
        'ankmrm2',
        'statrm2',
        'typerm3',
        'motrm3',
        'enerm3',
        'apmcrm3',
        'cylrm3',
        'ankmrm3',
        'statrm3',
        'typerm4',
        'motrm4',
        'enerm4',
        'apmcrm4',
        'cylrm4',
        'ankmrm4',
        'statrm4',
        'ancout', # cout annuel entretien/réparation flotte de veh
        'asscout', # cout annuel assurance
        'revenu', # classe de revenu net mensuel
        ]
    
    df_menages = df_menages[variables_menages]
    del variables_menages

    return df_menages

    
def load_data_personnes(weekend):
    df_personnes_semaine = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\personnes_semaine.dta')
    df_personnes_samedi = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\personnes_samedi.dta')
    df_personnes_dimanche = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\personnes_dimanche.dta')
    
    if weekend == True:
        df_personnes = pd.concat([df_personnes_semaine, df_personnes_samedi, df_personnes_dimanche])
    else:
        df_personnes = df_personnes_semaine
    del df_personnes_semaine, df_personnes_samedi, df_personnes_dimanche
    
    # Selection des variables personnes (on passe de 61 à 49...)
    variables_personnes = [
        'nquest',
        'np',
        'typep', # type de personne
        'sexe',
        'lienpref', # lien avec personne de référence,
        'age',
        'trage', # classe d'âge
        'permvp', # permis voiture
        'abonvp', # abonnement autopartage
        'perm2rm', # permis 2rm
        'abontc', # abonnement tc
        'zonitc', # zonage de 'labonnement tc (première zone)
        'zonftc', # zonage de 'labonnement tc (dernière zone)
        'supptc', # support abonnement
        'rembtc', # % de l'abonnement à charge
        'abonvls', # abonnement vélib ou vls
        'dipl', # niveau d'étude atteint
        'occp', # occupation principale
        'typlt', # type lieu de travail
        'cs24l', # cat socio-pro
        'cs8', # cat socio-pro en 8 postes
        'cat', # categories de personne
        'ultrav', # unicité lieu de travail/étude
        'ltravcour', # couronne lieu de travail/études
        'ltravdep', # département
        'ltravsect', # secteur
        'ltravcomm', # commune
        'ltravc', # carreau
        'pkvptrav', # disponibilité parking lieu de travail/étude
        'pkvltrav', # dispo parking vélo
        'handi', # gêne dans les déplacements en général
        'handi1', # type de gène 1
        'handi2',
        'handi3',
        'handi4',
        'conge', # conge, arrête de maladie
        'nondepl', # déplacement ou non hier
        'perturb', # pertubations pour les déplacements
        'tperturb', # type de perturbation
        'gene', # gene temporaire ou permanente pour la journée enquêtée
        'puvp', # possibilité d'utiliser un véhicule motorisé conducteur ?????
        'nbdepl', # nb déplacements réalisés
        'nbdeplvp', # nb en voiture
        'nbdeplvpc', # nb en voiture en tant que conducteur
        'nbdepltc', # nb en transports collectifs
        'nbdeplvelo', # nb à vélo
        'nbdepl2rm', # nb à 2 roues motorisé
        'nbdeplmap', # nb à pied
        'ddomtrav', # portée du déplacement domicile-travail/étude en km
        ]
    
    df_personnes = df_personnes[variables_personnes]
    del variables_personnes

    return df_personnes


def load_data_deplacements(weekend):
    df_deplacements_semaine = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\deplacements_semaine.dta')
    df_deplacements_samedi = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\deplacements_samedi.dta')
    df_deplacements_dimanche = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\deplacements_dimanche.dta')
    
    if weekend == True:
        df_deplacements = pd.concat([df_deplacements_semaine, df_deplacements_samedi, df_deplacements_dimanche], sort = False)
    else:
        df_deplacements = df_deplacements_semaine
    del df_deplacements_semaine, df_deplacements_samedi, df_deplacements_dimanche
    
    # Selection des variables déplacements (on passe de 54 à 44...)
    variables_deplacements = [
        'nquest',
        'np',
        'nd',
        'orcour', # couronne d'origine du déplacement
        'ordep', # departement
        'orsect', # secteur
        'orcomm', # commune
        'orc', # carreau
        'orh', # heure de départ
        'orm', # minute de départ
        'ormot', # motif au départ
        'ormot_h9', # motif, 9 catégories
        'destcour', # couronne de destination
        'destdep', # département
        'destsect',
        'destcomm',
        'destc',
        'desth',
        'destm',
        'destmot',
        'destmot_h9',
        'destmot_iaurif02', # motif à l'arrivée
        'motif_combine', # motif combiné origine/destination
        'dportee', # portée du déplacement en km
        'duree', # durée en minutes
        'tlt', # type du lieu de travail si dest = lieu de travail
        'tla', # type lieu d'achat si...
        'nbat', # nb d'arrêts dans la tournée
        'trp', # avez vous traversé Paris intra muros pendant le déplacement ?
        'modp_strict', # mode principal strict détaillé
        'modp_h6', #C mode pirncipal, 6 modalités
        'modp_h7',
        'modp_h12',
        'modp_h19',
        'nbtraj', # nb trajets
        'nbtrajvp', # nb en voiture
        'nbtrajvpc', # en tant que conducteur
        'nbtrajtc', # transports collectifs
        'nbtrajvelo', # nb en vélo
        'nbtraj2rm',
        'idm', # indicateur de déplacement motorisé
        'nbco', # nb de correspondances
        'rab_tc', # mode principal rabattement vers les TC
        'diff_tc' # mode principal diffusion depuis les TC
        ]
    
    df_deplacements = df_deplacements[variables_deplacements]
    del variables_deplacements

    return df_deplacements


def load_data_trajets(weekend):
    df_trajets_semaine = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\trajets_semaine.dta')
    df_trajets_samedi = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\trajets_samedi.dta')
    df_trajets_dimanche = pd.read_stata(r'C:\Users\t.douenne\Documents\Data\data_egt\egt_2010\Stata\trajets_dimanche.dta')
    
    if weekend == True:
        df_trajets = pd.concat([df_trajets_semaine, df_trajets_samedi, df_trajets_dimanche])
    else:
        df_trajets = df_trajets_semaine
    del df_trajets_semaine, df_trajets_samedi, df_trajets_dimanche
    
    # Selection des variables trajets (on passe de 24 à 20...)
    variables_trajets = [
        'nquest',
        'np',
        'nd',
        'nt',
        'moyen', # moyen utilisé pour le trajet
        'tt', # titre de transport utilisé
        'ligne', # ligne de TC utilisée
        'entc', # carreau d'entrée
        'sortc', # carreau de sortie
        'tportee', # portee du trajet en km
        'typv', # num du veh du menage utilisé
        'tstat', # type de stationnement
        'nbpv', # nb personnes dans le veh
        'utp', # emprunté le périph
        'uta86', # emprunté l'A86
        'utfrl', # emprunté la francilienne
        'rembf', # remboursement frais véhicule par employeur
        'pct', # cout du trajet à charge
        'entsect', # secteur entrée dans le mode
        'sortsect', # secteur de sortie
        ]
    
    df_trajets = df_trajets[variables_trajets]
    del variables_trajets

    return df_trajets


if __name__ == "__main__":
    data = load_data_menages()

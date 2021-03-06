###### pollution_transports_ile_de_france


# To do :
    # Améliorer l'efficience du code, ne pas répéter en permanence la définition de l'option
    # Virer les variables qu'on n'utilise plus au fur et à mesure (celles utilisées pour la construction)

    # Faire des progrès sur le calcul de la conso des véhicules
    # Réfléchir à commencer imputer des prix contraints vis-à-vis de prix qui prendraient en compte
    # une forme de loisir (ex : véhicules plus luxueux)
    
    # Tester des mécanismes alternatifs pour le calcul de la distance : utiliser la variable "ddomtrav"
    # qui donne la distance du trajet domicile-travail.
    
    # Commencer à prendre en compte la question de la congestion via horaires de départ
    
    # Regarder comment estimer un RUM et tester via données actuelles. Exemple :
    # https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Main%20PyLogit%20Example.ipynb
    # https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8 
    
    # Faire des progrès sur l'imputation des coûts des transports en commun d'après la zone géographique
    # Utiliser aussi le pourcentage de l'abonnement à charge
    
    # Commencer à réflechir à la manière d'imputer la pollution
    
    # Regarder si les données de l'ERFS permettent d'avoir une meilleure distribution des revenus en IDF
    # Etudier la possibilité d'effectuer un matching ERFS / EGT pour obtenir une meilleure distribution des revenus

    # Construire un RUM tel que la seule variable qui joue soit le coût généralisé des logements / transports
    # i.e. la somme de toutes les variables de coût, définie selon chacune des options.

    # Réfléchir aux variables de contrôle que je pourrais vouloir intégrer
    
    # Essayer de comprendre ce que signifie la présence de "duplicates" dans la database finale


# Organization of the scripts:
    # _1 are the scripts used to load the datasets
    # Since these data come from separate tables, _1_2 merges separate datasets from _1_1 to match together
    # households variables from personal ones.
    
    # _2 are used to select sub-samples from these datasets.
    # These sub-samples discard some households or some trips that will be irrelevant to our analysis
    # Here we move away from he representative raw data and make modleing choices, so this is separated
    # from the data collection in _1 scripts
    # _2_2 defines the agent prefered option (the one chosen)
    
    # _3 are used to compute variables at the household or individual level, such as prices for trips
    # income, non-monetary costs from trips, etc.
    # _3_1 defines income using several approach (random draw, average)
    # _3_2 defines various variables related to the monetary cost of trips
    # _3_3 defines various variables related to the non-monetary cost of trips
    # _3_4 defines variables other than the ones related to trips
    
    # _4 are used to put all the previous things together and build the final database for estimation
    # _4_1 builds the database, _4_2 checks it is fine, and _4_3 runs some descriptive statistics
    
    # _5 are the scripts that estimate the different versions of the RUM

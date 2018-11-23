###### pollution_transports_ile_de_france


# To do :
    # Faire des progrès sur le calcul de la conso des véhicules
    
    # Tester des mécanismes alternatifs pour le calcul de la distance : utiliser la variable "ddomtrav"
    # qui donne la distance du trajet domicile-travail.
    
    # Commencer à prendre en compte la question de la congestion via horaires de départ
    
    # Regarder comment estimer un RUM et tester via données actuelles
    
    # Faire des progrès sur l'imputation des coûts des transports en commun d'après la zone géographique
    # Utiliser aussi le pourcentage de l'abonnement à charge
    
    # Commencer à réflechir à la manière d'imputer la pollution
    
    # Réorganiser les scripts de manière plus claire
    # Aussi, mieux commenter chaque script au début en disant clairement ce que je fais

    # Trouver un moyen de virer les fichiers .pyc


# Organisation of the scripts:
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
    # _3_1 defines various variables related to the monetary cost of trips
    # _3_2 defines various variables related to the non-monetary cost of trips
    # _3_3 defines variables other than the ones related to trips
    
    # _4 are used to put all the previous things together and build the final database for estimation
    # _4_1 builds the database and _4_2 runs some descriptive statistics
    
    # _5 are the scripts that estimate the RUM

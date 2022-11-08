import csv
import numpy

# Retourne la liste des sujets qui ont mal appris la tâche
def mauvais_app(all) :
    testdur = []

    # On récupère toutes les lignes qui correspondent à l'apprentissage
    for row in all:
        if row[80] == 'TESTDUR':
            testdur.append(row)

    # 120 : 1 si rep correcte, 0 sinon
    sujet = 0 # le numéro du sujet qu'on regarde
    bad_guys = [] # la liste des sujets qui ont mal appris
    compt_mauv_rep = 0 # compte les mauvaises réponses pour un sujet

    for i in range(1, len(testdur)):
        if testdur[i][120] == '0': # si c'est une mauvaise réponse

            if sujet == int(testdur[i][1]): # si je suis encore sur le même sujet
                compt_mauv_rep += 1 # une erreur en plus
                if compt_mauv_rep > 4: # si il en fait plus que 4 (25%)
                    if sujet not in bad_guys:
                        bad_guys.append(sujet) # je l'ajoute à la liste des bad guys
            else:
                sujet = int(testdur[i][1]) # Sinon je suis sur un autre sujet, je retiens son numéro
                compt_mauv_rep = 1

    return bad_guys

# Retire une liste de sujets
def remove_subject(all, liste_sujet) :
    print('Sujet à retirer : ', len(liste_sujet), liste_sujet)
    tri_sujet = []
    for row in all :
        if int(row[1]) not in liste_sujet :
            tri_sujet.append(row)
    return tri_sujet


def find_male(all):
    liste_sujet = []
    tri_sujet = []
    for row in all :
        if row[35] == 'Homme' :
            if int(row[1]) not in liste_sujet:
                liste_sujet.append(int(row[1]))
    tri_sujet = remove_subject(all, liste_sujet)
    return tri_sujet


def extract_long_court_35(all_trie):

    final_list = []
    final_list_court = []
    final_list_long = []
    cpt_35_premiers_essai = 0
    # cpt_35_premiers_essai = 0


    # Parcours du fichier
    for row in all_trie:
        # Row
        # 44 : Type sujet : 1 court Entree, 2 court Control
        # 48 : 1 pour Biss1, 2 pour intermede, 3 pour Biss2
        # 117 : 1 pour ENTER, 2 pour CONTROL
        # 116 : vide si phase d'apprentissage
        # 98 : durée stimulus

        # On garde toutes les lignes avec les réponses longues et la ligne vide de l'intermède
        # if row[116] != '' and row[48] != 2 and cpt_35_premiers_essai<35:
        if row[116] != '' and row[48] != 2 and cpt_35_premiers_essai < 35:
            cpt_35_premiers_essai += 1
            # if row[44] != row[117]:  # on ne garde que les réponses longues
            final_list.append(row)

        if row[48] == '2':  # et la ligne vide pour l'intermède
            # cpt_35_premiers_essai = 0
            cpt_35_premiers_essai = 0
            final_list.append(row)

        # Si je suis au dernier au essai -> nouveau sujet
        if row[91] == '70':
            cpt_35_premiers_essai = 0
           # cpt_35_premiers_essai = 0

    # Récupérer la liste des numéros de sujets
    liste_sujets = [1001]
    last = 1001
    compteur_sujet = 0

    # Récupère tous les numéros des sujets
    # Si le numéro de sujet est différent du dernier, je l'enregistre
    for i in range(2, len(final_list)):
        if int(final_list[i][1]) != int(final_list[i - 1][1]):
            last = final_list[i][1]
            liste_sujets.append(last)
            compteur_sujet += 1
    print('Nombre total de sujets : ', compteur_sujet)


    # Comptage des durées
    duree = [208, 272, 336, 400, 464, 528, 592]
    head = ["Sujet", "Session", "Procedure", "DurStim", "RepLong", "RepCourt", "NbRep", "RepLongCorr", 'RepCourtCorr']

    # Première ligne du fichier final
    with open('/Users/admin/OneDrive - Université de Bourgogne/Thèse/Bissolfzique/2021/Résultats/Data_trie_35_premiers.csv',
              'w') as f:
        writer = csv.writer(f)
        writer.writerow(head)

    j = 0  # variable pour les sujets
    compt_duree2_court = [0, 0, 0, 0, 0, 0, 0]  # compteur rep longue pour chaque durée
    compt_duree2_long = [0, 0, 0, 0, 0, 0, 0]  # compteur rep longue pour chaque durée
    compt_duree1_court = [0, 0, 0, 0, 0, 0, 0]  # bissection 1 / bissection 2
    compt_duree1_long = [0, 0, 0, 0, 0, 0, 0]  # bissection 1 / bissection 2

    for i in range(0, len(final_list)):
        if int(final_list[i][1]) == int(liste_sujets[j]):  # Si je suis encore au même sujet

            # Si j'arrive à la deuxième bissection, j'enregistre les valeurs de la première
            if final_list[i][48] == '2':
                compt_duree1_long = compt_duree2_long
                compt_duree1_court = compt_duree2_court
                compt_duree2_court = [0, 0, 0, 0, 0, 0, 0]
                compt_duree2_long = [0, 0, 0, 0, 0, 0, 0]

            # Comptage pour les longs
            if final_list[i][44] != final_list[i][117]:
                if final_list[i][98] == '208':
                    compt_duree2_long[0] += 1
                if final_list[i][98] == '272':
                    compt_duree2_long[1] += 1
                if final_list[i][98] == '336':
                    compt_duree2_long[2] += 1
                if final_list[i][98] == '400':
                    compt_duree2_long[3] += 1
                if final_list[i][98] == '464':
                    compt_duree2_long[4] += 1
                if final_list[i][98] == '528':
                    compt_duree2_long[5] += 1
                if final_list[i][98] == '592':
                    compt_duree2_long[6] += 1

            elif final_list[i][44] == final_list[i][117]:
                if final_list[i][98] == '208':
                    compt_duree2_court[0] += 1
                if final_list[i][98] == '272':
                    compt_duree2_court[1] += 1
                if final_list[i][98] == '336':
                    compt_duree2_court[2] += 1
                if final_list[i][98] == '400':
                    compt_duree2_court[3] += 1
                if final_list[i][98] == '464':
                    compt_duree2_court[4] += 1
                if final_list[i][98] == '528':
                    compt_duree2_court[5] += 1
                if final_list[i][98] == '592':
                    compt_duree2_court[6] += 1

        # Si j'ai fini les données d'un sujet
        else:
            #print("End sujet", liste_sujets[j], compt_duree1, compt_duree2)
            res = []  # tableau pour un sujet
            # Je remplis le tableau avec les données sous la forme
            # N°sujet N°Session Bissection 1/2 Durée NbLong NbCourt
            for k in range(0, 14):
                if k < 7:
                    if compt_duree1_long[k]+compt_duree1_court[k] != 0:
                        res.append(
                            [final_list[i - 1][1], final_list[i - 1][2], 1, duree[k], compt_duree1_long[k],
                             compt_duree1_court[k], compt_duree1_long[k]+compt_duree1_court[k],
                             compt_duree1_long[k]*10/(compt_duree1_long[k]+compt_duree1_court[k]),
                             compt_duree1_court[k]*10/(compt_duree1_long[k]+compt_duree1_court[k])])
                    else:
                        res.append(
                            [final_list[i - 1][1], final_list[i - 1][2], 1, duree[k], compt_duree1_long[k],
                             compt_duree1_court[k], compt_duree1_long[k]+compt_duree1_court[k],
                             0,
                             0])
                else:
                    if compt_duree2_long[k-7]+compt_duree2_court[k-7]!=0:
                        res.append([final_list[i - 1][1], final_list[i - 1][2], 2, duree[k - 7], compt_duree2_long[k - 7],
                                    compt_duree2_court[k - 7], compt_duree2_long[k-7]+compt_duree2_court[k-7],
                                    compt_duree2_long[k-7]*10/(compt_duree2_long[k-7]+compt_duree2_court[k-7]),
                                    compt_duree2_court[k - 7] * 10 / (compt_duree2_long[k - 7] + compt_duree2_court[k - 7])
                                    ])
                    else:
                        res.append([final_list[i - 1][1], final_list[i - 1][2], 2, duree[k - 7], compt_duree2_long[k - 7],
                                compt_duree2_court[k - 7], compt_duree2_long[k-7]+compt_duree2_court[k-7],
                                0,
                                0
                                ])


            # J'ajoute ces données à mon fichier
            with open(
                    '/Users/admin/OneDrive - Université de Bourgogne/Thèse/Bissolfzique/2021/Résultats/Data_trie_35_premiers.csv',
                    'a') as f:
                writer = csv.writer(f)
                writer.writerows(res)

            # Réinitialisation puis on passe au sujet suivant
            j = j + 1
            compt_duree2_court = [0, 0, 0, 0, 0, 0, 0]
            compt_duree2_long = [0, 0, 0, 0, 0, 0, 0]

    return liste_sujets




def extract_long_court(all_trie):
    final_list = []

    # Parcours du fichier
    for row in all_trie:
        # Row
        # 44 : Type sujet : 1 court Entree, 2 court Control
        # 48 : 1 pour Biss1, 2 pour intermede, 3 pour Biss2
        # 117 : 1 pour ENTER, 2 pour CONTROL
        # 116 : vide si phase d'apprentissage
        # 98 : durée stimulus

        # On garde toutes les lignes avec les réponses longues et la ligne vide de l'intermède
        if row[116] != '' and row[48] != 2:
            if row[44] != row[117]:  # on ne garde que les réponses longues
                final_list.append(row)

        if row[48] == '2':  # et la ligne vide pour l'intermède
            final_list.append(row)

    # Récupérer la liste des numéros de sujets
    liste_sujets = [1001]
    last = 1001
    compteur_sujet = 0

    # Récupère tous les numéros des sujets
    # Si le numéro de sujet est différent du dernier, je l'enregistre
    for i in range(2, len(final_list)):
        if int(final_list[i][1]) != int(final_list[i - 1][1]):
            last = final_list[i][1]
            liste_sujets.append(last)
            compteur_sujet += 1
    print('Nombre total de sujets : ', compteur_sujet)

    # Comptage des durées
    duree = [208, 272, 336, 400, 464, 528, 592]
    head = ["Sujet", "Session", "Procedure", "DurStim", "RepLong", "RepCourt"]

    # Première ligne du fichier final
    with open('/Users/admin/OneDrive - Université de Bourgogne/Thèse/Bissolfzique/2021/Résultats/Data_trie.csv',
              'w') as f:
        writer = csv.writer(f)
        writer.writerow(head)

    j = 0  # variable pour les sujets
    compt_duree2 = [0, 0, 0, 0, 0, 0, 0]  # compteur rep longue pour chaque durée
    compt_duree1 = [0, 0, 0, 0, 0, 0, 0]  # bissection 1 / bissection 2

    for i in range(1, len(final_list)):
        if int(final_list[i][1]) == int(liste_sujets[j]):  # Si je suis encore au même sujet

            # Si j'arrive à la deuxième bissection, j'enregistre les valeurs de la première
            if final_list[i][48] == '2':
                compt_duree1 = compt_duree2
                compt_duree2 = [0, 0, 0, 0, 0, 0, 0]

            # Comptage
            if final_list[i][98] == '208':
                compt_duree2[0] += 1
            if final_list[i][98] == '272':
                compt_duree2[1] += 1
            if final_list[i][98] == '336':
                compt_duree2[2] += 1
            if final_list[i][98] == '400':
                compt_duree2[3] += 1
            if final_list[i][98] == '464':
                compt_duree2[4] += 1
            if final_list[i][98] == '528':
                compt_duree2[5] += 1
            if final_list[i][98] == '592':
                compt_duree2[6] += 1

        # Si j'ai fini les données d'un sujet
        else:
            # print("End sujet", liste_sujets[j], compt_duree1, compt_duree2)
            res = []  # tableau pour un sujet
            # Je remplis le tableau avec les données sous la forme
            # N°sujet N°Session Bissection 1/2 Durée NbLong NbCourt
            for k in range(0, 14):
                if k < 7:
                    res.append(
                        [final_list[i - 1][1], final_list[i - 1][2], 1, duree[k], compt_duree1[k], 10 - compt_duree1[k]])
                else:
                    res.append([final_list[i - 1][1], final_list[i - 1][2], 2, duree[k - 7], compt_duree2[k - 7],
                                10 - compt_duree2[k - 7]])

            # J'ajoute ces données à mon fichier
            with open(
                    '/Users/admin/OneDrive - Université de Bourgogne/Thèse/Bissolfzique/2021/Résultats/Data_trie.csv',
                    'a') as f:
                writer = csv.writer(f)
                writer.writerows(res)

            # Réinitialisation puis on passe au sujet suivant
            j = j + 1
            compt_duree2 = [0, 0, 0, 0, 0, 0, 0]
            compt_duree1 = [0, 0, 0, 0, 0, 0, 0]

    return liste_sujets




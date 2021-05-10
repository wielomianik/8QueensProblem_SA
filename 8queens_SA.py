import numpy as np
import time


def funkcjaCelu(hetmany, rozmiar, liczba_hetmanow):

    s = 0
    for i in range(rozmiar):    #kolumny
        for j in range(rozmiar):    #wiersze

            if hetmany[i][j] == 0:
                continue
            else:
                for k in range(rozmiar):
                    s += hetmany[i][k] + hetmany[k][j]
                s -= 2
                k = 1

                while i - k >= 0 and j - k >= 0:
                    s += hetmany[i - k][j - k]
                    k+=1
                k = 1

                while i + k <= rozmiar - 1 and j + k <= rozmiar - 1:
                    s += hetmany[i + k][j + k]
                    k += 1
                k = 1

                while i - k >= 0 and j + k <= rozmiar - 1:
                    s += hetmany[i - k][j + k]
                    k += 1
                k = 1

                while i + k <= rozmiar - 1 and j - k >= 0:
                    s += hetmany[i + k][j - k]
                    k += 1

    return s / liczba_hetmanow


def losowanieX(liczba_hetmanow, rozmiar):

    indeksy = [i for i in range(rozmiar ** 2)]
    hetmany = [0 for i in range(rozmiar ** 2)]

    unikalne_indeksy = []
    while len(unikalne_indeksy) != liczba_hetmanow:
        losowana = np.random.choice(indeksy)
        if losowana not in unikalne_indeksy:
            unikalne_indeksy.append(losowana)
    
    for element in unikalne_indeksy:
        hetmany[element] = 1

    hetmany = np.array(hetmany)
    hetmany = list(hetmany.reshape(rozmiar, rozmiar))
    hetmany = [list(i) for i in hetmany]

    return hetmany


def wybierzLosoweX(hetmany):
    
    '''print("\nRozwiązanie początkowe X: ")
    for row in hetmany:
        print(row)'''
    
    rozmiar_tablicy = len(hetmany)
    for i in range(rozmiar_tablicy - 1):
        for j in range(rozmiar_tablicy - 1):

            if hetmany[i][j] == 1:

                if hetmany[i][j + 1] == 0:

                    hetmany[i][j + 1] = 1
                    hetmany[i][j] = 0
                    break

                if hetmany[i][j - 1] == 0:

                    hetmany[i][j - 1] = 1
                    hetmany[i][j] = 0
                    break
                
                if hetmany[i + 1][j] == 0:
                    
                    hetmany[i + 1][j] = 1
                    hetmany[i][j] = 0
                    break

                if hetmany[i + 1][j - 1] == 0:

                    hetmany[i + 1][j - 1] = 1
                    hetmany[i][j] = 0
                    break
                    
                if hetmany[i + 1][j + 1] == 0:

                    hetmany[i + 1][j + 1] = 1
                    hetmany[i][j] = 0
                    break
                    
                if hetmany[i - 1][j] == 0:

                    hetmany[i - 1][j] = 1
                    hetmany[i][j] = 0
                    break
                    
                if hetmany[i][j + 1] == 0:

                    hetmany[i][j + 1] = 1
                    hetmany[i][j] = 0
                    break
                    
                if hetmany[i][j + 1] == 0:

                    hetmany[i][j + 1] = 1
                    hetmany[i][j] = 0
                    break
        
        else:
            continue
        break
                    

    '''print("\nLosowe rozwiązanie X' znajdujące się w pobliżu X: ")
    for row in hetmany:
        print(row)'''

    return hetmany


def funkcjaBoltzmanna(x, xPrim, temperatura):
    return np.e ** ((x - xPrim)/temperatura)


def przyjmowanieRozwiazania(prawdopodobienstwo):
    check = np.random.uniform(0,1)
    if check < prawdopodobienstwo:
        return True

            
start_time = time.time()

liczba_hetmanow_na_szachownicy = 5
rozmiar_szachownicy = 5
T = 4000
liczba_prób = 15
liczba_epok = 3000
wspolczynnik = 0.95
rozwiazania = []


for epoka in range(liczba_epok):
    for proba in range(liczba_prób):

        hetmany = losowanieX(liczba_hetmanow_na_szachownicy, rozmiar_szachownicy)
        hetmanyPrim = wybierzLosoweX(hetmany)
        avg_het = funkcjaCelu(hetmany, rozmiar_szachownicy, liczba_hetmanow_na_szachownicy)
        avg_het_prim = funkcjaCelu(hetmanyPrim, rozmiar_szachownicy, liczba_hetmanow_na_szachownicy)

        if avg_het_prim < avg_het:
            rozwiazania.append([avg_het_prim, hetmanyPrim])
        else:
            prob = funkcjaBoltzmanna(avg_het, avg_het_prim, T)
            check = przyjmowanieRozwiazania(prob)

            if check:
                rozwiazania.append([avg_het_prim, hetmanyPrim])
            else:
                rozwiazania.append([avg_het, hetmany])

    T *= wspolczynnik


for element in rozwiazania:
    if element[0] == 0:
        print("\nŚrednia: ", element[0])
        print("Oczekiwane rozmieszczenie hetmanów:")
        for row in element[1]:
            print(row)

print("--- %s seconds ---" % (time.time() - start_time))

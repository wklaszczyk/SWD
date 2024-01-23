import numpy as np

def licz_topsis(daneA, daneK, wektorWag):
    # Określenie wielkości problemu
    liczbaAlternatyw = len(daneA)
    iloscKryteriow = len(daneA[1])

    # Określenie ilości klas
    # Kod dostosowany do dwóch klas
    liczbaKlas = len(daneK)
    iloscWymiarow = len(daneK[0])
    iloscWymiarow -= 1

    # Sprawdzenie punktów alternatyw
    alternatywyOK = np.zeros((liczbaAlternatyw, 1))

    for i in range(liczbaAlternatyw):
        for j in range(2, iloscKryteriow) :
            if daneA[i][j] >= daneK[0][j-1] and daneA[i][j] <= daneK[1][j-1]:
                alternatywyOK[i][0] = i + 1
            else:
                alternatywyOK[i][0] = 0

    liczbaAlternatywTemp = np.count_nonzero(alternatywyOK)

    # Uzupełnienie macierzy decyzyjnej
    id = 0
    macierz_decyzyjna = np.zeros((liczbaAlternatywTemp, iloscKryteriow))

    for i in range(liczbaAlternatyw):
        if alternatywyOK[i][0] != 0:
            for j in range(2, iloscKryteriow + 2):
                macierz_decyzyjna[id][j - 2] = daneA[i][j]
            id += 1

    # Proces skalowania
    macierz_skalowana = np.zeros((liczbaAlternatywTemp, iloscKryteriow))

    for i in range(liczbaAlternatywTemp):
        for j in range(iloscKryteriow):
            if j < len(wektorWag):
                macierz_skalowana[i][j] = (macierz_decyzyjna[i, j] * wektorWag[j]) / np.sqrt(
                    np.sum((macierz_decyzyjna[:][j] ** 2)))
            else:
                macierz_skalowana[i][j] = 0.0

    # Wyznaczenie wektora idealnego oraz antyidealnego
    wektorIdealny = np.zeros(iloscKryteriow)
    wektorAntyIdealny = np.zeros(iloscKryteriow)

    for j in range(iloscKryteriow):
        wektorIdealny[j] = np.min(macierz_skalowana[:][j])
        wektorAntyIdealny[j] = np.max(macierz_skalowana[:][j])

    # Wyznaczenie odległości w przestrzeni euklidesowej
    odleglosci = np.zeros((liczbaAlternatywTemp, 2))

    for i in range(liczbaAlternatywTemp):
        sumaIdealny = 0
        sumaAntyIdealny = 0
        for j in range(iloscKryteriow):
            sumaIdealny += (macierz_skalowana[i, j] - wektorIdealny[j]) ** 2
            sumaAntyIdealny += (macierz_skalowana[i, j] - wektorAntyIdealny[j]) ** 2

        odleglosci[i][0] = np.sqrt(sumaIdealny)
        odleglosci[i][1] = np.sqrt(sumaAntyIdealny)

    # Uszeregowanie obiektów
    ranking = np.zeros((liczbaAlternatywTemp, 2))

    for i in range(liczbaAlternatywTemp):
        ranking[i][0] = i + 1
        ranking[i][1] = odleglosci[i][1] / (odleglosci[i, 0] + odleglosci[i, 1])

    return ranking

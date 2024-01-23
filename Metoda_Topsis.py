import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def licz_topsis(daneA, daneK, wektorWag):
    # Określenie wielkości problemu
    liczbaAlternatyw, _ = daneA.shape
    iloscKryteriow = daneA.shape[1]
    iloscKryteriow -= 2

    # Określenie ilości klas
    # Kod dostosowany do dwóch klas
    liczbaKlas, _ = daneK.shape
    _, iloscWymiarow = daneK.shape
    iloscWymiarow -= 1

    # Sprawdzenie punktów alternatyw
    alternatywyOK = np.zeros((liczbaAlternatyw, 1))

    for i in range(liczbaAlternatyw):
        for j in range(2, iloscKryteriow + 2):
            if daneA[i, j] >= daneK[0, j-1] and daneA[i, j] <= daneK[1, j-1]:
                alternatywyOK[i, 0] = i + 1
            else:
                alternatywyOK[i, 0] = 0

    liczbaAlternatywTemp = np.count_nonzero(alternatywyOK)

    # Uzupełnienie macierzy decyzyjnej
    id = 0
    macierz_decyzyjna = np.zeros((liczbaAlternatywTemp, iloscKryteriow))

    for i in range(liczbaAlternatyw):
        if alternatywyOK[i, 0] != 0:
            for j in range(2, iloscKryteriow + 2):
                macierz_decyzyjna[id, j - 2] = daneA[i, j]
            id += 1

    # Proces skalowania
    macierz_skalowana = np.zeros((liczbaAlternatywTemp, iloscKryteriow))

    for i in range(liczbaAlternatywTemp):
        for j in range(iloscKryteriow):
            if j < len(wektorWag):
                macierz_skalowana[i, j] = (macierz_decyzyjna[i, j] * wektorWag[j]) / np.sqrt(
                    np.sum((macierz_decyzyjna[:, j] ** 2)))
            else:
                macierz_skalowana[i, j] = 0.0

    # Wyznaczenie wektora idealnego oraz antyidealnego
    wektorIdealny = np.zeros(iloscKryteriow)
    wektorAntyIdealny = np.zeros(iloscKryteriow)

    for j in range(iloscKryteriow):
        wektorIdealny[j] = np.min(macierz_skalowana[:, j])
        wektorAntyIdealny[j] = np.max(macierz_skalowana[:, j])

    # Wyznaczenie odległości w przestrzeni euklidesowej
    odleglosci = np.zeros((liczbaAlternatywTemp, 2))

    for i in range(liczbaAlternatywTemp):
        sumaIdealny = 0
        sumaAntyIdealny = 0
        for j in range(iloscKryteriow):
            sumaIdealny += (macierz_skalowana[i, j] - wektorIdealny[j]) ** 2
            sumaAntyIdealny += (macierz_skalowana[i, j] - wektorAntyIdealny[j]) ** 2

        odleglosci[i, 0] = np.sqrt(sumaIdealny)
        odleglosci[i, 1] = np.sqrt(sumaAntyIdealny)

    # Uszeregowanie obiektów
    ranking = np.zeros((liczbaAlternatywTemp, 2))

    for i in range(liczbaAlternatywTemp):
        ranking[i, 0] = i + 1
        ranking[i, 1] = odleglosci[i, 1] / (odleglosci[i, 0] + odleglosci[i, 1])

    # Sortowanie rankingu po drugiej kolumnie (odległość od antyidealnego)
    ranking = ranking[ranking[:, 1].argsort()]

    # Wypisanie wyników
    print("Macierz Decyzyjna:\n", macierz_decyzyjna)
    print("Wektor Wag:\n", wektorWag)
    print("Macierz Skalowana:\n", macierz_skalowana)
    print("Wektor Idealny:\n", wektorIdealny)
    print("Wektor AntyIdealny:\n", wektorAntyIdealny)
    print("Odległości:\n", odleglosci)
    print("Ranking:\n", ranking)

    # Rysowanie
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')

    if iloscKryteriow == 2:
        ax.scatter(macierz_decyzyjna[:, 0], macierz_decyzyjna[:, 1], marker='+')
        ax.scatter(daneK[:, 1], daneK[:, 2], marker='o')
        ax.set_xlabel('Kryterium 1')
        ax.set_ylabel('Kryterium 2')
    else:
        ax.scatter(macierz_decyzyjna[:, 0], macierz_decyzyjna[:, 1], macierz_decyzyjna[:, 2], marker='+')
        ax.scatter(daneK[:, 1], daneK[:, 2], daneK[:, 3], marker='o')
        ax.set_xlabel('Kryterium 1')
        ax.set_ylabel('Kryterium 2')
        ax.set_zlabel('Kryterium 3')

    plt.grid(True)
    plt.show()

# Przykładowe dane do testów
daneA = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
daneK = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
wektorWag = [0.5, 0.3, 0.2]

# Wywołanie funkcji z przykładowymi danymi
licz_topsis(daneA, daneK, wektorWag)
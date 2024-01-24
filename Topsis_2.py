import numpy as np

def topsis(data, weights=None):
    # Znormalizuj dane
    norm_data = data / np.sqrt((data**2).sum(axis=0))

    # Zastosuj wagi
    if weights is None:
        weights = np.ones(data.shape[1])
    weighted_data = norm_data * weights

    # Oblicz idealne rozwiązanie pozytywne i negatywne
    ideal_positive = np.max(weighted_data, axis=0)
    ideal_negative = np.min(weighted_data, axis=0)

    # Oblicz odległości od idealnego rozwiązania pozytywnego i negatywnego
    dist_positive = np.sqrt(((weighted_data - ideal_positive)**2).sum(axis=1))
    dist_negative = np.sqrt(((weighted_data - ideal_negative)**2).sum(axis=1))

    # Oblicz wynik TOPSIS
    topsis_score = dist_negative / (dist_positive + dist_negative)

    # Zwróć ranking
    ranking = np.argsort(topsis_score)[::-1]
    return ranking

# Przykładowe dane
daneK = np.array([[1500,	4,	2,  6.39,   2, 3],
                  [1500,	4,	2,	6.08,	2, 2],
                  [1500,	4,	2,	27.50,	2, 1],
                  [3000,	3,	4,	7.81,	1, 3],
                  [3000,	3,	4,	9.24,	1, 2],
                  [3000,	3,	4,	55.71,	1, 1],
                  [4800,	5,	3,	9.97,	0, 3],
                  [4800,	5,	4,	14.52,	0, 2],
                  [4800,	5,	5,	107.14,	0, 1],
                  [1000,    1,	3,	10.30,  0, 4]])
wektorWag = [0.6, 0.5, 0.5, 0.9, 1, 3]

# Wywołaj funkcję TOPSIS
ranking = topsis(daneK, wektorWag)
print("Ranking:", ranking)
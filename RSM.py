def normalize_data(A):
    row_num = len(A)
    col_num = len(A[0])

    column_sum = [0 for i in range(col_num)]
    normalized_matrix = [None for x in range(row_num)]
    
    for row in A:
        for i, el in enumerate(row):
            column_sum[i] += el**2

    column_sum = [x**0.5 for x in column_sum]
    row = [None for i in range(col_num)]
    for n in range(row_num):
        for i, el in enumerate(A[n]):
            row[i] = el/column_sum[i]

        normalized_matrix[n] = tuple(x for x in row)
        
    return normalized_matrix

def reference_set_check(A):
    for a in A:
        if len(a) > 1:
            i = 0
            while i < len(a) - 1:
                if all(a[i][n] == a[i+1][n] for n in range(len(a[i]))):
                    a.pop(i)
                
                else:
                    i += 1

    #wewnętrzna niesprzeczność
    for n in range(len(A)):
        a = A[n]
        if len(a) > 1:
            for i in range(len(a)):
                for j in range(i+1, len(a)):
                    if all(a[i][z] >= a[j][z] for z in range(len(a[i]))):
                        if len(A) == n+1:
                            A.append([])

                        A[n+1].append(a[i])
                        a.pop(i)

                    elif all(a[i][z] <= a[j][z] for z in range(len(a[i]))):
                        if len(A) == n+1:
                            A.append([])

                        A[n+1].append(a[j])
                        a.pop(j)
    
    #wzajemna niesprzeczność
    for i in range(len(A)-1):
        for m in range(len(A[i+1])):
            ph = A[i+1][m]
            for n in range(len(A[i])):
                pl = A[i][n]
                #if pl[0] >= ph[0] and pl[1] >= ph[1]:
                if all(pl[z] >= ph[z] for z in range(len(pl))):
                    A[i+1].append(pl)
                    A[i].pop(n)

def RSM(A, U):
    #A - lista punktów odniesienia, U - lista alternatyw
    #zwraca posortowany ranking od najlepszego do najgorszego
    reference_set_check(A)
    nU = normalize_data(U)

    norm_to_input = {}
    for i in range(len(U)):
        norm_to_input[nU[i]] = U[i]

    f = {}
    for i in range(len(A) - 1):
        f[i] = []

    for u in nU:
        #wyznaczanie najbliższych zbiorów
        lower_sets = []
        higher_sets = []

        for a in A:
            lower_sets.append([])
            higher_sets.append([])
            for el in a:
                if all(u[z] == el[z] for z in range(len(u))):
                    break

                if all(u[z] >= el[z] for z in range(len(u))):
                    lower_sets[-1].append(el)

                if all(u[z] <= el[z] for z in range(len(u))):
                    higher_sets[-1].append(el)
        
        lower_sets = [x for x in lower_sets if x != []]
        higher_sets = [x for x in higher_sets if x != []]

        lower_set = lower_sets[-1]
        higher_set = higher_sets[0]

        #prostokąty
        volumes = {}
        volume_sum = 0
        f_val = 0

        for i in range(len(lower_set)):
            lp = lower_set[i]
            for j in range(len(higher_set)):
                hp = higher_set[j]
                V = 1
                edges = [abs(lp[z] - hp[z]) for z in range(len(lp))]

                for edge in edges:
                    V = V * edge

                volumes[(i, j)] = V
                volume_sum += V
        

        for i in range(len(lower_set)):
            lp = lower_set[i]
            for j in range(len(higher_set)):
                hp = higher_set[j]
                
                lower_dist = (sum([(lp[z] - u[z])**2 for z in range(len(hp))]))**0.5
                higher_dist = (sum([(hp[z] - u[z])**2 for z in range(len(hp))]))**0.5
                
                f_val += (volumes[(i, j)] / volume_sum) * higher_dist / (lower_dist + higher_dist)
            
        f[len(A) - len(lower_sets) - 1].append((norm_to_input[u], f_val))

    ranking = []

    for key in range(len(A)-2, -1, -1):
        temp = f[key]
        temp.sort(reverse = True, key = lambda x: x[1])

        for el in temp:
            ranking.append(el)

    return ranking

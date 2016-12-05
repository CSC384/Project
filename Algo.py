class Unsolvable(Exception):
    pass

def switches(vs):
    n, m = len(vs), len(vs[0])
    eqs = []
    for i in xrange(n):
        for j in xrange(m):
            eq = set()
            for d in xrange(-1, 2):
                if 0 <= i+d < n: eq.add((i+d)*m+j)
                if d != 0 and 0 <= j+d < m: eq.add(i*m+j+d)
            eqs.append([vs[i][j], eq])

    N = len(eqs)
    for i in xrange(N):
        for j in xrange(i, N):
            if i in eqs[j][1]:
                eqs[i], eqs[j] = eqs[j], eqs[i]
                break
        else:
            raise Unsolvable()
        for j in xrange(i+1, N):
            if i in eqs[j][1]:
                eqs[j][0] ^= eqs[i][0]
                eqs[j][1] ^= eqs[i][1]

    for i in xrange(N-1, -1, -1):
        for j in xrange(i):
            if i in eqs[j][1]:
                eqs[j][0] ^= eqs[i][0]
                eqs[j][1] ^= eqs[i][1]
    return [(i//m,i%m) for i, eq in enumerate(eqs) if eq[0]]

print(switches(([1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0])))
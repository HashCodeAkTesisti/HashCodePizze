import numpy as np

def read_file(filename):
    """
    B number of different books
    L number of libraries
    D number of available days
    S array of score given by books
    DS array length L: day to signup library j
    BD array length L: num books can be scanned in one day from library j
    BL dictionary of sets: set of books available in library key
    """
    with open(filename, 'r') as infile:
        f = infile.readlines()

    # 1st line
    B, L, D = [int(x) for x in f[0].split(' ')]

    S = np.array([int(x) for x in f[1].split(' ')])

    # L section
    line = 2
    DS = np.zeros(L)
    BD = np.zeros(L)
    BL = {}
    for j in range(L):
        (n_books, DS[j], BD[j]) = [int(x) for x in f[line].split(' ')]
        line += 1
        BL[j] = set([int(x) for x in f[line].split(' ')])
        line += 1
    return B, L, D, S, DS, BD, BL


def write_file(solution, filename):
    with open(filename, 'w') as outfile:
        # DO STUFF
        pass

def scorer(solution):
    return 0

def check_constraint(solution):
    return True



if __name__ == '__main__':
    files = ['example']

    algos = []
    tot_score = 0

    for f in files:
        B, L, D, S, DS, BD, BL = read_file("input/{}.txt".format(f))
        breakpoint()

        scores = {}
        solutions = {}
        for alg in algos:
            solution = alg(B, L, D, S, DS, BD, BL)
            scores[alg] = scorer(solution)
            solutions[alg] = solution
            print("{:20s}{:50s}{}".format(f, alg.__name__, scores[alg]))

        # search for best
        best_alg = sorted(scores.items(), key=lambda x: -x[1])[0][0]
        print("Using {}\n".format(best_alg.__name__))
        tot_score += scores[best_alg]
        solution = solutions[best_alg]
        write_file(solution, "./output{}.txt".format(f))


    print("Final score is {} ".format(tot_score))

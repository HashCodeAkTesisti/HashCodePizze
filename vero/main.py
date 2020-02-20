import numpy as np

def read_file(filename):
    """
    B number of different books
    L number of libraries
    D number of available days
    DS array length L: day to signup library j
    BD array length L: num books can be scanned in one day from library j
    BL dictionary of sets: set of books available in library key
    """
    with open(filename, 'r') as infile:
        f = infile.readlines()

    # 1st line
    B, L, D = [int(x) for x in f[0].split(' ')]

    # L section
    line = 1
    DS = np.zeros(L)
    BD = np.zeros(L)
    BL = {}
    for j in range(L):
        (n_books, DS[j], BD[j]) = [int(x) for x in f[line].split(' ')]
        line += 1
        BL[j] = set([int(x) for x in f[line].split(' ')])
        line += 1
    return B, L, D, DS, BD, BL







def write_file(solution, filename):
    with open(filename, 'w') as outfile:
        # DO STUFF
        pass

def scorer(solution):
    return 0

def check_constraint(solution):
    return True


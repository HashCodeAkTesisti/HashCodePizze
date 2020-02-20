import numpy as np
from stecer import stecer1
from stev import stev

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
    nnz = sum([1 for l in solution if len(solution[l]) > 0])
    with open(filename, 'w') as outfile:
        outfile.write("{}\n".format(nnz))
        for library in solution:
            if len(solution[library]) == 0:
                continue
            outfile.write("{} {}\n".format(library, len(solution[library])))
            for book in solution[library]:
                outfile.write("{} ".format(book))
            outfile.write('\n')


def scorer(solution, D, S, DS, BD):
    score = 0
    scanned_books = set()
    days = {}
    signup_day = 0
    for library in solution:
        signup_day += DS[library]
        days[library] = signup_day
        scanned = 0
        for book in solution[library]:
            if days[library] >= D:
                print('Books not scanned, out of time')
                break
            if book not in scanned_books:
                score += S[book]
                scanned_books.add(book)
            else:
                print('Scanning the same book')
            scanned += 1
            #print(scanned)
            if scanned == BD[library]:
                days[library] += 1
                scanned = 0
    return score

def check_constraint(solution):
    return True

def example(B, L, D, S, DS, BD, BL):
    solution = {}
    solution[1] = [5,2,3]
    solution[0] = [0,1,2,3,4]
    return solution



if __name__ == '__main__':
    files = ['a_example',
             'b_read_on',
             'c_incunabula',
             'd_tough_choices',
             'e_so_many_books',
             'f_libraries_of_the_world'
             ]
    algos = [stecer1,
             #stev
             ]
    tot_score = 0
    maximum = 0

    for f in files:
        B, L, D, S, DS, BD, BL = read_file("input/{}.txt".format(f))

        scores = {}
        solutions = {}
        for alg in algos:
            solution = alg(B, L, D, S, DS, BD, BL)
            check_constraint(solution)
            scores[alg] = scorer(solution, D, S, DS, BD)
            solutions[alg] = solution
            maximum += sum(S)
            print("{:20s}{:30s}{}/{}".format(f, alg.__name__, scores[alg],
                                             maximum))

        # search for best
        best_alg = sorted(scores.items(), key=lambda x: -x[1])[0][0]
        print("Using {}\n".format(best_alg.__name__))
        tot_score += scores[best_alg]
        solution = solutions[best_alg]
        write_file(solution, "./output/{}.txt".format(f))


    print("Final score is {}/{}".format(tot_score, maximum))

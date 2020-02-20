import numpy as np
from tqdm import tqdm

def stecer1(B, L, D, S, DS, BD, BL):
    pot_scores = compute_potential_library_scores(B, L, D, S, DS, BD, BL)
    sorted_libraries = np.argsort(-pot_scores)
    solution = {}
    day = 0
    scanned_books = set()
    sorted_books = list(np.argsort(-S))

    for library in tqdm(sorted_libraries):
        day += DS[library]
        if day >= D:
            # time up
            break

        solution[library] = []
        num_readable_books = int(np.floor((D - day) / BD[library]))

        best_books = [book for book in sorted_books if book in BL[library]]
        solution[library] = [book for book in
                             best_books[:num_readable_books]
                             if book not in scanned_books]
        scanned_books.update(solution[library])
        if len(solution[library]) == 0:
            del solution[library]
            day -= DS[library]

    return solution


def compute_potential_library_scores(B, L, D, S, DS, BD, BL):
    potential_scores = np.zeros(L)
    for library in range(L):
        potential_scores[library] = (np.sum(S[list(BL[library])]) * BD[library]
                                     * (D - DS[library]))
    return potential_scores

def compute_potential_library_scores_2(B, L, D, S, DS, BD, BL, day, scanned):
    potential_scores = np.zeros(L)
    for library in range(L):
        score = np.sum(S[[b for b in BL[library] if b not in scanned]])
        potential_scores[library] = (score * BD[library] * (D - DS[library] - day))
    return potential_scores

def stecer2(B, L, D, S, DS, BD, BL):
    solution = {}
    day = 0
    scanned_books = set()
    sorted_books = tuple(np.argsort(-S))

    changed = True
    while changed and day <= D:
        if day / D * 100 % 10 == 0:
            print(day/D)
        changed = False
        pot_scores = compute_potential_library_scores_2(B, L, D, S, DS, BD, BL,
                                                        day, scanned_books)
        sorted_libraries = np.argsort(-pot_scores)

        for library in sorted_libraries:
            if library in solution:
                continue
            if DS[library] + day > D:
                continue

            day += DS[library]

            solution[library] = []
            num_readable_books = int(np.floor((D - day) / BD[library]))

            best_books = [book for book in sorted_books if book in BL[library]]
            solution[library] = [book for book in
                                 best_books[:num_readable_books]
                                 if book not in scanned_books]
            scanned_books.update(solution[library])
            changed = True
            break
            if len(solution[library]) == 0:
                del solution[library]
                day -= DS[library]
                changed = False

    return solution


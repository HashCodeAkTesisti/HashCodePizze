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
                                     / DS[library])
    return potential_scores

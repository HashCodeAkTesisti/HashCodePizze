import numpy as np

def stecer1(B, L, D, S, DS, BD, BL):
    pot_scores = compute_potential_library_scores(B, L, D, S, DS, BD, BL)
    sorted_libraries = np.argsort(-pot_scores)
    solution = {}
    day = 0
    scanned_books = set()

    for library in sorted_libraries:
        day += DS[library]
        if day >= D:
            # time up
            break

        solution[library] = []
        num_readable_books = int(np.floor((D - day) / BD[library]))
        sorted_books = np.argsort(-S[list(BL[library])])
        solution[library] = [book for book in
                             sorted_books[:num_readable_books]
                             if book not in scanned_books]
        scanned_books.update(solution[library])

    return solution


def compute_potential_library_scores(B, L, D, S, DS, BD, BL):
    potential_scores = np.zeros(L)
    for library in range(L):
        potential_scores[library] = np.sum(S[list(BL[library])])
    return potential_scores

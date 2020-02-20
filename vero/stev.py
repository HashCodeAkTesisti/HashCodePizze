import numpy as np

from queue import Queue
from tqdm import trange


def stev(B, L, D, S, DS, BD, BL):
    libraries = np.argsort(DS)
    lib_index = 0
    end_sign = -1
    scanned_books = {l: 0 for l in range(L)}
    all_scanned_b = np.zeros(B)
    signed_lib = []
    sol = {}

    for d in trange(D):
        if end_sign == -1:
            end_sign = d + DS[libraries[lib_index]]
        elif end_sign == d:
            end_sign = -1
            lib_index += 1
            signed_lib.append(libraries[lib_index - 1])
            sol[libraries[lib_index - 1]] = []
        for l in libraries[:lib_index]:
            que = Queue(maxsize=B)
            for b in list(BL[l])[scanned_books[l]:int(BD[l])]:
                que.put(b)
            aux = scanned_books[l] + BD[l]
            i = 0
            while not que.empty():
                if i == BD[l]:
                    break
                b = que.get()
                a = 1
                if all_scanned_b[b] == 0:
                    sol[l].append(b)
                    all_scanned_b[b] = 1
                    scanned_books[l] += 1
                else:
                    # the book is already present, we take the next one to scan
                    if aux < len(BL[l]):
                        que.put(list(BL[l])[int(aux)])
                        aux += 1
    return sol

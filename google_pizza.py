import random
import numpy as np
from itertools import chain, combinations

def read_file(filename):
    """ Read submission file, return
    M: maximum number of slices
    N: number of tipes
    S: list of slice per type
    """
    with open(filename, 'r') as infile:
        f = infile.readlines()

    m, n = [int(x) for x in f[0].split(' ')]
    s = [int(x) for x in f[1].split(' ')]
    return m, n, s


def writer(selected, filename):
    with open(filename, 'w') as outfile:
        outfile.write("{}\n".format(len(selected)))
        for sel in selected:
            outfile.write("{} ".format(sel))
        outfile.write("\n")


def scorer(wanted, selected, s):
    ordered_slices = 0
    seen = set()
    for pizza_type, pizza_slices in enumerate(s):
        if pizza_type in seen:
            raise Exception("Cannot order 2 times same pizza")
        if pizza_type in selected:
            ordered_slices += pizza_slices
            seen.add(pizza_type)

    if ordered_slices > wanted:
        raise Exception("ERROR: too many slices ordered")
    #print("ordered {} slices, we wanted {}".format(ordered_slices, wanted))
    #print("optimality is {}".format(100*ordered_slices/wanted))
    return ordered_slices


def stupid_solver(max_slices, s):
    """ Start from first element, add until exceed M
    return list of selected indices of s.
    """
    selected = []
    tot_slices = 0
    for pizza_type, pizza_slices in enumerate(s):
        if pizza_slices + tot_slices <= max_slices:
            tot_slices += pizza_slices
            selected.append(pizza_type)
    return selected


def reverse_stupid_solver(max_slices, s):
    """ start from big pizzas
    """
    selected = []
    tot_slices = 0
    for pizza_type, pizza_slices in enumerate(s[::-1]):
        if pizza_slices + tot_slices <= max_slices:
            tot_slices += pizza_slices
            selected.append(pizza_type)
    return selected


def randomized_stupid_solver(max_slices, s):
    """ Bad results
    """
    rounds = 100
    selections = {}
    tot_slices = {}
    s_shuffle = s.copy()

    for rn in range(rounds):
        random.shuffle(s_shuffle)
        selections[rn] = []
        tot_slices[rn] = 0
        for pizza_type, pizza_slices in enumerate(s_shuffle):
            if pizza_slices + tot_slices[rn] <= max_slices:
                tot_slices[rn] += pizza_slices
                selections[rn].append(pizza_type)

    # now look for best shuffle
    best = sorted(tot_slices.items(), key=lambda x: -x[1])[0][0]
    return selections[best]

def refined_stupid_solver(max_slices, s):
    return refine_selection(stupid_solver(max_slices, s), max_slices, s)


def refine_selection(selection, max_slices, s):
    """ Try to improve selection by making space for non-included pizzas """
    MAX_ITERS = 8  # refinement iterations
    SUBSET_L = 5  # max length of subsets for candidate removal
    slices = np.array(s)

    # try to improve untill there is space or we did not find a way to improve
    available_space = max_slices - sum(slices[selection])
    changed = True
    iters = 0
    while available_space > 0 and changed and iters < MAX_ITERS:
        iters += 1
        changed = False

        unordered_pizzas = set(range(len(s))) - set(selection)
        for pizza_type in unordered_pizzas:
            # TODO: any way to prune this?

            adding_slices = slices[pizza_type]
            if changed:
                break # we need to recompute unordered_pizzas

            # how much space do we need to create?
            remove_slices = adding_slices - available_space

            # we can simply insert this pizza
            if remove_slices <= 0:
                selection.append(pizza_type)
                changed = True
                available_space -= adding_slices
                continue

            # try to make space for this pizza by removig as less as possible
            current_slices = sum(slices[selection])
            removal_candidates = set(selection)

            # prune the removal set
            pruning = set()
            for candidate in removal_candidates:
                if (-slices[candidate] + adding_slices) <= 0:
                    pruning.add(candidate)
            for prune in pruning:
                removal_candidates.remove(prune)

            bad_subsets = set()
            for candidate_removal_set in arrays_and_powerset(removal_candidates,
                                                             SUBSET_L):
                skip = False
                for bad in bad_subsets:
                    if all([b in candidate_removal_set for b in bad]):
                        skip = True
                        break
                if skip:
                    continue

                candidate_slices = sum(slices[list(candidate_removal_set)])

                if candidate_slices < remove_slices:
                    # not enough
                    continue

                score_delta = -candidate_slices + adding_slices
                if score_delta <= 0:
                    # not convenient
                    bad_subsets.add(candidate_removal_set)
                    continue

                # score delta is positive, make the change (even if it's not
                # the optimal change, checking all is too much
                for rem_pizza in candidate_removal_set:
                    selection.remove(rem_pizza)
                    available_space += slices[rem_pizza]
                selection.append(pizza_type)
                available_space -= adding_slices
                changed = True
                break

            # if we did not break then we did not found any candidate set with
            # positive delta, check another type of pizza

    return selection

def arrays_and_powerset(s, subset_l):
    return chain.from_iterable([subarrays(s), powerset(s, subset_l)])


def subarrays(s):
    l = tuple(s)
    for idx1 in range(len(l)):
        idx2 = idx1 + 1  # 1-length done in subsets
        while idx2 < len(l):
            yield l[idx1:idx2+1]
            idx2 += 1


def powerset(s, l=None):
    if l is not None:
        lengths = range(min(l, len(s)-1))
    else:
        lengths = range(len(s)-1)
    return chain.from_iterable(combinations(s, r+1) for r in lengths)


def bruteforce(max_slices, s):
    slices = np.array(s)
    best_num = 0
    best_order = []
    for subset in powerset(range(len(s))):
        ordering = list(subset)
        score = sum(slices[ordering])
        if score > max_slices:
            continue
        if score == max_slices:
            return ordering
        if score > best_num:
            best_num = score
            best_order = ordering
    return best_order


def knapsack(max_slices, s):
    W = max_slices  # capacity of knapsack is number of pizza slices
    wt = s  # a pizza weights the number of slices
    val = s  # value == weight
    n = len(val)

    K_new = np.zeros(W+1, dtype=np.uint8)
    sel_new = np.zeros((W+1, len(val)), dtype=np.bool) # bool is still a byte
    # we need to reduce the first idx, but I don't think it's feasible

    # Build table K[][] in bottom up manner
    for i in range(n+1):  # all items (iterations)
        K_old = K_new
        K_new = np.zeros(W+1, dtype=np.uint8)
        sel_old = sel_new
        sel_new = np.zeros((W+1, len(val)), dtype=np.bool)

        for w in range(W+1):  # increase weigth
            if i == 0 or w == 0:
                continue

            elif wt[i-1] <= w:  # we can pick this
                val_inc = val[i-1] + K_old[w-wt[i-1]]
                val_non_inc = K_old[w]
                if val_inc > val_non_inc:  # should we pick it?
                    K_new[w] = val_inc
                    sel_new[w, :] = sel_old[w-wt[i-1], :]
                    sel_new[w, i-1] = 1

                    if K_new[w] == W:  # early exit
                        return np.where(sel_new[w])[0]

                else:  # don't pick
                    K_new[w] = val_inc
                    sel_new[w, :] = sel_old[w, :]

            else:  # not pickable
                K_new[w] = K_old[w]
                sel_new[w, :] = sel_old[w, :]

    return np.where(sel_new[W, :])[0]

def knapSack_onlyScore(max_slices, s):
    W = max_slices  # capacity of knapsack is number of pizza slices
    wt = s  # a pizza weights the number of slices
    val = s  # value == weight
    n = len(val)

    K_new = np.zeros(W+1, dtype=np.uint8)

    # Build table K[][] in bottom up manner
    for i in range(n+1):  # all items (iterations)
        K_old = K_new
        K_new = np.zeros(W+1, dtype=np.uint8)

        for w in range(W+1):  # increase weigth
            if i == 0 or w == 0:
                continue

            elif wt[i-1] <= w:  # we can pick this
                val_inc = val[i-1] + K_old[w-wt[i-1]]
                val_non_inc = K_old[w]
                if val_inc > val_non_inc:  # should we pick it?
                    K_new[w] = val_inc

                    if K_new[w] == W:  # early exit
                        return K_new[w]

                else:  # don't pick
                    K_new[w] = val_inc

            else:  # not pickable
                K_new[w] = K_old[w]

    return K_new[W]




if __name__ == '__main__':
    files = [
        "a_example",
        "b_small",
        "c_medium",
        "d_quite_big",
        "e_also_big"]

    algos = [stupid_solver, reverse_stupid_solver, knapsack,
             refined_stupid_solver]
    tot_wanted = 0
    tot_score = 0

    for f in files:
        m, n, s = read_file("{}.in".format(f))
        tot_wanted += m

        scores = {}
        selections = {}
        for alg in algos:
            if alg in[bruteforce, knapsack] and f in ["d_quite_big", "e_also_big"]:
                continue
            selected = alg(m, s)
            scores[alg] = scorer(m, selected, s)
            selections[alg] = selected
            print("{:20s}{:50s}{}/{}".format(f, alg.__name__, scores[alg],
                                                m))

        # search for best
        best_alg = sorted(scores.items(), key=lambda x: -x[1])[0][0]
        print("Using {}\n".format(best_alg.__name__))
        tot_score += scores[best_alg]
        selected = selections[best_alg]
        writer(selected, "{}.out".format(f))


    print("Final score is {} over {}: {}%".format(tot_score, tot_wanted,
                                                  100*tot_score/tot_wanted))

import sys
import numpy as np

lights = []
buttons = []
joltages = []

while True:
    line = sys.stdin.readline().rstrip()

    if line == "":
        break

    comps = line.split()

    lights.append(np.array([state == "#" for state in comps[0][1:-1]]))
    toggle = np.zeros((lights[-1].shape[0], len(comps) - 2), dtype=bool)
    for i, button in enumerate(comps[1:-1]):
        for idx in button[1:-1].split(","):
            toggle[int(idx), i] = 1

    buttons.append(toggle)
    joltages.append(np.array([int(j) for j in comps[-1][1:-1].split(",")]))


def array(*args, **kwargs):
    return np.array(*args, **kwargs, dtype=np.uint8) % 2


def zeros(*shape):
    return np.zeros(shape, dtype=np.uint8)


def pivot(matrix, vec):
    i = -1
    for i, v in enumerate(matrix[:, 0]):
        if v == 1:
            break
    assert i != -1

    if i == 0:
        return

    temp = array(matrix[i])
    matrix[i] = matrix[0]
    matrix[0] = temp

    temp = int(vec[i])
    vec[i] = vec[0]
    vec[0] = temp


def row_reduce(matrix, vec):
    # n is output dimension
    # m is input dimension
    n, m = matrix.shape
    assert n == len(vec)

    offset = 0
    i = 0
    while i - offset < n:
        if i >= m:
            break
        submatrix = matrix[i - offset :, i:]
        subvec = vec[i - offset :]
        pivot(submatrix, subvec)
        if submatrix[0, 0] == 0:
            offset += 1
            i += 1
            continue

        for j, row in enumerate(submatrix[1:]):
            if row[0] != 1:
                continue
            row[:] += submatrix[0]
            row[:] %= 2
            subvec[j + 1] += subvec[0]
            subvec[j + 1] %= 2

        i += 1

    # otherwise system is overdetermined with no solution
    assert np.all(vec[m:] == 0)

    return matrix[:m], vec[:m]


def solve(triangular, b):
    n, m = triangular.shape
    assert n == len(b)

    solution = zeros(m)
    n_done = 0
    null_space = []

    for i, row in enumerate(triangular[::-1]):
        i = n - 1 - i
        j = 0
        for j, val in enumerate(row[i:]):
            if val == 1:
                j -= 1
                break
        j += 1

        new_null_space_vecs = range(j + i + 1, m - len(null_space) - n_done)

        for x in new_null_space_vecs:
            null_space.append(zeros(m))
            null_space[-1][x] = 1

        rem = row[i + 1 + j :]
        if i + j < m - n_done:
            n_done += 1
            if len(rem) == 0:
                solution[i + j] = b[i]
            else:
                solution[i + j] = (b[i] + np.sum(rem * solution[-len(rem) :])) % 2
                for v in null_space:
                    v[i + j] = np.sum(v[-len(rem) :] * rem) % 2

    assert np.all(b == ((triangular @ solution) % 2))
    null_space = array(null_space).T
    if len(null_space) == 0:
        null_space = zeros(m, 0)
    assert np.all((triangular @ null_space) % 2 == 0)

    return (solution, null_space)


def gauss(buttons, initial_lights):
    """Computes solution vector and null space of matrix `buttons` with respect to vector `initial_lights`"""
    matrix = array(buttons)
    vec = array(initial_lights)
    assert matrix.shape[0] == len(vec)

    triangular, b = row_reduce(matrix, vec)

    return solve(triangular, b)


sol1 = 0


for bts, initial_lights in zip(buttons, lights):
    sol, null_space = gauss(bts, initial_lights)
    lowest = np.sum(sol)
    best = array(sol)
    for i in range(2 ** null_space.shape[1]):
        possibility = array(sol)
        for vec in null_space.T:
            if i % 2 == 1:
                possibility += vec
                possibility %= 2
            i >>= 1
        value = np.sum(possibility)
        if value < lowest:
            lowest = value
            best = possibility

    print(sol, lowest)
    sol1 += lowest

print(f"\nSolution 1: {sol1}")

import sys

devices: dict[str, set[str]] = {}


while True:
    line = sys.stdin.readline().rstrip()

    if line == "":
        break

    source, targets = line.split(":")

    devices[source] = set(target for target in targets.strip().split())


cache: dict[str, int] = {"out": 1}


def find_n_paths(device: str) -> int:
    if device in cache:
        return cache[device]

    n = 0
    for target in devices[device]:
        n += find_n_paths(target)

    cache[device] = n
    return n


cache_strict: dict[tuple[str, bool, bool], int] = {
    ("out", True, True): 1,
    ("out", False, False): 0,
    ("out", False, True): 0,
    ("out", True, False): 0,
}


def find_n_paths_strict(device: str, fft_visited: bool, dac_visited: bool) -> int:
    if (device, fft_visited, dac_visited) in cache_strict:
        return cache_strict[(device, fft_visited, dac_visited)]

    _fft_visited = device == "fft" or fft_visited
    _dac_visited = device == "dac" or dac_visited
    n = 0
    for target in devices[device]:
        n += find_n_paths_strict(target, _fft_visited, _dac_visited)

    cache_strict[(device, fft_visited, dac_visited)] = n
    return n


if len(sys.argv) < 2 or sys.argv[1] == "1":
    sol1 = find_n_paths("you")
    print(f"Solution 1: {sol1}")
if len(sys.argv) < 2 or sys.argv[1] == "2":
    sol2 = find_n_paths_strict("svr", False, False)
    from pprint import pprint

    pprint(cache_strict)
    print(len(cache_strict))
    print(f"Solution 2: {sol2}")

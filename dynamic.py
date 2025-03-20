from common import parse, taxicab, check, go_around_house
from itertools import permutations


def dynamic(strArr):
    charlie, house, foods = parse(strArr)
    n = len(foods)
    e = {}
    h = {}
    for i, j in filter(
        lambda x: x[0] < x[1],
        permutations(range(n), 2)
    ):
        # print(f"i: {i}, j: {j}")
        e[(i, j)] = e[(j, i)] = taxicab(foods[i], foods[j])
        h[(i, j)] = h[(j, i)] = go_around_house(
            foods[i], foods[j], house
        )

    def get_total(perm: tuple[int, ...]) -> int:
        total = (
            taxicab(charlie, foods[perm[0]]) +
            taxicab(foods[perm[-1]], house)
        )
        for i, j in zip(perm, perm[1:]):
            total += e[(i, j)] + h[(i, j)]
        return total
    return min(get_total(perm)
               for perm in permutations(range(n)))


if __name__ == "__main__":
    check(dynamic)

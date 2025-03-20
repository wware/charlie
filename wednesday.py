from itertools import permutations
from common import parse, taxicab, check, Location, go_around_house


def wednesday(strArr):
    charlie, house, foods = parse(strArr)

    def get_total(perm: tuple[Location, ...]) -> int:
        # Start from Charlie to first food
        current = charlie
        total = taxicab(current, perm[0])
        needs_detour = go_around_house(current, perm[0], house)
        if needs_detour:
            total += 2
        current = perm[0]
        
        # Go through each food item
        for food2 in perm[1:]:
            dist = taxicab(current, food2)
            needs_detour = go_around_house(current, food2)
            if needs_detour:
                dist += 2
            total += dist
            current = food2
        
        # Finally go to house
        dist = taxicab(current, house)
        needs_detour = go_around_house(current, house, house)
        if needs_detour:
            dist += 2
        final_total = total + dist
        return final_total

    all_totals = [get_total(perm) for perm in permutations(foods)]
    return min(all_totals)


if __name__ == "__main__":
    check(wednesday)

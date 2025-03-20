from common import parse, taxicab, check, go_around_house


def solve_bitmask(strArr):
    charlie, house, foods = parse(strArr)
    n = len(foods)
    # dp[(pos, mask)] = min cost to collect remaining
    # foods and reach the house
    dp = {}
    
    def solve(pos: int, collected: int) -> int:
        # If we've collected all foods, return cost to house
        if collected == (1 << n) - 1:
            return taxicab(foods[pos], house)
            
        # Check if we've already solved this state
        state = (pos, collected)
        if state in dp:
            return dp[state]
            
        # Try collecting each uncollected food
        result = None
        for next_pos in range(n):
            if not (collected & (1 << next_pos)):
                dist = taxicab(foods[pos], foods[next_pos])
                # Add penalty if we need to go around house
                if go_around_house(foods[pos], foods[next_pos], house):
                    dist += 2
                # Recursively solve for new state
                candidate = dist + solve(
                    next_pos,
                    collected | (1 << next_pos)
                )
                result = (
                    candidate if result is None
                    else min(result, candidate)
                )
                
        dp[state] = result
        return result
    
    # Try starting with each food as first collection
    if n == 0:
        return taxicab(charlie, house)
        
    return min(
        taxicab(charlie, foods[first]) + solve(first, 1 << first)
        for first in range(n)
    )


if __name__ == "__main__":
    check(solve_bitmask)

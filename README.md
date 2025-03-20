# Further work on the "Charlie the Dog" Problem

This repository contains three solutions to the "Charlie the Dog" problem.
In increasing order of sophistication, the solutions are:

- `wednesday.py`, a brute force solution that uses permutations to try every
possible order of collecting the food items, similar to my interview
solution
- `dynamic.py`, a dynamic programming solution that uses a dictionary to store
the distances between each pair of food locations, and whether a trip from one
food location to another requires a detour around the house
- `bitmask.py`, a solution that uses a bitmask to represent the current state
of the problem. See https://algo.monster/liteproblems/847 for a detailed
explanation.

## Problem statement

Charlie the dog moves around a 4x4 grid. The grid contents are
represented by four strings of four characters each. The characters
are:

- `C` - Charlie the dog
- `F` - Food
- `H` - House

Charlie starts at a specified location in the grid. He needs to collect all
the food in the grid and return to the house. He can only move up, down,
left, or right. If any food remains, he cannot enter the grid square with
the house. The goal is to find the shortest path for Charlie to collect all
the food and return to the house.

In my interview on Wednesday, I was able to solve the problem in
O(n! n) time, where n is the number of food locations. For very small n,
this is practical, but for larger n, it becomes infeasible.

In the spirit of dynamic programming, I've implemented a solution that uses
more memory to speed up the computation. Two dictionaries are used to store
the number of steps required to move from one food location to another, and
whether a trip from one food location to another requires a detour around
the house.

## Kibitzing from Cursor IDE's AI helper

The `wednesday.py` code uses `itertools.permutations(foods)` to try every
possible order of collecting the food items. For n food items:

1. Number of permutations = n!
2. For each permutation, we calculate the total distance by:
   - Moving from Charlie to first food: O(1)
   - Moving through each food item: O(n)
   - Moving to house: O(1)

So the overall complexity is O(n! n).

Even though n (number of food items) is small in this case, the factorial growth makes this quite expensive as n increases:

- n=2: 2! 2 = 4 operations
- n=3: 6 3 = 18 operations
- n=4: 24 4 = 96 operations
- n=5: 120 5 = 600 operations
- n=8: 40,320 8 = 322,560 operations

This is why the problem is constrained to a small number of food items. The factorial growth would make it impractical for larger numbers of food items.

### Is the solution in `dynamic.py` more time-efficient?

Looking at `dynamic.py`, it's actually still O(n! n) complexity like the first solution, as it's still using permutations to try every possible order of food collection.

The main optimization in `dynamic.py` is that it pre-computes and caches two things in dictionaries:

- e: The distances between each pair of food locations
- h: Whether going between each pair of food locations requires going around the house

This means that during the permutation evaluation:

- Instead of calculating distances each time with `taxicab()`
- Instead of checking `go_around_house()` each time

These values are looked up in O(1) time from the dictionaries.

The preprocessing step to build these dictionaries is O(n²), but this
is dominated by the O(n! n) of the main algorithm.

So while this solution is more efficient in practice (fewer repeated calculations), its big-O complexity remains the same as the original solution. For truly better time complexity, we'd need a fundamentally different approach, like:

- Dynamic programming with state compression
- Branch and bound
- A search with admissible heuristics

### Dynamic Programming with State Compression

The key insight is that we can represent the "state" of our problem as:

- Current position
- Set of foods we've collected so far (can be represented as a bit mask)

For example, with 3 foods, state (pos=2, collected=101) means:

- We're at food position 2
- We've collected foods 0 and 2 (binary 101)

The recurrence relation would be:

- Time complexity: O(n 2ⁿ) where n is number of foods
- 2ⁿ possible subsets of foods
- n possible current positions

Much better than O(n! n), as 2ⁿ grows slower than n!

### Branch and Bound - I haven't tried this yet

Similar to the permutation approach but we prune paths that can't be optimal

At each step, we:

- Calculate a lower bound on the best possible solution from this state
- If this bound is worse than our best solution so far, skip this branch

For this problem, a lower bound could be:

- Current distance traveled +
- Minimum spanning tree distance of remaining foods +
- Distance from closest remaining food to house

Time complexity is still O(n!) in worst case, but in practice much faster due to pruning.

The key advantages of DP over the permutation approach:

- Better theoretical complexity (2ⁿ vs n!)
- Avoids recalculating overlapping subproblems
- Can be extended to handle larger instances

### With state compression, don't you still need the permutation operation to scan thru all the possible bit masks?

The key insight is that we don't need permutations at all with the bit mask approach. Instead of generating permutations, we:

- Use bitwise operations to check which foods are available
- Try collecting any uncollected food

The key differences from permutations:

- We don't care about the order we discovered the foods, just which ones we have
- We build solutions incrementally, reusing overlapping subproblems
- Each state transition only looks at O(n) possible next moves
- So while we do examine all 2ⁿ possible subsets eventually, we:
  - Don't generate them up front
  - Don't care about their order
  - Reuse calculations when multiple paths lead to the same state

This is why it's O(n 2ⁿ) rather than O(n!): we're working with combinations (which
foods do we have?) rather than permutations (in what order did we get them?). The
full bitmask solution is in `bitmask.py`.

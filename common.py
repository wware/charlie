from pydantic import BaseModel
from typing import Iterator, List, Optional

ROWLIMIT = 4
COLLIMIT = 4


class Location(BaseModel):
    row: int
    col: int

    def neighbors(self) -> Iterator["Location"]:
        for r in (self.row - 1, self.row + 1):
            if 0 <= r < ROWLIMIT:
                yield Location(row=r, col=self.col)
        for c in (self.col - 1, self.col + 1):
            if 0 <= c < COLLIMIT:
                yield Location(row=self.row, col=c)

    @property
    def params(self) -> tuple[int, int]:
        return (self.row, self.col)


INVALID, OKAY, FINISHED = range(3)


class Config(BaseModel):
    charlie: Location
    house: Location
    foods: List[Location]
    parent: Optional["Config"] = None

    def valid(self) -> int:
        if len(self.foods) == 0:
            if self.house == self.charlie:
                return FINISHED
        elif self.house == self.charlie:
            return INVALID
        return OKAY

    def __len__(self) -> int:
        if self.parent is None:
            return 1
        return 1 + len(self.parent)

    @property
    def params(self) -> tuple[tuple[int, int],
                              tuple[int, int],
                              tuple[tuple[int, int], ...]]:
        return (
            self.charlie.params,
            self.house.params,
            tuple(f.params for f in self.foods)
        )


def parse(strArr: str) -> tuple[Location, Location, list[Location]]:
    charlie = house = None
    foods = []
    assert isinstance(strArr, list)
    for i, row in enumerate(strArr):
        assert isinstance(row, str)
        for j, char in enumerate(row):
            if char == 'C':
                charlie = Location(row=i, col=j)
            elif char == 'H':
                house = Location(row=i, col=j)
            elif char == 'F':
                foods.append(Location(row=i, col=j))
    assert charlie is not None
    assert house is not None
    assert 1 <= len(foods) <= 8
    return charlie, house, foods


def taxicab(a: Location, b: Location) -> int:
    return abs(a.row - b.row) + abs(a.col - b.col)


def go_around_house(food1: Location,
                    food2: Location,
                    house: Location) -> bool:
    return ((food1.row == food2.row == house.row and
             (min(food1.col, food2.col) <= house.col
              <= max(food1.col, food2.col))) or
            (food1.col == food2.col == house.col and
             (min(food1.row, food2.row) <= house.row
              <= max(food1.row, food2.row))))


def check(candidate):
    examples = [
        (["F00F", "00H0", "0000", "C000"], 8),
        (["0F00", "00F0", "H000", "C000"], 9)
    ]
    for inp, exp in examples:
        assert candidate(inp) == exp, (inp, exp, candidate(inp))

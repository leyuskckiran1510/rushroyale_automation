from collections import Counter
from dataclasses import dataclass, field

from typing import NamedTuple, Tuple, List

from os import environ

from event import Dragers,Event
from utils import find_average
from postitions import deck

if not environ.get("DEBUG"):
    __breakpoint = breakpoint
    breakpoint = lambda *args: ...


class Matlike:
    ...



class Color(NamedTuple):
    r: int | float
    b: int | float
    g: int | float
    a: int | float | None = None


Color_Type = (
    Color
    | Tuple[int | float, int | float, int | float]
    | Tuple[int | float, int | float, int | float, None | float | int]
)

UA_WIDTH = 5
UA_HEIGHT = 3
DECK_WIDTH = 5


@dataclass
class Frame_Diff:
    hero: bool = False
    spwanner: bool = False
    decks: List[bool] = field(default_factory=lambda: [False] * DECK_WIDTH)
    unit_area: List[bool] = field(default_factory=lambda: [False] * UA_WIDTH * UA_HEIGHT)


class Frame_Object(NamedTuple):
    match_threshold: int
    hero: Color_Type
    spwanner: Color_Type
    decks: Tuple[Color_Type, Color_Type, Color_Type, Color_Type, Color_Type]
    unit_area: Tuple[
        Tuple[Color_Type, Color_Type, Color_Type, Color_Type, Color_Type],
        Tuple[Color_Type, Color_Type, Color_Type, Color_Type, Color_Type],
        Tuple[Color_Type, Color_Type, Color_Type, Color_Type, Color_Type],
    ]

    def __eq__(self, other) -> Frame_Diff | None:
        _diff: Frame_Diff = Frame_Diff()
        if not isinstance(other, Frame_Object):
            return None
        if not self._close_range(self.match_threshold,self.spwanner, other.spwanner):
            _diff.spwanner = True
        if not self._close_range(self.match_threshold,self.hero, other.hero):
            _diff.hero = True
        if len(self.decks) != len(other.decks):
            return None
        for n, deck in enumerate(zip(self.decks, other.decks)):
            if not self._close_range(self.match_threshold,deck[0], deck[1]):
                _diff.decks[n] = True
        if len(self.unit_area) != len(other.unit_area):
            return None
        for i in range(len(self.unit_area)):
            if len(self.unit_area[i]) != len(other.unit_area[i]):
                return None
            for j in range(len(self.unit_area[i])):
                if not self._close_range(self.match_threshold,self.unit_area[i][j], other.unit_area[i][j]):
                    _diff.unit_area[j * UA_WIDTH + i] = True
        return _diff

    @staticmethod
    def _close_range(match_threshold, color1, color2):
        return all(abs(c1 - c2) <= match_threshold for c1, c2 in zip(color1, color2))


class Game:
    me: "Game|None" = None

    def __new__(cls) -> "Game":
        if not Game.me:
            Game.me = super().__new__(cls)
        return Game.me

    def __init__(self, event: Event) -> None:
        self.id = -1
        self.event = event
        self.first_frame_averages: Frame_Object | None = None
        print(self)

    # Utilities

    def find_average(self, img: Matlike) -> Frame_Object:
        """
        Finds average color of each rec of
            hero,spwanner,unit_area,decks
        """
        ...

    def is_game_screen(self, img: Matlike) -> bool:
        """
        Check if the screen is a valid game screen or not
        """
        if not self.first_frame_averages:
            self.first_frame_averages = self.find_average(img)

        assert "Not Implemented" == 1

        return False

    # Actions

    def click_hero(self) -> None:
        ...

    def click_spwanner(self) -> None:
        ...

    def power_up_decisions(self,new_frame:Frame_Object) -> None:
        ...

    def merger(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        right = start if start[0] > end[0] else end
        left  = start if start != right else end
        self.event.drag(right,left,Dragers.bezier())

    def levelup(self,new_frame:Frame_Object):
        to_level_up = {}
        for unit_row in new_frame.unit_area:
            for unit_avg in unit_row:
                to_level_up[unit_avg] = to_level_up.get(unit_avg,0)+1
        c = Counter(to_level_up)
        most = c.most_common(1)
        for n,_deck in enumerate(new_frame.decks):
            if  Frame_Object._close_range(50,_deck,most):
                x,y=deck[n]
                self.event.click(x,y)


    def __next__(self, img: Matlike):
        if not self.is_game_screen(img):
            raise StopIteration()
        new_frame: Frame_Object = self.find_average(img)
        diff: Frame_Diff | None = new_frame == self.first_frame_averages
        if not diff:
            return
        # if the current patch is not different from inital patch
        # then they are same as ground in first frame, ie are grounds
        ground_count = len(list(filter(lambda x: not x, diff.unit_area)))
        if diff.hero:
            self.click_hero()
        if ground_count > 0:
            self.click_spwanner()
        if not ground_count:
            self.power_up_decisions(new_frame)

    def __enter__(self):
        ...

    def __exit__(self):
        ...

    def __str__(self) -> str:
        return f"[Game] {self.id}"

    def __repr__(self) -> str:
        return f"[Game]"


def main():
    c = Frame_Object(
        10,
        (10, 10, 10),
        (10, 10, 10),
        ((10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10)),
        (
            ((10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10)),
            ((10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10)),
            ((10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10)),
        ),
    )
    d = Frame_Object(
        10,
        Color(10, 10, 10),
        Color(10, 10, 10),
        (Color(10, 10, 10), Color(10, 10, 10), Color(10, 10, 10), Color(10, 10, 10), Color(10, 10, 10)),
        (
            ((10, 10, 10), (10, 10, 10), (10, 100, 10), (10, 10, 10), (10, 10, 10)),
            ((10, 10, 10), (10, 101, 10), (10, 101, 10), (10, 10, 10), (10, 10, 10)),
            ((10, 10, 310), (10, 10, 10), (10, 10, 10), (10, 10, 10), (10, 10, 10)),
        ),
    )
    diff = c == d
    if diff:
        ground_count = list(filter(lambda x: not x, diff.unit_area))
        print(ground_count, len(ground_count))
    print(c == d, c.decks[0])
    pass


if __name__ == "__main__":
    main()

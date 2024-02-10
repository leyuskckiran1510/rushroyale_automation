import time

from event import Dragers, Event
from postitions import spwanner


position_to_follow = [
    [186, 518],  # first posiotn
    [100, 100],  # any random posiotn to continue
    [100, 100],  # spwanner_click again
    [100, 100],  # spwanner_click again
    [100, 100],  # spwanner_click again
    [100, 100],  # spwanner_click again
    ...,  # to add more
]


class Tutorial:
    def __init__(self, event: Event):
        self.event = event

    def center(self, two_cooridantes) -> tuple[int, int]:
        a, b = two_cooridantes
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def follow(self):
        x, y = self.center(spwanner)
        for i in range(1, 10):
            time.sleep(0.1)
            self.event.drag(spwanner[0], (x, y), Dragers.linear())
            # self.event.click_rel(x + i, y + i)
            print(x + i, y + i)

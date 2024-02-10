import os
import sys
import time
from typing import NamedTuple
import cv2
import numpy as np
from pickle import load, dump
from collections import namedtuple

from postitions import deck, unit_area, hero, spwanner, resize_poses, og_size, og_window
from tutorial import Tutorial
from event import Dragers, Event, Screencapture
from utils import PreComputedImg, analyze_deck, draw_rec


from typing import Callable
from cv2.typing import MatLike


TEMPLATE_PATH = "all_units"
THREADSHOLD = 0.1


def log(string, /, level=0):
    print(f"[{level}]:{string}")


def template_paint(_object, templates):
    img_gray = cv2.cvtColor(_object, cv2.COLOR_BGR2GRAY)
    _object = _object.copy()

    for name, template in templates.items():
        if not "t" in name:
            continue
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED)
        loc = np.where(res < THREADSHOLD)
        value = 0
        for pt in zip(*loc[::-1]):
            cv2.rectangle(_object, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            if value > 4:
                break
            value += 1
        if value > 0:
            print(name, "was found", value, "times", "With Threadshold", THREADSHOLD)
            cv2.imshow("FOUND THIS", template)
            cv2.waitKey(0)

    return _object


def load_all_template(force_reload=False) -> list[PreComputedImg]:
    pre_computed_list = []
    pickle_name = "pickled_templates.pickle"
    if not force_reload and os.path.exists(pickle_name):
        with open(pickle_name, "rb") as fp:
            array = load(fp)
        return array

    for template in os.listdir(TEMPLATE_PATH):
        _path = os.path.join(TEMPLATE_PATH, template)
        if os.path.isdir(_path):
            continue
        log(f"Loaded {_path}")
        # template_img = cv2.cvtColor(cv2.imread(_path), cv2.COLOR_BGR2GRAY)
        # pre_computed_list[template] = template_img
        pre_computed_list.append(PreComputedImg(_path))
        print(pre_computed_list[-1])

    with open(pickle_name, "wb") as fp:
        dump(pre_computed_list, fp)

    return pre_computed_list


class Callback(NamedTuple):
    mouse_callback: Callable
    keyboard_callback: Callable
    setter: Callable
    getter: Callable


def opencv_event_callbacks(ev: Event) -> Callback:
    start, end = None, None

    def mouse_callback(event, mouseX, mouseY, flags, param):
        nonlocal start, end
        if event == cv2.EVENT_LBUTTONUP:
            print(mouseX, mouseY)
            # for tutorial automation,
            ev.click(mouseX, mouseY)

        if event == cv2.EVENT_RBUTTONUP:
            print(mouseX, mouseY)
            if not start:
                start = (mouseX, mouseY)
            elif not end:
                end = (mouseX, mouseY)
                ev.drag(start, end, Dragers.bezier())
                start = None
                end = None

    def keyboard_callback(event, *args, **kwargs):
        print(event, args, kwargs)

    def setter(*args):
        ...

    def getter():
        ...

    return Callback(
        mouse_callback=mouse_callback,
        keyboard_callback=keyboard_callback,
        setter=setter,
        getter=getter,
    )


templates = None


def main():
    event, sc = Screencapture("Rush Royale", size=og_window)
    # event, sc = Screencapture("a - Paint")

    # t = Tutorial(event)
    # t.follow()
    # exit()

    global THREADSHOLD, templates, deck, hero, spwanner, unit_area
    force = False
    SIZE = (350, 650)
    image_name = "./test/screen.png"
    if len(sys.argv) > 1:
        if sys.argv[1] in ("true", "True"):
            force = True
        else:
            if sys.argv[1].endswith(".jpg"):
                image_name = sys.argv[1]

    templates = load_all_template(force)

    # img = cv2.imread(image_name)
    # img = cv2.resize(img, SIZE)

    img2 = next(sc).copy()
    callback = opencv_event_callbacks(event)

    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("image", 300, 0)
    cv2.setMouseCallback("image", callback.mouse_callback)
    count = 0
    # deck = resize_poses((img2.shape[1], img2.shape[0]), deck)
    # unit_area = resize_poses((img2.shape[1], img2.shape[0]), unit_area)
    # hero = resize_poses((img2.shape[1], img2.shape[0]), hero)
    # spwanner = resize_poses((img2.shape[1], img2.shape[0]), spwanner)
    # analyed = False
    while True:
        img2 = next(sc).copy()
        img2.setflags(write=True)
        # exit(0)
        # img2 = template_paint(img, templates)
        # t.follow()
        # if not analyed:
        #     img2, filtred_template = analyze_deck(img, templates)
        #     analyed = True
        # img2 = draw_rec(img2, None)
        # callback.setter(img2)
        # img2 = callback.getter()
        cv2.imshow("image", img2)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("a"):
            THREADSHOLD += 0.1
        if key == ord("d"):
            THREADSHOLD -= 0.1
        if key == ord("w"):
            THREADSHOLD += 0.01
        if key == ord("s"):
            THREADSHOLD -= 0.01
        count += 1


if __name__ == "__main__":
    main()

import cv2
import os
from cv2.typing import MatLike
import win32gui
import pywintypes
import numpy as np
from pickle import load,dump
from bshot.screenshot import get_image
from tutorial import Tutorial
import sys


TEMPLATE_PATH = "all_units"
THREADSHOLD = 0.1

def log(string,/,level=0):
    print(f"[{level}]:{string}")

class Screencapture:

    def __init__(self,window_name,/):
        self.win_name = window_name
        self.win_id = win32gui.FindWindow(None, self.win_name)
        if self.win_id<1:
            raise ValueError(f"Couldn't Find any window with name {self.win_name}")

    def __next__(self):
        try:
            return get_image(self.win_id, method="windll")
        except pywintypes.error as _:
            raise Exception(f"{self.win_name} is closed or crahsed Couldn't detect")


def template_paint(_object, templates):
    img_gray = cv2.cvtColor(_object, cv2.COLOR_BGR2GRAY)
    _object = _object.copy()

    for name,template in templates.items():
        if not "t" in  name:
            continue
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED)
        loc = np.where(res < THREADSHOLD)
        value = 0
        for pt in zip(*loc[::-1]):
            cv2.rectangle(_object, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            if value>4:
                break
            value +=1
        if value>0:
            print(name,"was found",value,"times","With Threadshold",THREADSHOLD)
            cv2.imshow("FOUND THIS",template)
            cv2.waitKey(0)

    return _object

def load_all_template(force_reload=False) -> dict[str,MatLike]:
    array_dic = {}
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
        template_img = cv2.cvtColor(cv2.imread(_path), cv2.COLOR_BGR2GRAY)
        array_dic[template]=template_img

    with open(pickle_name, "wb") as fp:
        dump(array_dic, fp)

    return array_dic

def main():
    # sc = Screencapture("all_units")
    global THREADSHOLD
    force = True
    if not len(sys.argv)>1:
        force = False
    templates = load_all_template(force)
    img = cv2.imread("./test/screen.png")
    while True:
        # img = next(sc)
        img2 = template_paint(img, templates)
        cv2.imshow("Captured and Tracked", img2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1)&0xff == ord('a'):
            THREADSHOLD+=0.1
        if cv2.waitKey(1)&0xff == ord('d'):
            THREADSHOLD-=0.1
        if cv2.waitKey(1)&0xff == ord('w'):
            THREADSHOLD+=0.01
        if cv2.waitKey(1)&0xff == ord('s'):
            THREADSHOLD-=0.01

        print("next loop",THREADSHOLD)

if __name__ == "__main__":
    main()
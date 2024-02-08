from typing import NoReturn
import cv2
import os
from cv2.typing import MatLike
import win32gui
import pywintypes
import numpy as np
from pickle import load, dump
from bshot.screenshot import get_image
from balancer import color_transfer
from tutorial import Tutorial
import sys
from postitions import *


TEMPLATE_PATH = "all_units"
THREADSHOLD = 0.1


def log(string, /, level=0):
    print(f"[{level}]:{string}")


class Screencapture:
    def __init__(self, window_name, /):
        self.win_name = window_name
        self.win_id = win32gui.FindWindow(None, self.win_name)
        if self.win_id < 1:
            raise ValueError(f"Couldn't Find any window with name {self.win_name}")

    def __next__(self):
        try:
            return get_image(self.win_id, method="srccopy")
        except pywintypes.error as _:
            raise Exception(f"{self.win_name} is closed or minimized Couldn't detect")
        except Exception as e:
            raise Exception(f"Problem while trying to capture screen with:-{e} ")


class PreComputedImg:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.name = self.filename.split(".")[0].split("/")[-1].split("\\")[-1].strip()
        self.image = cv2.imread(self.filename)
        self.width = self.image.shape[0]
        self.height = self.image.shape[1]
        self.av_color = find_average(self.image, [0, 0, self.width, self.height])

    def __repr__(self) -> str:
        return f"PreComputedImg[{self.name},{self.width}x{self.height},{self.av_color}]"


def filter_deck(img: MatLike) -> None:
    for i in deck:
        print(i)


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


def find_closest(img1: MatLike, imgs: list[PreComputedImg]):
    average_color = find_average(img1, [0, 0, img1.shape[0], img1.shape[1]])
    min_dis = float("INF")
    index: PreComputedImg | None = None
    for img in imgs:
        color = img.av_color
        distances = np.linalg.norm(average_color - np.array(color))
        # res = cv2.matchTemplate(img1, img.image, cv2.TM_SQDIFF_NORMED)
        # loc = np.where(res < THREADSHOLD)
        # print(loc)
        if distances < min_dis:
            min_dis = distances
            index = img
        if img.name == "empty" and min_dis != float("inf"):
            print(min_dis)

    return index


def find_top_five(image):
    img = image
    data = np.reshape(img, (-1, 3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)

    # print("Dominant color is: bgr({})".format(centers[0].astype(np.int32)))
    return tuple(float(i) for i in centers[0])


def find_average(img, rectangle) -> tuple:
    sub_rectangle = img[
        rectangle[1] : rectangle[1] + rectangle[3],
        rectangle[0] : rectangle[0] + rectangle[2],
        :,
    ]
    # average_color = np.average(sub_rectangle, axis=(0, 1)).astype(int)
    average_color = np.median(sub_rectangle, axis=(0, 1)).astype(float)
    average_color = tuple(float(i) for i in average_color)

    # distances = [np.linalg.norm(average_color - np.array(color)) for color in empty]
    # min_distance = min(distances)
    # # print(distances, min_distance)
    # if min_distance < 20:
    #     average_color = (0.0, 0.0, 255.0)
    return average_color


def draw_rec(img, templates=None):
    _img = np.copy(img)
    """
        DeckCard Area Each Unit
    """
    for i in deck:
        cv2.rectangle(_img, i[0], i[1], (0, 0, 255), 2)
        x, y, stepx, stepy = i[0][0], i[0][1], i[1][0] - i[0][0], i[1][1] - i[0][1]
        average_color = find_average(_img, [x, y, stepx, stepy])
        cv2.fillPoly(
            _img,
            [
                np.array(
                    [[x, y], [x + stepx, y], [x + stepx, y + stepy], [x, y + stepy]]
                )
            ],
            average_color,
        )
        if templates:
            at_here = img[y : y + stepy, x : x + stepx, :]
            new_img = find_closest(at_here, templates)
            if new_img:
                try:
                    new_img = cv2.resize(new_img.image, (stepx, stepy))
                    _img[y : y + stepy, x : x + stepx, :] = new_img
                except Exception as e:
                    print(e)
                    pass
    """
        Unit Ground Area
    """
    stepx = (unit_area[1][0] - unit_area[0][0]) // 5
    stepy = (unit_area[1][1] - unit_area[0][1]) // 3
    averages = []
    for x in range(unit_area[0][0], unit_area[1][0] - stepx, stepx):
        for y in range(unit_area[0][1], unit_area[1][1] - stepy, stepy):
            average_color = find_average(_img, [x, y, stepx, stepy])
            averages.append(average_color)
            cv2.rectangle(_img, (x, y), (x + stepx, y + stepy), (255, 0, 0), 2)
            cv2.fillPoly(
                _img,
                [
                    np.array(
                        [[x, y], [x + stepx, y], [x + stepx, y + stepy], [x, y + stepy]]
                    )
                ],
                average_color,
            )
            if templates:
                at_here = img[y : y + stepy, x : x + stepx, :]
                new_img = find_closest(at_here, templates)
                if new_img:
                    try:
                        new_img = cv2.resize(new_img.image, (stepx, stepy))
                        _img[y : y + stepy, x : x + stepx, :] = new_img
                    except Exception as e:
                        pass
    """
        Hero Area
    """
    x, y, stepx, stepy = (
        hero[0][0],
        hero[0][1],
        hero[1][0] - hero[0][0],
        hero[1][1] - hero[0][1],
    )
    average_color = find_average(_img, [x, y, stepx, stepy])
    averages.append(average_color)
    cv2.rectangle(_img, (x, y), (x + stepx, y + stepy), (255, 0, 0), 2)
    cv2.fillPoly(
        _img,
        [np.array([[x, y], [x + stepx, y], [x + stepx, y + stepy], [x, y + stepy]])],
        average_color,
    )

    """
        Spawnner
    """
    x, y, stepx, stepy = (
        spwanner[0][0],
        spwanner[0][1],
        spwanner[1][0] - spwanner[0][0],
        spwanner[1][1] - spwanner[0][1],
    )
    average_color = find_average(_img, [x, y, stepx, stepy])
    averages.append(average_color)
    cv2.rectangle(_img, (x, y), (x + stepx, y + stepy), (255, 0, 0), 2)
    cv2.fillPoly(
        _img,
        [np.array([[x, y], [x + stepx, y], [x + stepx, y + stepy], [x, y + stepy]])],
        average_color,
    )

    return _img


def _match_template(img, templates):
    for template in templates:
        # _tmpl = np.resize(template.image, img.shape)
        _tmpl = cv2.cvtColor(template.image, cv2.COLOR_BGR2GRAY)
        print(_tmpl.shape, "<=>", img.shape)
        # _tmpl = cv2.cvtColor(_tmpl, cv2.COLOR_BGR2GRAY)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # res = cv2.matchTemplate(img, _tmpl, cv2.TM_SQDIFF_NORMED)
        hist1 = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([_tmpl], [0], None, [256], [0, 256])

        res = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        if res > -100:
            cv2.imshow(".", img)
            cv2.imshow("..", _tmpl)
            print(res, template.name)
            cv2.waitKey(0)

        continue
        loc = np.where(res < 0.5)
        value = 0
        for pt in zip(*loc[::-1]):
            # cv2.rectangle(_object, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            if value > 4:
                break
            value += 1
        if value > 0:
            print(
                template.name,
                "was found",
                value,
                "times",
                "With Threadshold",
                THREADSHOLD,
            )
            cv2.imshow("FOUND THIS", template.image)
            cv2.waitKey(1)
        # print(img.shape, template.image.shape, _tmpl.shape, value)
    exit(0)
    return templates[0]


def normalize(arr):
    rng = arr.max() - arr.min()
    amin = arr.min()
    return (arr - amin) * 255 / rng


def match_template(img_, templates):
    img = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
    for template in templates:
        _tmpl = cv2.resize(
            template.image, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC
        )
        _tmpl = color_transfer(img_, _tmpl, clip=False)
        _tmpl = cv2.cvtColor(_tmpl, cv2.COLOR_BGR2GRAY)
        edges1 = cv2.Canny(image=img, threshold1=1, threshold2=100)
        edges2 = cv2.Canny(image=_tmpl, threshold1=1, threshold2=100)
        ed1 = normalize(img)
        ed2 = normalize(_tmpl)
        print(img.shape, _tmpl.shape)
        # diff = ed1 - ed2
        diff = edges1 - edges2
        m_norm = sum(sum(abs(diff)))
        print(m_norm)
        THREADSHOLD = 200000
        if m_norm < THREADSHOLD:
            print("Found Image")
            cv2.imshow("-", edges1)
            cv2.imshow("--", edges2)
            cv2.moveWindow("-", 200, 200)
            cv2.moveWindow("-", 250, 250)
            cv2.waitKey(0)
        cv2.imshow(".", img)
        cv2.imshow("..", _tmpl)
        cv2.waitKey(0)

    exit(0)


def analyze_deck(img, template) -> tuple:
    _img = img.copy()
    _template = []
    for i in deck:
        cv2.rectangle(_img, i[0], i[1], (0, 0, 255), 2)
        x, y, stepx, stepy = i[0][0], i[0][1], i[1][0] - i[0][0], i[1][1] - i[0][1]
        average_color = find_average(_img, [x, y, stepx, stepy])
        # cv2.fillPoly(
        #     _img,
        #     [
        #         np.array(
        #             [[x, y], [x + stepx, y], [x + stepx, y + stepy], [x, y + stepy]]
        #         )
        #     ],
        #     average_color,
        # )
        if templates:
            at_here = img[y : y + stepy, x : x + stepx, :]
            new_img = match_template(at_here, templates)
            _template.append(new_img)
            if new_img:
                try:
                    new_img = cv2.resize(new_img.image, (stepx, stepy))
                    # _img[y : y + stepy, x : x + stepx, :] = new_img
                except Exception as e:
                    print(e)
                    pass
    return _img, _template


templates = None


def main():
    # sc = Screencapture("all_units")
    sc = Screencapture("Rush Royale")
    global THREADSHOLD, templates
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

    def draw_circle(event, x, y, flags, param):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img, (x, y), 1, (255, 0, 0), -1)
            mouseX, mouseY = x, y
            print(mouseX, mouseY)

    # t = Tutorial()
    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("image", 00, 0)
    cv2.setMouseCallback("image", draw_circle)
    count = 0
    analyed = False
    while True:
        img = next(sc).copy()
        print(img.shape)
        img.setflags(write=True)
        # img2 = template_paint(img, templates)
        # t.follow()
        if not analyed:
            img2, filtred_template = analyze_deck(img, templates)
            analyed = True
        # img2 = draw_rec(img, filtred_template)
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
        # cv2.imwrite(f"./test/actual_src{count}.png", img)
        count += 1


if __name__ == "__main__":
    main()

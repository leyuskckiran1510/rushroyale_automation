import cv2
import numpy as np
from cv2.typing import MatLike


from balancer import color_transfer

from postitions import (
    deck,
    hero,
    spwanner,
    resize_poses,
    unit_area,
)


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
    # data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(
        data, 1, None, criteria, 10, flags
    )  # type:ignore

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


def draw_rec(img, templates=None, _deck=[], _hero=[], _spwanner=[], _unit_area=[]):
    if not _deck:
        _deck = deck
        _hero = hero
        _spwanner = spwanner
        _unit_area = unit_area
    _img = np.copy(img)
    """
        DeckCard Area Each Unit
    """
    for i in _deck:
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
    stepx = (_unit_area[1][0] - _unit_area[0][0]) // 5
    stepy = (_unit_area[1][1] - _unit_area[0][1]) // 3
    averages = []
    for x in range(_unit_area[0][0], _unit_area[1][0] - stepx, stepx):
        for y in range(_unit_area[0][1], _unit_area[1][1] - stepy, stepy):
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
        _hero[0][0],
        _hero[0][1],
        _hero[1][0] - _hero[0][0],
        _hero[1][1] - _hero[0][1],
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
        _spwanner[0][0],
        _spwanner[0][1],
        _spwanner[1][0] - _spwanner[0][0],
        _spwanner[1][1] - _spwanner[0][1],
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


def analyze_deck(img, templates) -> tuple:
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

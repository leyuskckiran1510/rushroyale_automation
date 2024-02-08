import cv2
import numpy as np
from postitions import deck, resize_poses, hero


def normalize(arr):
    rng = arr.max() - arr.min()
    amin = arr.min()
    return (arr - amin) * 255 / rng


def detect_edges(img1, img2):
    # Canny Edge Detection
    edges1 = cv2.Canny(image=img1, threshold1=1, threshold2=100)
    edges2 = cv2.Canny(image=img2, threshold1=1, threshold2=100)
    ed1 = normalize(img1)
    ed2 = normalize(img2)
    diff = ed1 - ed2
    m_norm = sum(sum(abs(diff)))
    print(m_norm)
    THREADSHOLD = 200
    if m_norm < THREADSHOLD:
        print("Found Image")
        cv2.imshow("-", edges1)
        cv2.imshow("--", edges2)
        cv2.moveWindow("-", 200, 200)
        cv2.moveWindow("-", 250, 250)
        cv2.waitKey(0)


def detect_orb(img1, img2):
    # Initialize ORB detector

    options = {
        "nfeatures": 1,
        "scaleFactor": 1,
        "nlevels": 80,
        "edgeThreshold": 2,
        "firstLevel": 3,
        "WTA_K": 2,
        "scoreType": cv2.ORB_HARRIS_SCORE,
        "patchSize": 2,
        "fastThreshold": 1,
    }
    orb = cv2.ORB().create(**options)

    kp1, des1 = orb.detectAndCompute(img1, None)  # type:ignore
    kp2, des2 = orb.detectAndCompute(img2, None)  # type:ignore

    # Initialize matcher
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = matcher.match(des1, des2)
    # draw only keypoints location,not size and orientation
    img3 = cv2.drawKeypoints(img1, kp1, None, color=(0, 255, 0), flags=0)  # type:ignore
    img4 = cv2.drawKeypoints(img2, kp2, None, color=(0, 255, 0), flags=0)  # type:ignore

    # Display Canny Edge Detection Image
    cv2.imshow(".", img3)
    cv2.imshow("..", img4)
    cv2.moveWindow(".", 50, 50)
    cv2.moveWindow("..", 150, 150)
    cv2.waitKey(0)

    matches = sorted(matches, key=lambda x: x.distance)
    MIN_MATCH_COUNT = 10
    if len(matches) >= MIN_MATCH_COUNT:
        return True
    else:
        return False


# Load images
img1 = cv2.imread(
    "./test/Screenshot_2024-02-06-11-22-49-509_com.my.defense.jpg", cv2.IMREAD_GRAYSCALE
)
img2 = cv2.imread(
    "./test/Screenshot_2024-02-06-11-24-21-819_com.my.defense.jpg", cv2.IMREAD_GRAYSCALE
)

SIZE = (350, 650)
SIZE2 = (338, 601)
img1 = cv2.resize(img1, SIZE)
img2 = cv2.resize(img2, SIZE)
# img2 = cv2.flip(img2, 0)
deck = resize_poses(SIZE, deck)
for i in deck:
    x, y, stepx, stepy = i[0][0], i[0][1], i[1][0] - i[0][0], i[1][1] - i[0][1]
    _img2 = img2[y : y + stepy, x : x + stepx]
    _img1 = img1[y : y + stepy, x : x + stepx]

    # Check if images match
    # if detect_orb(_img1, _img2):
    if detect_edges(_img1, _img2):
        print("Images match!")
    else:
        print("Images do not match.")
cv2.imshow("_", img1)
cv2.imshow("__", img2)
cv2.waitKey(0)

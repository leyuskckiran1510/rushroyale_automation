import cv2


haystack_img = cv2.imread("test/screen.png", 0)
needle_img = cv2.imread("all_units/tutorial.png", 0)


result = cv2.matchTemplate(haystack_img, needle_img, cv2.TM_CCOEFF_NORMED)


min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
threshold = 0.66

while True:
    if max_val >= threshold:
        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]

        top_left = max_loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        copy_ = haystack_img.copy()
        cv2.rectangle(
            copy_,
            top_left,
            bottom_right,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4,
        )
        cv2.imshow("Match", copy_)

    cv2.imshow("1", haystack_img)
    cv2.imshow("2", needle_img)
    key = cv2.waitKey(1) & 0xFF
    match key:
        case x if x == ord("q"):
            exit(0)
        case x if x == ord("w"):
            threshold += 0.1
            print("Needle not found.", threshold)
        case x if x == ord("s"):
            threshold -= 0.1
            print("Needle not found.", threshold)
        case x if x == ord("a"):
            threshold += 0.01
            print("Needle not found.", threshold)
        case x if x == ord("d"):
            threshold -= 0.01
            print("Needle not found.", threshold)

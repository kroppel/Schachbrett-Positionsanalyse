import numpy as np
from cv2 import VideoCapture, imread, waitKey, imshow, EVENT_LBUTTONDOWN, setMouseCallback, getPerspectiveTransform, warpPerspective
from image_processing import preprocessing, draw_lines, extract_lines, filter_lines, get_intersections, draw_points, resize_image
import sys

def get_points(event, x, y, flags, points):
    if event == EVENT_LBUTTONDOWN and len(points) < 4:
        print((x,y))
        points.append([x, y])

pts1 = []

input = 0 if len(sys.argv) == 1 else sys.argv[1]
cap = VideoCapture(input)    # Use video/webcam as input 
ret_val, img = cap.read()

# Show camera input, for rearranging the setup etc.
while ret_val:
    ret_val, img = cap.read()
    img = resize_image(img, 1.5)
    imshow("Input", img)
    if not waitKey(1) < 0:
        break

# Collect points for Warping
while len(pts1) < 4 and ret_val:
    ret_val, img = cap.read()
    img = resize_image(img, 1.5)
    imshow("Input", img)
    setMouseCallback("Input", get_points, pts1)
    if not waitKey(1) < 0:
        break

pts1 = np.float32(pts1)
pts2 = np.float32([[0,0], [800,0], [0,800], [800,800]])

while ret_val:
    ret_val, img = cap.read()
    img = resize_image(img, 1.5)

    M = getPerspectiveTransform(pts1,pts2)
    img = warpPerspective(img,M,(800,800))

    img_threshold = preprocessing(img)
    h_lines, v_lines = filter_lines(extract_lines(img_threshold))
    intersections = get_intersections(h_lines, v_lines)
    if not intersections is None:
        intersections = [tuple(map(int, point)) for point in list(intersections.flatten())]

    img_display = draw_points(draw_lines(img, h_lines+v_lines), intersections)
    imshow("Input", img_display)
    if not waitKey(1) < 0:
        break

import numpy as np
from cv2 import VideoCapture, imread, resize, INTER_LINEAR, waitKey, imshow
from image_processing import preprocessing, draw_lines, extract_lines, filter_lines, get_intersections, draw_points

"""
input = 0 if len(argv) == 1 else argv[1]
cap = VideoCapture(input)    # Use video/webcam as input 
ret_val, image = cap.read()

while ret_val:
    # TODO

    ret_val, image = cap.read()
"""

img = imread("../data/img_1.jpg")                           # Use image as input source
img_threshold = preprocessing(img)

h_lines, v_lines = filter_lines(extract_lines(img_threshold))
intersections = list(get_intersections(h_lines, v_lines).flatten())
intersections = [tuple(map(int, point)) for point in intersections]
print(intersections)

img_display = resize(draw_points(draw_lines(img, h_lines+v_lines), intersections), (int(img.shape[1]/4), int(img.shape[0]/4)), interpolation = INTER_LINEAR)
while True:
    imshow("Input", img_display)
    key = waitKey(1)
    if (key == 27):
        break

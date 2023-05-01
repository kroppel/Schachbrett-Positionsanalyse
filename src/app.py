import cv2
import numpy as np

"""
input = 0 if len(argv) == 1 else argv[1]
cap = VideoCapture(input)    # Use video/webcam as input 
ret_val = True

while ret_val:
    ret_val, image = cap.read()
"""

img = cv2.imread("../data/img_1.jpg")                           # Use image as input source

lines = extract_lines(img_threshold)
print(lines)

img_display = cv2.resize(draw_lines(img, lines), (int(img.shape[1]/4), int(img.shape[0]/4)), interpolation = cv2.INTER_LINEAR)
while True:
    cv2.imshow("Input", img_display)
    key = cv2.waitKey(1)
    if (key == 27):
        break

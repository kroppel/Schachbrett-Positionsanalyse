import numpy as np
import cv2
from Backend.image_processing import preprocessing, draw_lines, extract_lines, filter_lines, get_intersections, draw_points, resize_image
import sys
from time import sleep
import threading as th


class VidIn:

    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.pts1 = []
        self.startvid()

    def startvid(self):
        input = 0 if len(sys.argv) == 1 else sys.argv[1]

        if self.vid.isOpened():
            while len(self.pts1) < 4:
                ret, img = self.vid.read()
                img = resize_image(img, 1.5)
                cv2.imshow("Input", img)
                cv2.setMouseCallback("Input", self.get_points, self.pts1)
                if not cv2.waitKey(1) < 0:
                    break
            print("yeah")
            self.pts1 = np.float32(self.pts1)
            self.pts2 = np.float32([[0, 0], [800, 0], [0, 800], [800, 800]])
            self.M = cv2.getPerspectiveTransform(self.pts1, self.pts2)

            cv2.destroyAllWindows()

    def get_frame(self):
        if self.vid.isOpened():
            ret, img = self.vid.read()
            img = resize_image(img, 1.5)

            img = cv2.warpPerspective(img, self.M, (800, 800))
            img_threshold = preprocessing(img)

            h_lines, v_lines = filter_lines(extract_lines(img_threshold))
            intersections = get_intersections(h_lines, v_lines)
            if not intersections is None:
                intersections = [tuple(map(int, point)) for point in list(intersections.flatten())]

            img_display = draw_points(draw_lines(img, h_lines + v_lines), intersections)

            if ret:
                return ret, cv2.cvtColor(img_display, cv2.COLOR_BGR2RGB)
            else:
                return ret, None

    def get_points(self, event, x, y, flags, points):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
            print((x,y))
            points.append([x, y])



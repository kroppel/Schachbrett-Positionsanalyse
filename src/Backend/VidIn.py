import numpy as np
import cv2
from Backend.image_processing import preprocessing, draw_lines, extract_lines, filter_lines, get_intersections, draw_points, resize_image, get_figures_in_fields, compare_states, get_move_coordinates
import sys
from time import sleep
import threading as th
#import Frontend.GUI

FRAME_COUNTER_THRESHOLD = 4

class VidIn:

    def __init__(self, gui, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.gui = gui
        self.pts1 = []
        self.startvid()
        self.last_figure_state = np.vstack((np.ones((2,8)), np.zeros((4,8)), np.ones((2,8))))
        self.new_figure_state = None
        self.compare_state_counter = FRAME_COUNTER_THRESHOLD

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
            self.pts1 = np.float32(self.pts1)
            # sortieren nach x koordinate
            self.pts1 = self.pts1[np.argsort(self.pts1[:,0]),:]
            points_left = self.pts1[0:2]
            points_right = self.pts1[2:4]
            # sortieren nach y koordinate
            points_left = points_left[np.argsort(points_left[:,1]),:]
            points_right = points_right[np.argsort(points_right[:,1]),:]
            self.pts1 = np.asarray([points_left[0], points_right[0], points_left[1], points_right[1]])
            self.pts2 = np.float32([[0, 0], [800, 0], [0, 800], [800, 800]])
            self.M = cv2.getPerspectiveTransform(self.pts1, self.pts2)

            cv2.destroyAllWindows()

    def get_frame(self):
        if self.vid.isOpened():
            ret, img = self.vid.read()
            img = resize_image(img, 1.5)

            if ret:
                img = cv2.warpPerspective(img, self.M, (800, 800))
                img_threshold = preprocessing(img)

                h_lines, v_lines = filter_lines(extract_lines(img_threshold))

                if not h_lines is None and not v_lines is None:
                    intersections = get_intersections(h_lines, v_lines)
                    if not intersections is None:
                        img_display = draw_lines(img, h_lines + v_lines)

                        fields = np.ndarray((intersections.shape[0]-1,intersections.shape[1]-1), dtype=np.ndarray)
                        for i in np.arange(fields.shape[0]):
                            for j in np.arange(fields.shape[1]):
                                fields[i,j] = img_threshold[int(intersections[i,j][1]):int(intersections[i+1,j+1][1]), int(intersections[i,j][0]):int(intersections[i+1,j+1][0])]
                        figs = get_figures_in_fields(fields)
                        ret_compare_last, diff_state_last = compare_states(self.last_figure_state, figs)

                        if ret_compare_last <= 0:
                            self.compare_state_counter = FRAME_COUNTER_THRESHOLD
                        else:
                            if self.new_figure_state is None:
                                self.new_figure_state = figs
                            else:
                                ret_compare_new, diff_state_new =  compare_states(self.new_figure_state, figs)
                                if ret_compare_new != 0:
                                    self.new_figure_state = None
                                    self.compare_state_counter = FRAME_COUNTER_THRESHOLD
                                else:
                                    self.compare_state_counter -= 1

                        if self.compare_state_counter == 0:
                            self.compare_state_counter = FRAME_COUNTER_THRESHOLD
                            self.last_figure_state = self.new_figure_state
                            print("New State: \n"+str(self.last_figure_state))
                            p1, p2 = get_move_coordinates(ret_compare_last, diff_state_last)
                            self.gui.callback_move_detection(p1)
                            sleep(2)
                            self.gui.callback_move_detection(p2)


                        return ret, cv2.cvtColor(img_display, cv2.COLOR_BGR2RGB)

                    return ret, cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                else:
                    return ret, img
            
            else:
                return ret, cv2.cvtColor(np.zeros((800,800)), cv2.COLOR_BGR2RGB)

    def get_points(self, event, x, y, flags, points):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
            print((x,y))
            points.append([x, y])



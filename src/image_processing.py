import cv2
import numpy as np

def preprocessing(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                 # Convert the input image to a grayscale
    img_threshold = cv2.adaptiveThreshold(src=img_gray, maxValue=255, \
        adaptiveMethod = cv2.ADAPTIVE_THRESH_MEAN_C, thresholdType = cv2.THRESH_BINARY_INV, blockSize=15, C=6)

    return img_threshold


# Draws the given lines onto a copy of the given image
# and returns it
def draw_lines(img, lines):
    img_lines = np.copy(img)

    for dline in lines:
        rho,theta = dline[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 10000*(-b))
        y1 = int(y0 + 10000*(a))
        x2 = int(x0 - 10000*(-b))
        y2 = int(y0 - 10000*(a))
        cv2.line(img_lines,(x1,y1),(x2,y2),(0,0,255),2)

    return img_lines

def extract_lines(img):
    # Parameters for setting an interval, in which the number of retrieved lines has to lie
    n = int((img.shape[1] * 0.8) / 8) # n: Pixel size of the field of a figure. Chess Board should fill about 80% of image width
    max_deviation = 20

    lines = []
    votes_upper_bound = min(img.shape)
    votes_lower_bound = 0
    min_votes = int(min(img.shape)/3) # Line should have length of at least 1/3 of shortest image side

    extracted_lines = cv2.HoughLines(img, 1, np.pi/180, min_votes)

    if not extracted_lines is None:
        lines = extracted_lines

    return lines
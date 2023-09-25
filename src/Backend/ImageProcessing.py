import cv2
import numpy as np

DEBUG = False


"""Preprocess input image with adaptive threshold method to obtain binary image similar to gradient image

Params:
    img (np.ndarray): the input image

Returns:
    img_threshold (np.ndarray): the processed image
"""


def preprocessing(img):
    img_gray = cv2.cvtColor(
        img, cv2.COLOR_BGR2GRAY
    )  # Convert the input image to a grayscale
    img_threshold = cv2.adaptiveThreshold(
        src=img_gray,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=15,
        C=3,
    )

    return img_threshold


"""Preprocess input image of the chess playing field to obtain two masked images for black and white figures respectively.
   The color masks are given by the lower and upper bound variables inside the function. 

Params:
    img (np.ndarray): the input image

Returns:
    mask_black (np.ndarray): the masked image for black figures
    mask_white (np.ndarray): the masked image for white figures
"""


def preprocessingFigures(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask_black = cv2.inRange(img_hsv, lower_black, upper_black)
    mask_white = cv2.inRange(img_hsv, lower_white, upper_white)

    mask_black = cv2.dilate(
        cv2.morphologyEx(
            mask_black,
            cv2.MORPH_OPEN,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        ),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)),
    )
    mask_white = cv2.dilate(
        cv2.morphologyEx(
            mask_white,
            cv2.MORPH_OPEN,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        ),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
    )

    return mask_black, mask_white


"""Resize a given image by a factor.

Params:
    img (np.ndarray): the input image
    factor (float): the factor by which the image is resized

Returns:
     (np.ndarray): the resized image
"""


def resizeImage(img, factor):
    return cv2.resize(
        img,
        (int(img.shape[1] * factor), int(img.shape[0] * factor)),
        interpolation=cv2.INTER_LINEAR,
    )


# Draws the given lines onto a copy of the given image
# and returns it
def drawLines(img, lines):
    if lines is None:
        return img

    img_lines = np.copy(img)

    for dline in lines:
        rho, theta = dline
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 10000 * (-b))
        y1 = int(y0 + 10000 * (a))
        x2 = int(x0 - 10000 * (-b))
        y2 = int(y0 - 10000 * (a))
        cv2.line(img_lines, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return img_lines


def drawPoints(img, points):
    if points is None:
        return img

    img_points = np.copy(img)

    for point in points:
        cv2.circle(img_points, point, 10, (0, 255, 0), -1)

    return img_points


def extractLines(img):
    # Parameters for setting an interval, in which the number of retrieved lines has to lie
    n = int(
        (img.shape[1] * 0.8) / 8
    )  # n: Pixel size of the field of a figure. Chess Board should fill about 80% of image width
    max_deviation = 20

    lines = []
    votes_upper_bound = min(img.shape)
    votes_lower_bound = 0
    min_votes = int(
        min(img.shape) / 3
    )  # Line should have length of at least 1/3 of shortest image side

    extracted_lines = cv2.HoughLines(img, 1, np.pi / 180, min_votes)

    if not extracted_lines is None:
        lines = extracted_lines

    return lines


# Filters out irrelevant lines (non-horizontal/non-vertical/duplicate)
def filterLines(lines):
    # Removes lines that are neither horizontally nor vertically aligned
    def getHorizontalAndVerticalLines(lines):
        vertical_lines = []
        horizontal_lines = []

        for line in lines:
            rho, theta = line[0]
            if (theta > 1.5407) and (theta < 1.6007):
                horizontal_lines.append((rho, theta))
            elif (theta > -0.05) and (theta < 0.05):
                vertical_lines.append((rho, theta))

        return horizontal_lines, vertical_lines

    # Removes lines that are probably duplicates and returns
    # the remaining ones
    def removeDuplicateLines(lines):
        d_lines = []
        for line in lines:
            rho, theta = line
            add_line = True
            for d_line in d_lines:
                d_rho = d_line[0]
                if not ((rho < (d_rho - 50)) or (rho > (d_rho + 50))):
                    add_line = False
            if add_line:
                d_lines.append(line)
        return d_lines

    # Removes lines that are probably not part of the
    # chess playing field and returns the remaining ones
    # (Based on their distance, etc)
    def keepChessLines(lines):
        lines.sort()
        chess_lines = lines
        deviation = 10000
        rhos = []
        rho_deviation_sum = 0

        # Parameter for maximal value of the rho devation sum for the processed set of lines to be counted as chess lines
        deviation_max = 100

        for line in lines:
            rho, theta = line
            rhos.append(rho)

        for i in np.arange(0, len(lines) - 8):
            rho_candidates = rhos[i : i + 9]
            rho_diffs = np.asarray(rho_candidates[1:9]) - np.asarray(
                rho_candidates[0:8]
            )
            rho_diff_mean = int(np.mean(rho_diffs))
            rho_abs_deviations = np.abs(rho_diffs - rho_diff_mean)
            max_single_deviation = np.max(rho_abs_deviations)
            rho_deviation_sum = np.sum(rho_abs_deviations)

            if deviation > rho_deviation_sum:
                deviation = rho_deviation_sum
                chess_lines = lines[i : i + 9]

        if deviation > deviation_max:
            return []

        return chess_lines

    if lines is None:
        return None, None

    # Keep horizontal/vertical lines
    horizontal_lines, vertical_lines = getHorizontalAndVerticalLines(lines)

    # Filter out similar lines
    horizontal_lines = removeDuplicateLines(horizontal_lines)
    vertical_lines = removeDuplicateLines(vertical_lines)

    horizontal_lines = keepChessLines(horizontal_lines)
    vertical_lines = keepChessLines(vertical_lines)

    return horizontal_lines, vertical_lines


# Computes the intersections of each horizontal line
# with each vertical line
def getIntersections(h_lines, v_lines):
    if (len(h_lines) != 9) or (len(v_lines) != 9):
        return None

    intersections = np.ndarray((9, 9), tuple)

    for i in np.arange(0, 9):
        h_line = h_lines[i]
        for j in np.arange(0, 9):
            v_line = v_lines[j]
            h_rho, h_theta = h_line
            v_rho, v_theta = v_line
            x_i, y_i = 0, 0

            if v_theta == 0:
                x_i = v_rho
            else:
                x_i = ((h_rho * np.sin(v_theta)) - (v_rho * np.sin(h_theta))) / (
                    (np.cos(h_theta) * np.sin(v_theta))
                    - (np.cos(v_theta) * np.sin(h_theta))
                )
            y_i = (h_rho / np.sin(h_theta)) - (
                x_i * (np.cos(h_theta) / np.sin(h_theta))
            )

            intersections[i, j] = (x_i, y_i)

    return intersections


def detectFigureInField(field):
    pruning_size = 15
    field_detection_threshold = field.shape[0] * field.shape[1] / 42
    # field edge pruning
    field = field[
        pruning_size : field.shape[0] - pruning_size,
        pruning_size : field.shape[1] - pruning_size,
    ]

    pixel_sum = int(np.add.reduce(field, None) / 255)
    """print("Pixel sum: {0} | Threshold: {1}".format(pixel_sum, field_detection_threshold))

    cv2.imshow("Field", field)
    k = cv2.waitKey(0)"""

    if pixel_sum > field_detection_threshold:
        return True

    return False


def getFiguresInFields(fields_black, fields_white):
    figures = np.zeros((2, fields_black.shape[0], fields_black.shape[1]))

    for i in np.arange(fields_black.shape[0]):
        for j in np.arange(fields_black.shape[1]):
            field_black = fields_black[i, j]
            field_white = fields_white[i, j]
            if detectFigureInField(field_black):
                figures[1, i, j] = 1
            elif detectFigureInField(field_white):
                figures[0, i, j] = 1

    return figures


# State comparison return values:
# -1 : invalid
# 0  : no change
# 1  : figure moved
# 2  : figure beaten
def compareStates(last_state, current_state):
    # detect difference between last state and current state
    diff_state = current_state - last_state

    # No move
    if np.add.reduce(np.abs(diff_state), None) == 0:
        return 0, diff_state

    # Standard move
    elif (
        np.add.reduce(np.abs(diff_state), None) == 2
        and np.add.reduce(diff_state, None) == 0
    ):
        return 1, diff_state

    # Figure beaten
    elif (
        np.add.reduce(np.abs(diff_state), None) == 3
        and np.add.reduce(diff_state, None) == -1
    ):
        return 2, diff_state

    # Rochade
    elif (
        np.add.reduce(np.abs(diff_state), None) == 4
        and np.add.reduce(diff_state, None) == 0
    ):
        return 3, diff_state

    else:
        if DEBUG:
            print("Illegal State Change!")
            print(last_state)
            print(current_state)
        return -1, diff_state


def getMoveCoordinates(compare_value, diff_state):
    if DEBUG:
        print("Diff State:" + str(diff_state))
        print("Cmp Value:" + str(compare_value))

    # diff_state = np.flip(diff_state, 0)
    if compare_value == 1:
        i1 = np.where(diff_state.flatten() == -1)[0] % 64
        i2 = np.where(diff_state.flatten() == 1)[0] % 64

        if i1.shape[0] > 1 or i2.shape[0] > 1:
            return None, None

        return ((i1 // 8, i1 % 8), (i2 // 8, i2 % 8))
    elif compare_value == 2:
        # determine if black beat white figure (i0==0) or the other way around
        i0 = np.where(diff_state.flatten() == 1)[0] // 64
        i1 = np.where(diff_state[i0, :].flatten() == -1)[0]
        i2 = np.where(diff_state[i0, :].flatten() == 1)[0]

        if i1.shape[0] > 1 or i2.shape[0] > 1:
            return None, None

        return ((i1 // 8, i1 % 8), (i2 // 8, i2 % 8))
    elif compare_value == 3:
        # determine if valid Rochade
        valid_move_indices = [
            [0, 4, 2, 3],
            [4, 7, 5, 6],
            [56, 60, 58, 59],
            [60, 63, 61, 62],
        ]
        # moved-from indices
        i0, i1 = np.where(diff_state.flatten() == -1)[0] % 64
        # moved-to indices
        i2, i3 = np.where(diff_state.flatten() == 1)[0] % 64

        if [i0, i1, i2, i3] not in valid_move_indices:
            if DEBUG:
                print([i0, i1, i2, i3])
                print("Invalid Move!")
            return None, None

        else:
            if [i0, i1, i2, i3] == [0, 4, 2, 3]:
                return ((0, 4), (0, 2))
            if [i0, i1, i2, i3] == [4, 7, 5, 6]:
                return ((0, 4), (0, 6))
            if [i0, i1, i2, i3] == [56, 60, 58, 59]:
                return ((7, 4), (7, 2))
            if [i0, i1, i2, i3] == [60, 63, 61, 62]:
                return ((7, 4), (7, 6))

import cv2
import numpy as np

def preprocessing(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                 # Convert the input image to a grayscale
    img_threshold = cv2.adaptiveThreshold(src=img_gray, maxValue=255, \
        adaptiveMethod = cv2.ADAPTIVE_THRESH_MEAN_C, thresholdType=cv2.THRESH_BINARY_INV, blockSize=15, C=3)

    return img_threshold


def resize_image(img, factor):
    return cv2.resize(img, (int(img.shape[1]*factor), int(img.shape[0]*factor)), interpolation = cv2.INTER_LINEAR)

# Draws the given lines onto a copy of the given image
# and returns it
def draw_lines(img, lines):
    if lines is None:
        return img

    img_lines = np.copy(img)

    for dline in lines:
        rho,theta = dline
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

def draw_points(img, points):
    if points is None:
        return img

    img_points = np.copy(img)

    for point in points:
        cv2.circle(img_points,point, 10,(0,255,0),-1)

    return img_points

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

# Filters out irrelevant lines (non-horizontal/non-vertical/duplicate)
def filter_lines(lines):
    # Removes lines that are neither horizontally nor vertically aligned
    def get_horizontal_and_vertical_lines(lines):
        vertical_lines=[]
        horizontal_lines=[]

        for line in lines:
            rho, theta = line[0]
            if ((theta > 1.5407) and (theta < 1.6007)):
                horizontal_lines.append((rho, theta))
            elif ((theta > -0.05) and (theta < 0.05)):      
                vertical_lines.append((rho, theta))

        return horizontal_lines, vertical_lines


    # Removes lines that are probably duplicates and returns
    # the remaining ones
    def remove_duplicate_lines(lines):
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
    def keep_chess_lines(lines):
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

        for i in np.arange(0, len(lines)-8):
            rho_candidates = rhos[i:i+9]
            rho_diffs = np.asarray(rho_candidates[1:9]) - np.asarray(rho_candidates[0:8])
            rho_diff_mean = int(np.mean(rho_diffs))
            rho_abs_deviations = np.abs(rho_diffs - rho_diff_mean)
            max_single_deviation = np.max(rho_abs_deviations) 
            rho_deviation_sum = np.sum(rho_abs_deviations)

            if deviation > rho_deviation_sum:
                deviation = rho_deviation_sum
                chess_lines = lines[i:i+9]
        
        if deviation > deviation_max:
            return []

        return chess_lines
    
    if lines is None:
        return None, None

    # Keep horizontal/vertical lines
    horizontal_lines, vertical_lines = get_horizontal_and_vertical_lines(lines)

    # Filter out similar lines
    horizontal_lines = remove_duplicate_lines(horizontal_lines)
    vertical_lines = remove_duplicate_lines(vertical_lines)

    horizontal_lines = keep_chess_lines(horizontal_lines)
    vertical_lines = keep_chess_lines(vertical_lines)

    return horizontal_lines, vertical_lines

# Computes the intersections of each horizontal line
# with each vertical line
def get_intersections(h_lines, v_lines):
    if (len(h_lines) != 9) or (len(v_lines) != 9):
        return None

    intersections = np.ndarray((9,9), tuple)

    for i in np.arange(0, 9):
        h_line = h_lines[i]
        for j in np.arange(0, 9):
            v_line = v_lines[j]
            h_rho, h_theta = h_line
            v_rho, v_theta = v_line
            x_i, y_i = 0, 0

            if (v_theta == 0):
                x_i = v_rho
            else:
                x_i = ((h_rho * np.sin(v_theta)) - (v_rho * np.sin(h_theta))) / \
                    ((np.cos(h_theta) * np.sin(v_theta)) - (np.cos(v_theta) * np.sin(h_theta)))
            y_i = ((h_rho / np.sin(h_theta)) - (x_i * (np.cos(h_theta) / np.sin(h_theta))))
                
            intersections[i,j] = (x_i, y_i)

    return intersections

def detect_figure_in_field(field):
    pruning_size = 10
    field_detection_threshold = field.shape[0]*field.shape[1]/16
    # field edge pruning
    field = field[pruning_size:field.shape[0]-pruning_size, pruning_size:field.shape[1]-pruning_size]

    pixel_sum = int(np.add.reduce(field, None)/255)
    """print("Pixel sum: {0} | Threshold: {1}".format(pixel_sum, field_detection_threshold))

    cv2.imshow("Field", field)
    k = cv2.waitKey(0)"""

    if (pixel_sum > field_detection_threshold):
        return True

    return False


def get_figures_in_fields(fields):
    figures = np.zeros_like(fields)

    for i in np.arange(fields.shape[0]):
        for j in np.arange(fields.shape[1]):
            field = fields[i,j]
            if detect_figure_in_field(field):
                figures[i,j] = 1
    
    return figures

# State comparison return values:
# -1 : invalid
# 0  : no change
# 1  : figure moved
# 2  : figure beaten
def compare_states(last_state, current_state):
    # detect difference between last state and current state
    diff_state = current_state - last_state

    if not np.add.reduce(diff_state, None) == 0 or (not np.add.reduce(np.abs(diff_state), None) <= 2):
        print("Illegal State Change!")
        return -1, diff_state

    elif np.add.reduce(np.abs(diff_state), None) == 0:
        return 0, diff_state

    elif np.add.reduce((diff_state), None) == -1:
        return 2, diff_state
    
    else:
        return 1, diff_state

def get_move_coordinates(compare_value, diff_state):
    if compare_value == 1:
        i1 = np.where(diff_state.flatten()==-1)[0]
        i2 = np.where(diff_state.flatten()==1)[0]
        return ((i1//8,i1%8), (i2//8,i2%8))
    if compare_value == 2:
        pass
    
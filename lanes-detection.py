# import cv2
# import numpy as np
# import mss


# def canny(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     canny = cv2.Canny(blur, 50, 150)
#     return canny


# def display_lines(image, lines):
#     line_image = np.zeros_like(image)
#     if lines is not None:
#         for x1, y1, x2, y2 in lines:
#             cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
#     return line_image


# def region(image):
#     # height = image.shape[0]
#     height = 400
#     polygons = np.array([[(200, height), (1900, height), (950, 250)]])
#     mask = np.zeros_like(image)
#     cv2.fillPoly(mask, polygons, 255)
#     masked_image = cv2.bitwise_and(image, mask)
#     return masked_image


# def average_slope_intercept(image, lines):
#     left_fit = []
#     right_fit = []

#     if lines is None:
#         return None

#     for line in lines:
#         x1, y1, x2, y2 = line.reshape(4)
#         parameters = np.polyfit((x1, x2), (y1, y2), 1)
#         slope = parameters[0]
#         intercept = parameters[1]
#         if slope < 0:
#             left_fit.append((slope, intercept))
#         else:
#             right_fit.append((slope, intercept))

#     left_fit_average = np.average(left_fit, axis=0)
#     right_fit_average = np.average(right_fit, axis=0)

#     left_line = make_coordinates(image, left_fit_average) if left_fit_average is not None else None
#     right_line = make_coordinates(image, right_fit_average) if right_fit_average is not None else None

#     return np.array([line for line in [left_line, right_line] if line is not None])


# def make_coordinates(image, line_parameters):
#     if line_parameters is None:
#         return None
#     slope, intercept = line_parameters
#     # y1 = image.shape[0]
#     y1 = 400
#     y2 = int(y1 * (3 / 5))
#     x1 = int((y1 - intercept) / slope)
#     x2 = int((y2 - intercept) / slope)
#     return np.array([x1, y1, x2, y2])


# with mss.mss() as sct:
#     monitor = sct.monitors[1]

#     while True:
#         screenshot = sct.grab(monitor)
#         frame = np.array(screenshot)
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

#         # Process the frame for lane detection
#         canny_image = canny(frame)
#         cropped_image = region(canny_image)
#         lines = cv2.HoughLinesP(
#             cropped_image,
#             2,
#             np.pi / 180,
#             100,
#             np.array([]),
#             minLineLength=40,
#             maxLineGap=5,
#         )
#         average_lines = average_slope_intercept(frame, lines)
#         line_image = display_lines(frame, average_lines)
#         merge_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

#         # Display the result
#         cv2.imshow("Screen Lane Detection", merge_image)

#         # Exit on pressing 'q'
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

# cv2.destroyAllWindows()


import cv2
import numpy as np
import matplotlib.pyplot as plt


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


def region(image):
    # height = image.shape[0]
    height = 400
    polygons = np.array([[(200, height), (1900, height), (950, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []

    if lines is None:
        return None

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)

    print(left_fit_average, right_fit_average)

    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)

    return np.array([left_line, right_line])


def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    # y1 = image.shape[0]
    y1 = 400
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


image = cv2.imread("./lane/lane1.png")
lane_image = np.copy(image)
canny_image = canny(lane_image)
cropped_image = region(canny_image)
lines = cv2.HoughLinesP(
    cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5
)
average_lines = average_slope_intercept(lane_image, lines)
line_image = display_lines(lane_image, average_lines)

merge_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

cv2.imshow("result", merge_image)
cv2.waitKey(0)
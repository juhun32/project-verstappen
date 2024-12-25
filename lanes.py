import cv2
import numpy as np


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
    height, width = image.shape[:2]
    polygons = np.array(
        [[(200, height), (width - 200, height), (width // 2, int(height * 0.6))]]
    )
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

    left_fit_average = np.average(left_fit, axis=0) if left_fit else None
    right_fit_average = np.average(right_fit, axis=0) if right_fit else None

    left_line = (
        make_coordinates(image, left_fit_average)
        if left_fit_average is not None
        else None
    )
    right_line = (
        make_coordinates(image, right_fit_average)
        if right_fit_average is not None
        else None
    )

    return np.array([line for line in [left_line, right_line] if line is not None])


def make_coordinates(image, line_parameters):
    if line_parameters is None:
        return None
    slope, intercept = line_parameters
    # height = image.shape[0]
    height = 400
    y1 = height
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    canny_image = canny(frame)
    cropped_image = region(canny_image)
    lines = cv2.HoughLinesP(
        cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5
    )
    average_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, average_lines)
    merge_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    cv2.imshow("Lane Detection", merge_image)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

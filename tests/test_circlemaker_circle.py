import sys, os, colorsys, subprocess
import pytest, cv2 as cv
from utils.circledetector import CircleDetector


# This is needed so that python can recognize the pyspix
THIS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
IMAGES_DIR = f"{ROOT_DIR}\\src\\images\\"

try:
    os.makedirs(IMAGES_DIR)
except FileExistsError:
    # directory already exists
    pass


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def rgb2hsv(rgb):
    red_percentage = rgb[0] / float(255)
    green_percentage = rgb[1] / float(255)
    blue_percentage = rgb[2] / float(255)

    # get hsv percentage: range (0-1, 0-1, 0-1)
    color_hsv_percentage = colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage)
    # get normal hsv: range (0-360, 0-255, 0-255)
    color_h = round(360 * color_hsv_percentage[0])
    color_s = round(255 * color_hsv_percentage[1])
    color_v = round(255 * color_hsv_percentage[2])
    color_hsv = (color_h, color_s, color_h)

    return color_hsv


def value_within_range(actual_v, expected_v, tolerance):
    return actual_v >= (expected_v - tolerance) and actual_v <= (expected_v + tolerance)


@pytest.mark.parametrize(
    "d,hue,expected_r,expected_hsv,r_tolerance,h_tolerance",
    {
        (40, 0, 20, (0, 100, 100), 1, 1),  # (d,hue ,r, hsv, r_tolerance, h_tolerance)
        (151, 360, 75.5, (0, 100, 100), 1, 1),  # I should expect 360 instead of 0 for the hue, but the 0 is due to the conversion
    },
)
def test_corner_hue(d, hue, expected_r, expected_hsv, r_tolerance, h_tolerance):

    _, _, returncode = capture(f"python {ROOT_DIR}\\src\\circlemaker.py -d {d} -hue {hue} -path {IMAGES_DIR}\\test.png")

    assert returncode == 0

    img_path = cv.imread(f"{IMAGES_DIR}\\test.png")
    circle = CircleDetector(img_path=img_path, circle_hue=hue)

    # assert the circle radius
    circle_r = circle.get_circle_radius()
    assert value_within_range(circle_r, expected_r, r_tolerance)

    # assert the circle color
    circle_color_h, _, _ = rgb2hsv(circle.get_circle_rgb_color())
    expected_color_h = expected_hsv[0]
    assert value_within_range(circle_color_h, expected_color_h, h_tolerance)


@pytest.mark.parametrize(
    "d,hue,expected_r,expected_hsv,r_tolerance,h_tolerance",
    {
        (3, 200, 1.5, (200, 100, 100), 1, 1),  # (d,hue ,r, hsv, r_tolerance, h_tolerance)
        (399, 150, 199, (150, 100, 100), 1, 1),
    },
)
def test_acceptable_corner_d(d, hue, expected_r, expected_hsv, r_tolerance, h_tolerance):

    _, _, returncode = capture(f"python {ROOT_DIR}\\src\\circlemaker.py -d {d} -hue {hue} -path {IMAGES_DIR}\\test.png")

    assert returncode == 0

    img_path = cv.imread(f"{IMAGES_DIR}\\test.png")
    circle = CircleDetector(img_path=img_path, circle_hue=hue)

    # assert the circle radius
    circle_r = circle.get_circle_radius()
    assert value_within_range(circle_r, expected_r, r_tolerance)

    # assert the circle color
    circle_color_h, _, _ = rgb2hsv(circle.get_circle_rgb_color())
    expected_color_h = expected_hsv[0]
    assert value_within_range(circle_color_h, expected_color_h, h_tolerance)


@pytest.mark.parametrize(
    "d,hue,expected_result",
    {
        (0, 200, None),  # (d,hue ,r, hsv, r_tolerance, h_tolerance)
        (2, 100, None),
    },
)
def test_unacceptable_corner_d(d, hue, expected_result):

    _, _, returncode = capture(f"python {ROOT_DIR}\\src\\circlemaker.py -d {d} -hue {hue} -path {IMAGES_DIR}\\test.png")

    assert returncode == 0

    img_path = cv.imread(f"{IMAGES_DIR}\\test.png")
    circle = CircleDetector(img_path=img_path, circle_hue=hue)

    # assert the circle doesn't exist
    circle_r = circle.get_circle_radius()
    assert circle_r == expected_result


@pytest.mark.parametrize(
    "d,hue,expected_r,expected_hsv,r_tolerance,h_tolerance",
    {
        (7, 1, 3.5, (1, 100, 100), 1, 1),  # odd low d and hue values
        (8, 2, 4, (2, 100, 100), 1, 1),  # even low d and hue values
        (395, 359, 197.5, (359, 100, 100), 1, 1),  # odd high d and hue values
        (396, 358, 198, (358, 100, 100), 1, 1),  # even high d and hue values
    },
)
def test_odd_even_values(d, hue, expected_r, expected_hsv, r_tolerance, h_tolerance):

    _, _, returncode = capture(f"python {ROOT_DIR}\\src\\circlemaker.py -d {d} -hue {hue} -path {IMAGES_DIR}\\test.png")

    assert returncode == 0

    img_path = cv.imread(f"{IMAGES_DIR}\\test.png")
    circle = CircleDetector(img_path=img_path, circle_hue=hue)

    # assert the circle radius
    circle_r = circle.get_circle_radius()
    assert value_within_range(circle_r, expected_r, r_tolerance)

    # assert the circle color
    circle_color_h, _, _ = rgb2hsv(circle.get_circle_rgb_color())
    expected_color_h = expected_hsv[0]
    assert value_within_range(circle_color_h, expected_color_h, h_tolerance)

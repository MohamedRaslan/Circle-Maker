import sys, os, subprocess
import pytest, cv2 as cv
from utils.circledetector import CircleDetector


# This is needed so that python can recognize the pyspix
THIS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
IMAGES_DIR = f"{ROOT_DIR}/src/images/"

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


@pytest.mark.smoke
@pytest.mark.parametrize(
    "d,hue,expected_result",
    {
        (-1, 350, (2, "error: argument -d: Argument must be within 0 <= arg <= 399")),  # (d,hue ,(error_code, message))
        (400, 350, (2, "error: argument -d: Argument must be within 0 <= arg <= 399")),
        (None, 320, (2, "error: argument -d: Argument must be a float type number")),
    },
)
def test_d_out_of_range(d, hue, expected_result):

    out, err, returncode = capture(f"python {ROOT_DIR}/src/circlemaker.py -d {d} -hue {hue} -path {IMAGES_DIR}/test.png")

    assert returncode == expected_result[0]
    assert expected_result[1] in str(err)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "d,hue,expected_result",
    {
        (50, -1, (2, "error: argument -hue: Argument must be within 0 <= arg <= 360")),  # (d,hue ,(error_code, message))
        (250, 361, (2, "error: argument -hue: Argument must be within 0 <= arg <= 360")),
        (320, None, (2, "error: argument -hue: Argument must be a float type number")),
    },
)
def test_hue_out_of_range(d, hue, expected_result):

    out, err, returncode = capture(f"python {ROOT_DIR}/src/circlemaker.py -d {d} -hue {hue} -path {IMAGES_DIR}/test.png")

    assert returncode == expected_result[0]
    assert expected_result[1] in str(err)


@pytest.mark.parametrize(
    "d,hue,expected_result",
    {
        (-10, -1, (2, "error: argument -d: Argument must be within 0 <= arg <= 399")),  # (d,hue ,(error_code, message))
        (400, 450, (2, "error: argument -d: Argument must be within 0 <= arg <= 399")),
        ("notNumber", "NotNumber", (2, "error: argument -d: Argument must be a float type number")),
    },
)
def test_both_out_of_range(d, hue, expected_result):

    out, err, returncode = capture(f"python {ROOT_DIR}/src/circlemaker.py -d {d} -hue {hue} -path {IMAGES_DIR}/test.png")

    assert returncode == expected_result[0]
    assert expected_result[1] in str(err)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "d,hue,expected_result",
    {
        (30, 15, (0, "")),  # (d,hue ,(error_code, message))
        (40, 60, (0, "")),
    },
)
def test_both_on_range(d, hue, expected_result):

    out, err, returncode = capture(f"python {ROOT_DIR}/src/circlemaker.py -d {d} -hue {hue} -path {IMAGES_DIR}/test.png")

    assert returncode == expected_result[0]
    assert expected_result[1] in str(err)

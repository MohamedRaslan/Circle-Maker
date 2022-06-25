import sys, os, subprocess
import cv2 as cv
from utils.circledetector import CircleDetector


# This is needed so that python can recognize the pyspix
THIS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
IMAGES_DIR = f"{ROOT_DIR}\\images\\"

try:
    os.makedirs(IMAGES_DIR)
except FileExistsError:
    # directory already exists
    pass


def test_try():
    x = 0
    for d in range(5, 50, 2):
        subprocess.call(f"python {ROOT_DIR}\\src\\circlemaker.py -d {d} -hue {x} -path {IMAGES_DIR}\\test.png")
        img_path = cv.imread(f"{IMAGES_DIR}\\test.png")
        circle = CircleDetector(img_path=img_path, circle_hue=x)
        dr = circle.get_circle_radius()
        print(f"For r= {d/2} the detected circle r was {dr}")
        # assert abs(dr - (d / 2)) >= 0 and abs(dr - (d / 2)) < 1

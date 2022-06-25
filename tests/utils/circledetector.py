"""_summary_
    This module handles the different ways to detect the circle and extract the circle color and radius

    Cautions: Give the use of CV2 keep in mind the following
     * HSV range in CV2: Hue range is [0,179] "or [0, 255] for COLOR_BGR2HSV_FULL" not [0 360], Saturation range is [0,255] and Value range is [0,255] not [0 100%]
     * For approximations cv2 uses nearest integer rounding
"""
import cv2 as cv, numpy as np, math


class CircleDetector:
    """_summary_

    The main class for detecting circles produced by circlemaker and extract the circle color and radius

      Args:
         img_path    (string): the path of the image produced circle maker.
         circle_hue  (int): the expected hue of the circle in a range of [0 360].
         color_range (tuple, optional): Color tolerance. Defaults to (1,0,0).
         crop_img    (bool, optional): crop the border from the image. Defaults to True.
    """

    def __init__(self, img_path, circle_hue, color_range=(1, 0, 0), crop_img=True):
        self.__img = img_path
        if crop_img:
            self.__img = self.__img[1:-1, 1:-1]  # without the border
        self.__circle_hsv = self.__get_hsv_color((circle_hue, 100, 100))

        circle_area = math.pi * math.pow(round(len(self.__img) / 2), 2)
        self.__max_circle_area = circle_area + 1000  # the "1000" is just an additional tolerance
        if self.__circle_hsv[0] == 255:  # just to handle the image h values that get converted to 0
            self.__minHSV = (
                0,
                self.__circle_hsv[1] - color_range[1],
                self.__circle_hsv[2] - color_range[2],
            )

            self.__maxHSV = (
                color_range[0],
                self.__circle_hsv[1] + color_range[1],
                self.__circle_hsv[2] + color_range[2],
            )
        else:
            self.__minHSV = (
                self.__circle_hsv[0] - color_range[0],
                self.__circle_hsv[1] - color_range[1],
                self.__circle_hsv[2] - color_range[2],
            )

            self.__maxHSV = (
                self.__circle_hsv[0] + color_range[0],
                self.__circle_hsv[1] + color_range[1],
                self.__circle_hsv[2] + color_range[2],
            )

        self.__circle_detected = False
        self.__circle = None

    def __get_hsv_color(self, normal_hsv_color):
        """_summary_
        Convert hsv numbers from normal 360 100% 100% to the CV2 hsv numbers [179,255,255]
        Args:
            normal_hsv_color (tuple): hsv color in normal range ([ 0 360] , [ 0 100%] , [0 100%])
        """
        h = round((normal_hsv_color[0] / 360) * 255)
        s = round((normal_hsv_color[1] / 100) * 255)
        v = round((normal_hsv_color[2] / 100) * 255)
        return (h, s, v)

    def __get_masked_image(self):
        """_summary_
        Clean an image and return the image in BRG color with only the needed hsv_color

        Args:
            img (cv2.image): the cv2 image that you need to clean it
            hsv_color (tuple): the mask color in normal range ([ 0 360] , [ 0 100%] , [0 100%])
            color_range (tuple, optional): Color tolerance. Defaults to (1,0,0).

        Returns:
            cv2.image: the BGR masked image
        """

        img = self.__img.copy()
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV_FULL)

        mask = cv.inRange(hsv_img, self.__minHSV, self.__maxHSV)

        return cv.bitwise_and(img, img, mask=mask)

    def __circle_detection_by_minEnclosingCircle(self):
        """_summary_

        This method depend on the cv2 minEnclosingCircle
        This method is by far the most accurate way with the lowest assumptions

        Cautions:
        * The method can't detect accurately circle with radius less than 1.5px (diameter == 3px)
        * The method detect the circle radius with accuracy equal to the actual value +/- 1 px "+/- 2 px of the circle diameter"

        Args:
            img (cv2.image): the cv2 image

        Returns:
            list (tuples): number of the circles found
        """

        gray_img = cv.cvtColor(self.__get_masked_image(), cv.COLOR_BGR2GRAY)

        # gray_img = cv.medianBlur(gray_img, 11) # commented out no need for it

        _, thresh = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # Not commented out but actually no need for it

        # Morph open --> commented out no need for it
        # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
        # opening = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=3)

        # Find contours and filter using contour area and aspect ratio
        contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for c in contours:
            peri = cv.arcLength(c, True)
            approx = cv.approxPolyDP(c, 0.0001 * peri, True)
            area = cv.contourArea(c)
            if len(approx) > 5 and area > 1 and area < self.__max_circle_area:
                ((x, y), r) = cv.minEnclosingCircle(c)
                return r
        return None

    def __circle_detection_by_houghCircles(self):
        """_summary_

        This method depend on the cv2 houghCircles method

        Cautions:
        * The method can't detect small circles with radius less than 15px  "diameter less than 30px"
        * The method detect the circle radius with accuracy equal to the actual value +/- 5 pixel "+/- 10 pixel of the circle diameter"

        Args:
            img (cv2.image): the cv2 image

        Returns:
            list (tuples): number of the circles found
        """
        # detect circles in the image, most of the values are an arbitrary number chosen after trial and error
        gray_img = cv.cvtColor(self.__get_masked_image(), cv.COLOR_BGR2GRAY)
        circles = cv.HoughCircles(
            image=gray_img,
            method=cv.HOUGH_GRADIENT,
            dp=3.2,
            minDist=200,
            param1=120,
            param2=60,
            minRadius=15,
            maxRadius=200,
        )
        # ensure at least some circles were found
        if circles is not None and len(circles) == 1:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            (x, y, r) = circles[0]
            return r

        return None

    def __circle_detection_naive_method(self):
        """_summary_

        This is a very naive solution: I will check the pixel color in the centre of
        the image if it is within the accepted color then I will move to the -x direction
        until I reach to unaccepted color or the image board and return my steps.

        This solution base on the following facts/assumptions:
        * The center of the circle is always the center of the image
        * It will be always circle and the only use is to get the radius not to validate its a circle
        * It is always with one color not a gradient

        Cautions:
        * The method should not be used if the previous assumptions may changes
        * The method can't detect accurately circle with radius less than 2
        * The method detect the circle radius with accuracy equal to the actual value +/- 0.5 pixel "+/- 1 pixel of the circle diameter"


        Args:
            img (cv2.image): the cv2 image
            hsv_color (tuple): the mask color
            color_range (tuple, optional): Color tolerance. Defaults to (1,0,0).

        Returns:
        int : the circle radius or None of radius less than 2
        """
        img = self.__img.copy()
        hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV_FULL)

        img_size = len(img)
        x = int(img_size / 2)
        y = int(img_size / 2)
        while self.__pixel_color_within_range(hsv_image, (x - 1, y - 1)):
            x -= 1
            if x <= 0:
                break
        r = int(img_size / 2) - x

        if r < 2:  # for r less than 2 the results are not accurate hence returning none
            return None

        return r

    def __pixel_color_within_range(self, img, loc, minHSV, maxHSV):
        """_summary_
        returns true if the color of the pixel at the specified location was within the needed color range
        Args:
            img : is cv2 hsv image
            loc : location (x,y) on the image
        """
        minHSV = self.__minHSV
        maxHSV = self.__maxHSV
        h, s, v = img[loc[0], loc[1]]
        if h >= (minHSV[0]) and s >= (minHSV[1]) and v >= (minHSV[2]):
            return h <= (maxHSV[0]) and s <= (maxHSV[1]) and v <= (maxHSV[2])
        return False

    def get_circle_rgb_color(self):
        """_summary_
        If a circle is detected it will return its color in RGB space otherwise none
        """

        if self.__circle_detected == False and self.__circle is None:

            # Detect the circle
            self.__circle = self.__circle_detection_by_minEnclosingCircle()
            self.__circle_detected = True

        if self.__circle is not None:
            x = round(len(self.__img) / 2)
            (b, g, r) = self.__img[x, x]
            return (r, g, b)

        return None

    def get_circle_radius(self):
        """_summary_
        If a circle is detected it will return its radius otherwise none
        """
        if self.__circle_detected == False and self.__circle is None:

            # Detect the circle
            self.__circle = self.__circle_detection_by_minEnclosingCircle()
            self.__circle_detected = True

        return self.__circle

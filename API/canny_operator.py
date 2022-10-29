import cv2
import sys
from utils import *
from datetime import datetime


class CannyOperator:

    def __init__(self, image_data):
        self.image_data = image_data

    def detect_edge(self):
        self.edges = cv2.Canny(self.image_data, 100, 200, 3, L2gradient=True)
        self.contours, _ = cv2.findContours(self.edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    def enclose(self):
        pass

    def save(self):
        #cv2.imwrite(f"pictures/{datetime.now()}.png", self.edges)
        drawing_img = np.zeros_like(self.edges)
        cv2.drawContours(drawing_img, self.contours, 0, (255), 1)
        cv2.imwrite(f"pictures/test.png", drawing_img)

    def main(self):
        self.detect_edge()
        self.save()
        return self.edges


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Usage: python canny_operator.py image_file")
    name = sys.argv[1]
    img_d = cv2.imread(name)
    edge = CannyOperator(img_d)
    edge.main()



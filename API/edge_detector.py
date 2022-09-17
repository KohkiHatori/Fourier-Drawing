import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('apple.png')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img, 100, 200, 3, L2gradient=True)
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

drawing_img = np.zeros_like(edges)
cv2.drawContours(drawing_img, contours, 0, (255), 1)
#cv2.imwrite('test.png', drawing_img)



plt.imsave('apple.png', edges, cmap='gray', format='png')

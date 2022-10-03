import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
point1 = [1, 2]
point2 = [3, 4]
point3 = [2, 1]
x_values = [point1[0], point2[0]]
y_values = [point1[1], point2[1]]
plt.plot(x_values, y_values, 'bo', linestyle="--")
plt.plot([2, 2.5],[1, 3], 'bo', linestyle="--")
plt.show()

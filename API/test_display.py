from config import *
from function import Function
from IPython import display



class ComplexVector:

    def __init__(self, coefficient, n):
        self.coefficient = coefficient
        self.n = n

    def func(self, t):
        return self.coefficient * (E ** (self.n * 2 * PI * 1j * t))


def sum_comp_vec(vectors, t):
    sum = 0
    for vector in vectors:
        sum += vector.func(t)
    return sum


def create_vec_data(compVectors, t):
    data = []
    for vector in compVectors:
        data.append([vector.func(t).real, vector.func(t).imag])
    data = np.array(data)
    origin = np.insert(data, 0, [0, 0], axis=0)
    origin = np.delete(origin, -1, axis=0)
    origin = origin.transpose()
    origin = origin.cumsum(axis=1)
    return data, origin

def animate(compVectors):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(19,10))
    ax = plt.axes(xlim=(-12, 12), ylim=(-12, 12))
    plt.gca().set_aspect('equal', adjustable='box')
    line, = plt.plot([], [], lw=2)
    xdata = []
    ydata = []
    vecs = [plt.plot([], [], linewidth=0.5)[0] for _ in range(len(compVectors))]
    circles = [plt.Circle([],[]) for _ in range(len(compVectors))]
    def update(i):
        t = i*0.001
        x = 0
        y = 0
        for vector, plot, circle in zip(compVectors, vecs, circles):
            x_updated = x + vector.func(t).real
            y_updated = y + vector.func(t).imag
            plot.set_data([x, x_updated], [y, y_updated])
            x = x_updated
            y = y_updated
            #    circle = plt.Circle(tuple(centre), abs(vector.func(t)), fill=False)
            #    ax.add_patch(circle)
            #    centre += np.array([vector.func(t).real, vector.func(t).imag]
            #plt.quiver(*origin, data[:, 0], data[:, 1], scale=1,scale_units="xy")
        xdata.append(x)
        ydata.append(y)
        line.set_data(xdata, ydata)
        data, origin = create_vec_data(compVectors, t)
        return line, *vecs

    ani = FuncAnimation(fig, update, frames=range(5000), interval=1, repeat=True, blit=True)
    plt.show()

def frame(compVectors, t):
    #plt.style.use('dark_background')
    fig = plt.figure()
    ax = plt.axes(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
    plt.gca().set_aspect('equal', adjustable='box')
    centre = np.array([0.0, 0.0])
    for vector in compVectors:
        circle = plt.Circle(tuple(centre), abs(vector.func(t)), fill=False)
        ax.add_patch(circle)
        centre += np.array([vector.func(t).real, vector.func(t).imag])
    data, origin = create_vec_data(compVectors, t)
    plt.quiver(*origin, data[:, 0], data[:, 1], scale=1, scale_units="xy", color="blue")
    plt.show()

if __name__ == "__main__":
    # myfunc = lambda x: complex(math.cos(2*PI*x), (math.sin(2*PI*x)))
    myfunc = lambda t: complex(5*COS(4*PI*t), 5*SIN(6*PI*t)+5*SIN(4*PI*t))
    values = [myfunc(x) for x in np.arange(0, 1 + DT, DT)]
    vdict = dict(zip(np.arange(0, 1 + DT, DT), values))
    func = Function(vdict)
    coeffs = func.get_coefficients()
    index = len(coeffs)//2 - (len(coeffs) % 2 == 0)
    steps = []
    for i in range(len(coeffs)):
        steps.append(index)
        index += (-1) ** (i % 2 != 0) * (i + 1)
    compVectors = [ComplexVector(coeffs[list(coeffs.keys())[i]], list(coeffs.keys())[i]) for i in steps]
    animate(compVectors)


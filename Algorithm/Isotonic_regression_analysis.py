import numbers
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def IsotonicRegression(X, y, weight=None):
    # If weight is not None, check the value is positive
    # else give ones
    if weight is not None:
        for i in range(len(weight)):
            if weight[i] <= 0:
                weight[i] = 1.
    else:
        weight = np.ones(len(y))

    y_ir = np.copy(y)
    y_new = np.copy(y_ir)
    weight_new = np.copy(weight)
    j = 0
    # floor_end is the end index of each step of isotonic regression
    floor_end = [ 0 for i in range(len(y)) ]
    floor_end[0], floor_end[1] = 0, 1
    for i in np.arange(1, len(y)):
        j += 1
        y_new[j] = y_ir[i]
        weight_new[j] = weight[i]
        while j > 0 and y_new[j] < y_new[j-1]:
            y_new[j-1] = (weight_new[j] * y_new[j]\
                        + weight_new[j-1] * y_new[j-1])\
                        / (weight_new[j] + weight_new[j-1])
            # set weight as number of points of each floor
            weight_new[j-1] += weight_new[j]
            j -= 1
        floor_end[j] = i
    # set result y of isotonic regression
    for k in np.arange(1, j+1):
        for l in np.arange(floor_end[k-1]+1, floor_end[k]+1):
            y_ir[l] = y_new[k]
    return y_ir

def LinearRegression(X, y):
    X_, y_ = np.copy(X), np.copy(y)
    n = np.size(X_)
    slope = (n * np.sum(X_ * y_) - (np.sum(X_) * np.sum(y_)))\
            / (n * np.sum(X_**2) - (np.sum(X_))**2)
    intercept = (np.sum(y_) - slope * np.sum(X_)) / n
    y_lr = slope * X_ + intercept
    return y_lr

def check_random_state(seed):
    # Turn seed into a np.random.RandomState instance
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)

if __name__ == '__main__':
    n = 100
    x = np.arange(n)
    #rs = check_random_state(0)
    #y = rs.randint(-50, 50, size=(n,)) + 50. * np.log1p(np.arange(n))
    y = np.random.uniform(-50, 50, n) + 50. * np.log1p(np.arange(n))
    #y = np.random.randn(100) * 30 + 50. * np.log1p(np.arange(n))

    # #############################################################################
    # Fit IsotonicRegression and LinearRegression models

    y_ir = IsotonicRegression(x, y)
    y_lr = LinearRegression(x, y)

    # #############################################################################
    # Plot result

    segments = [[[i, y[i]], [i, y_ir[i]]] for i in range(n)]
    lc = LineCollection(segments, zorder=0)
    lc.set_array(np.ones(len(y)))
    lc.set_linewidths(np.full(n, 0.5))

    fig = plt.figure()
    plt.plot(x, y, 'r.', markersize=12)
    plt.plot(x, y_ir, 'g.-', markersize=12)
    plt.plot(x, y_lr, 'b-')
    plt.gca().add_collection(lc)
    plt.legend(('Data', 'Isotonic Fit', 'Linear Fit'), loc='lower right')
    plt.title('Isotonic regression')
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
import colorcet as cc


def plot_barnsley_fern(n_points=100000,
                       A1=np.array([[0.0, 0.0], [0.0, 0.16]]),
                       b1=np.array([0.0, 0.0]),
                       A2=np.array([[.85, .04], [-0.04, 0.85]]),
                       b2=np.array([0.0, 1.6]),
                       A3=np.array([[0.20, -0.26], [0.23, 0.22]]),
                       b3=np.array([0.0, 1.6]),
                       A4=np.array([[-0.15, 0.28], [0.26, 0.24]]),
                       b4=np.array([0.0, 0.44]),
                       **kwargs,
                       ):

    X = np.zeros((2, n_points))
    u = np.random.rand(n_points-1)

    for i in range(n_points-1):
        if u[i] < 0.85:
            X[:, i+1] = A2 @ X[:, i] + b2
        elif u[i] < 0.92:
            X[:, i+1] = A3 @ X[:, i] + b3
        elif u[i] < 0.99:
            X[:, i+1] = A4 @ X[:, i] + b4
        else:
            X[:, i+1] = A1 @ X[:, i] + b1

    fig, ax = plt.subplots(1, 1, figsize=(10, 20))
    ax.set_xlim([-2.5, 3.75])
    ax.set_ylim([-.1, 12.4])
    ax.scatter(X[0, :], X[1, :], s=1, marker='.')

    fig.savefig('barnsley_plot.png')

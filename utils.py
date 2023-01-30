import numpy as np
from plotly import graph_objects as go


def make_noise(data: np.array, mu=0.01):
    return data * np.random.normal(1, mu, len(data))


def hill(x: float, scale=1, height=1):
    def f(x):
        return -(x - 1) ** 2 + 1

    x = x / scale
    y = f(x)
    return (np.sign(y) + 1) / 2 * y * height


def mnk(X, Y):
    return np.sum(X * Y) / np.sum(X * X)
import numpy as np
# import scipy as sp
import scipy.optimize
import scipy.special
import matplotlib.pyplot as plt

def plot_with_arrow(x, y, xlabel=None, ylabel=None, custom_title=None):
  plt.plot(x, y)
  if custom_title is not None:
    plt.title(custom_title)
  if xlabel is not None:
    plt.xlabel(xlabel)
  if ylabel is not None:
    plt.ylabel(ylabel)
  arrow_length = 0.05
  dx = x[-1]-x[-2]
  dy = y[-1]-y[-2]
  theta = np.arctan2(dy, dx)
  plt.arrow(x[-2], y[-2], np.cos(theta)*arrow_length, np.sin(theta)*arrow_length, head_width=0.01, head_length=0.01, length_includes_head=True)
  plt.show()

def plot_2x1(xaxis, upper, lower, xlabel=None, upper_ylabel=None, lower_ylabel=None, custom_title=None):
  fig, (ax1, ax2) = plt.subplots(2, 1)

  ax1.plot(xaxis, upper)
  if upper_ylabel is not None:
    ax1.set_ylabel(upper_ylabel)

  ax2.plot(xaxis, lower)
  if lower_ylabel is not None:
    ax2.set_ylabel(lower_ylabel)

  if xlabel is not None:
    ax2.set_xlabel(xlabel)
  if custom_title is not None:
    fig.suptitle(custom_title)

  plt.show()
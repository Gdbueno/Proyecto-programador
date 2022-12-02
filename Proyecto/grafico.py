import matplotlib.axes
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import io
import base64

import matplotlib
matplotlib.use('Agg')


def graficar(x, y, ex, ey, tit):

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(x, y)
    ax.grid('solid')
    ax.set_facecolor('whitesmoke')
    plt.xlabel(ex)
    plt.ylabel(ey)
    plt.title(tit)

    image_html = io.BytesIO()
    FigureCanvas(fig).print_png(image_html)
    plt.close(fig)
    return image_html

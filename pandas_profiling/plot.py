try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')


def _plot_histogram(series, bins=10, figsize=(6, 4), facecolor='#337ab7'):
    """Plot an histogram from the data and return the AxesSubplot object.

    Parameters
    ----------
    series: Series, default None
        The data to plot
    figsize: a tuple (width, height) in inches, default (6,4)
        The size of the figure.
    facecolor: str
        The color code.

    Returns
    -------
    matplotlib.AxesSubplot, The plot.
    """
    if get_vartype(series) == 'DATE':
        # TODO: These calls should be merged
        fig = plt.figure(figsize=figsize)
        plot = fig.add_subplot(111)
        plot.set_ylabel('Frequency')
        try:
            plot.hist(series.values, facecolor=facecolor, bins=bins)
        except TypeError: # matplotlib 1.4 can't plot dates so will show empty plot instead
            pass
    else:
        plot = series.plot(kind='hist', figsize=figsize,
                           facecolor=facecolor,
                           bins=bins)  # TODO when running on server, send this off to a different thread
    return plot


def histogram(series, **kwargs):
    """Plot an histogram of the data.

    Parameters
    ----------
    series: Series, default None
        The data to plot.

    Returns
    -------
    str, The resulting image encoded as a string.
    """
    imgdata = BytesIO()
    plot = _plot_histogram(series, **kwargs)
    plot.figure.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0, hspace=0)
    plot.figure.savefig(imgdata)
    imgdata.seek(0)
    result_string = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    # TODO Think about writing this to disk instead of caching them in strings
    plt.close(plot.figure)
    return result_string


def mini_histogram(series, **kwargs):
    """Plot a small (mini) histogram of the data.

    Parameters
    ----------
    series: Series, default None
        The data to plot.

    Returns
    -------
    str, The resulting image encoded as a string.
    """
    imgdata = BytesIO()
    plot = _plot_histogram(series, figsize=(2, 0.75), **kwargs)
    plot.axes.get_yaxis().set_visible(False)

    if LooseVersion(matplotlib.__version__) <= '1.5.9':
        plot.set_axis_bgcolor("w")
    else:
        plot.set_facecolor("w")

    xticks = plot.xaxis.get_major_ticks()
    for tick in xticks[1:-1]:
        tick.set_visible(False)
        tick.label.set_visible(False)
    for tick in (xticks[0], xticks[-1]):
        tick.label.set_fontsize(8)
    plot.figure.subplots_adjust(left=0.15, right=0.85, top=1, bottom=0.35, wspace=0, hspace=0)
    plot.figure.savefig(imgdata)
    imgdata.seek(0)
    result_string = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    plt.close(plot.figure)
    return result_string

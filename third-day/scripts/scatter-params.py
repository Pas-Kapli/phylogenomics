#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

def read_data(filename1, filename2):
    data1 = pd.read_table(filename1, delim_whitespace=True)
    data2 = pd.read_table(filename2, delim_whitespace=True)
    return data1, data2

def plot_data(ax, data1, data2, param_prefix, title, label1, label2):
    import numpy as np

    # get all columns that start with the parameter prefix
    cols = list(filter(lambda x: x.startswith(param_prefix), data1.columns.values))
    if len(cols) == 0:
        ax.set_visible(False)
        return

    # compute means and 95% intervals
    means1 = data1[cols].mean()
    means2 = data2[cols].mean()
    lower1 = data1[cols].quantile(0.025)
    upper1 = data1[cols].quantile(0.975)
    lower2 = data2[cols].quantile(0.025)
    upper2 = data2[cols].quantile(0.975)

    # determine plot bounds and cap width
    maxval = max(means1.max(), means2.max(), upper1.max(), upper2.max()) * 1.01
    cap_width = 0.01 * maxval

    # scatter plot

    for col in cols:
        x = means1[col]
        y = means2[col]

        # horizontal (x) uncertainty
        ax.plot([lower1[col], upper1[col]], [y, y], color="gray", lw=1, alpha=0.5)
        ax.plot([lower1[col], lower1[col]], [y - cap_width/2, y + cap_width/2], color="gray", lw=1, alpha=0.5)
        ax.plot([upper1[col], upper1[col]], [y - cap_width/2, y + cap_width/2], color="gray", lw=1, alpha=0.5)

        # vertical (y) uncertainty
        ax.plot([x, x], [lower2[col], upper2[col]], color="gray", lw=1, alpha=0.5)
        ax.plot([x - cap_width/2, x + cap_width/2], [lower2[col], lower2[col]], color="gray", lw=1, alpha=0.5)
        ax.plot([x - cap_width/2, x + cap_width/2], [upper2[col], upper2[col]], color="gray", lw=1, alpha=0.5)

    # axis settings
    ax.set_xlim(0, maxval)
    ax.set_ylim(0, maxval)
    ax.plot([0, maxval], [0, maxval], color="black", linestyle="dashed")
    ax.scatter(means1, means2, color="blue")
    ax.set_title(title,fontsize=18)
    ax.set_xlabel(label1)
    ax.set_ylabel(label2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " mcmcfile1 mcmcfile2")
        sys.exit(0)

    plt.rcParams.update({
      "text.usetex": True,
      "font.family": "Helvetica"
    })

    # read MCMC data
    data1, data2 = read_data(sys.argv[1], sys.argv[2])

    # create a 2x2 plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    plot_data(axes[0], data1, data2, "tau", r"$\tau$", sys.argv[1], sys.argv[2])
    plot_data(axes[1], data1, data2, "theta", r"$\theta$", sys.argv[1], sys.argv[2])
    fig.suptitle(r'Posterior means and 95\% CI for parameters $\tau$ and $\theta$')

    # Hide the unused subplot
    #axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig("posterior.pdf", format='pdf')
    plt.close("all")


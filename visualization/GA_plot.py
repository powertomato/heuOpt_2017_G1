from matplotlib import pyplot as plt
import numpy as np
import matplotlib
from solvers.evolution.Chromosome import *

class GAPlot():
    def __init__(self):
        self.cost_y_axis = []
        self.gen_x_axis = []
        self.type_color = []

    def add_specimens(self, generation, time, specimens):
        for specimen in specimens:
            self.gen_x_axis.append(generation)
            self.cost_y_axis.append(specimen.numCrossings())
            col = "c"
            if specimen.chType == ChType.ELITE:
                col = "r"
            elif specimen.chType == ChType.RECOMBINED:
                col = "g"
            elif specimen.chType == ChType.MUTATED:
                col = "b"
            elif specimen.chType == ChType.IMMIGRATED:
                col = "k"

            self.type_color.append(col)

    def plot(self):
        plt.scatter(self.gen_x_axis, self.cost_y_axis, s=1, c=self.type_color, marker="o")
        plt.ylim(ymin=0)
        plt.show()

if __name__ == "__main__":
    # Fixing random state for reproducibility
    np.random.seed(19680801)


    x = np.arange(0.0, 50.0, 2.0)
    y = x ** 1.3 + np.random.rand(*x.shape) * 30.0
    s = np.random.rand(*x.shape) * 80

    plt.scatter(x, y, s, c="g", alpha=0.5, marker='o',
                label="Luck")
    plt.xlabel("Leprechauns")
    plt.ylabel("Gold")
    plt.ylim(ymin=0)
    plt.legend(loc=2)
    plt.show()
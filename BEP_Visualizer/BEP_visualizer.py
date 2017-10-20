import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
import numpy as np
import colorsys

import csv
import os
from graph import Graph

class View():
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x800+30+30")

        self.canvas = Canvas(self.root)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.canvas.grid(row=1, column=1, sticky=N + S + E + W)
        self.canvas.focus_set()
        self.spine = None

    def draw(self, graph):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        nnodes = len(graph.nodes)
        line_height = height * 0.9
        top_inset = (height - line_height) / 2
        left_inset = width * 0.5
        p1 = (left_inset, top_inset)
        p2 = (left_inset, top_inset + line_height)

        self.canvas.create_oval(left_inset, top_inset, left_inset, top_inset+line_height)

        node_positions = np.arange(top_inset, top_inset+line_height, line_height/(nnodes-1))
        node_positions = np.append(node_positions, top_inset + line_height)

        for pos in node_positions:
            self.canvas.create_oval(left_inset-5, pos-5, left_inset+5, pos+5)

        # draw edges
        for edge in graph.edges:
            n1 = edge[0]
            n2 = edge[1]
            p = edge[2]

            pagecolor = colorsys.hsv_to_rgb(359 / graph.pages * p, 1, 1)
            pagecolor = tuple(int(x * 255) for x in pagecolor)
            tk_rgb = "#%02x%02x%02x" % pagecolor

            in1 = graph.nodes.index(n1)
            in2 = graph.nodes.index(n2)

            pos1 = node_positions[in1]
            pos2 = node_positions[in2]

            width = abs(in2 - in1) * line_height/(nnodes-1)
            width /= 2

            start = 270
            if p%2 is 1:
                start = 90

            self.canvas.create_arc(left_inset-width, pos1, left_inset+width, pos2, style=tk.ARC, start=start, extent = 180, outline=tk_rgb)

def load_and_draw( event):
    graph = Graph()
    graph.read('../instances/automatic-3.txt')

    view.draw(graph)

root = Tk()
view = View(root)

view.canvas.bind("<Button-1>", load_and_draw)

root.title="BEP Visualizer"
root.deiconify()
root.mainloop()
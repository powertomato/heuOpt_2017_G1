import csv
import os

class Graph():
    def __init__(self):
        self.nodes = list()
        self.edges = list()
        self.pages = 1

    def read(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            next(reader)
            next(reader)
            next(reader)
            self.pages = int(next(reader)[0])
            for row in reader:
                if row[0][0] is '#':
                    continue
                elif len(row) is 1:
                    self.nodes.append(int(row[0]))
                else:
                    n1 = int(row[0])
                    n2 = int(row[1])

                    p = int(row[2][1:-1])
                    self.pages = max(self.pages, p)
                    self.edges.append((n1, n2, p))


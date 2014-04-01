# This is used to draw the vector map of GHC7 using GHC7_vector.txt
# Author: Kai Kang

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5,4))
ax  = fig.add_subplot(1,1,1)

def getVectors(filename="GHC7_vector.txt"):
    start_points = []
    end_points   = []
    with open(filename, 'r') as f:
        for line in f:
            data  = map(float, line.split(","))
            start = (data[0], data[1])
            end   = (data[2], data[3])
            start_points.append(start)
            end_points.append(end)
    return (start_points, end_points)

def drawVectors(start_points, end_points):
    for i in xrange(len(start_points)):
        x_data = [start_points[i][0], end_points[i][0]]
        y_data = [start_points[i][1], end_points[i][1]]
        ax.plot(x_data, y_data, color="blue", linewidth="1")

if __name__ == "__main__":
    start_points, end_points = getVectors()
    drawVectors(start_points, end_points)
    plt.show()

import matplotlib.pyplot as plt
import random


def notAllInf(l):
    """ Returns true if there is at least one non-inf entry """
    for error in l:
        if error[1] != float('inf'):
            return True
    return False



def stripInf(l):
    """ Strip all the inf entries and process all the non-inf entries"""
    result = dict()
    for error in l:
        if error[1] != float('inf'):
            area = tuple(map(float, error[0].split('!')))
            result[ area ] = error[1]
    return result



def plotSingle(x, y, fig, ax, color):
    """
    Plot single bssid object
    """
    x_data, y_data = [x], [y]
    ax.scatter(x_data, y_data, color=color, marker="o",  alpha=1)



def getVectors(filename="GHC7_vector.txt"):
    """
        Get vector data from GHC7_vector.txt
    """
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



def drawVectors(start_points, end_points, ax):
    for i in xrange(len(start_points)):
        x_data = [start_points[i][0], end_points[i][0]]
        y_data = [start_points[i][1], end_points[i][1]]
        ax.plot(x_data, y_data, color="blue", linewidth="1")



def plotBssids(listOfBssids, debug=True):
    """ Plot multiple bssids """
    fig = plt.figure(figsize=(5,4))
    ax  = fig.add_subplot(1,1,1)
    ax.set_title("GHC7 - estimated locations based on Wifi strength")
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'w']
    i = 0
    start_points, end_points = getVectors()
    drawVectors(start_points, end_points, ax)  # Draw GHC7 map
    listOfEntries = []
    for bssid in listOfBssids:
        for area in bssid.data:
            listOfEntries.append(  (area, bssid.data[area])   )
    print "-------------quarter-----------"
    try:
        location = quarter(listOfEntries)
        if debug:
            plotSingle(location[0], location[1], fig, ax, "RED")
            plt.ylim((-60,60))
            plt.xlim((-30,30))
            plt.show()
        else:
            pass
        return location
    except Exception as e:
        print str(e)
    return "10,10"

def calcWeight(dif):
    T = 5
    if dif >= T:
        return 0
    else:
        return (T-dif)**3

def quarter(listOfEntries, x_limit_low=-30,
            x_limit_high=30, y_limit_low=-60, y_limit_high=60):
    """
    listOfEntries is of form: [((x,y), dif),... ]
    """
    data = [0,0,0,0] # top_left, top_right, bottom_left, bottom_right
    entries = [[],[],[],[]]
    mid_x, mid_y = (x_limit_low+x_limit_high)/2.0, (y_limit_low+y_limit_high)/2.0
    if (y_limit_high - y_limit_low) <= 1:
        # Accurate enough
        print "AAAAAAAAAAAAA"
        print (mid_x, mid_y)
        return (mid_x, mid_y)
    for area in listOfEntries:
        x, y, dif = area[0][0], area[0][1], area[1]
        if ((x_limit_low <= x <= mid_x) and (mid_y<=y<=y_limit_high)):
            # top left
            index = 0
        elif ((mid_x<=x<=x_limit_high)and(mid_y<=y<=y_limit_high)):
            # top right
            index = 1
        elif ((x_limit_low<=x<=mid_x)and(y_limit_low<=y<=mid_y)):
            # bottom left
            index = 2
        else:
            # bottom right
            index = 3
        data[index] += calcWeight(dif)
        entries[index].append(((x,y), dif))
    max_index = data.index(max(data))
    if max_index == 0:
        # top left
        x_new_low, x_new_high = x_limit_low, mid_x
        y_new_low, y_new_high = mid_y, y_limit_high
    elif max_index == 1:
        # top right
        x_new_low, x_new_high = mid_x, x_limit_high
        y_new_low, y_new_high = mid_y, y_limit_high
    elif max_index == 2:
        # bottom left
        x_new_low, x_new_high = x_limit_low, mid_x
        y_new_low, y_new_high = y_limit_low, mid_y
    else:
        # bottom right
        x_new_low, x_new_high = mid_x, x_limit_high
        y_new_low, y_new_high = y_limit_low, mid_y
    return quarter(entries[max_index], x_new_low, x_new_high, y_new_low, y_new_high)




class Bssid(object):


    def __init__(self, tup):
        self.name = tup[0]
        self.data = tup[1] # a dictionary
        self.bssids = tup[1].keys()

    def __str__(self):
        return "I am a Bssid Object with %d data" %(len(self.data))

    def getData(self):
        return self.data

    def getWeightedAverage(self):
        """ abandoned """
        average_x, average_y = 0, 0
        total = 0
        max_str_dif = max(self.data.values())
        for area in self.data:
            weight = abs(max_str_dif - self.data[area])
            average_x += area[0] * weight
            average_y += area[1] * weight
            total += weight
        average_x /= total
        average_y /= total
        return (average_x, average_y)

if __name__ == "__main__":
    plotBssids([])

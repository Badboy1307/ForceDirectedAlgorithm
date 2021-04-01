import os
import numpy as np
import matplotlib.pyplot as plt


def importTest():
    print("import test successed.")


def getParameters():
    kr = 5
    ks = 10
    L = 5

    return kr, ks, L


def updateRepulsion(nodes, kr=10):
    # kr = 10

    res = np.zeros((nodes.shape[0], 2))
    for i in range(nodes.shape[0]):
        for j in range(i + 1, nodes.shape[0]):
            dist = np.power(np.power(nodes[i][0] - nodes[j][0], 2) + 
                            np.power(nodes[i][1] - nodes[j][1], 2), 0.5)
            dtor = np.power(max(1, dist), 3)

            fx = kr * (nodes[i][0] - nodes[j][0]) / dtor
            res[i][0] += fx
            res[j][0] -= fx

            fy = kr * (nodes[i][1] - nodes[j][1]) / dtor
            res[i][1] += fy
            res[j][1] -= fy

    return res


def updateSpring(nodes, edges, ks=1, L=10):
    # ks = 1
    # L = 10

    res = np.zeros((nodes.shape[0], 2))
    for i in range(edges.shape[0]):
        for j in range(edges.shape[0]):
            if (i > j or edges[i][j] == 0):
                continue

            dist = np.power(np.power(nodes[i][0] - nodes[j][0], 2) + 
                            np.power(nodes[i][1] - nodes[j][1], 2), 0.5)
            fs = ks * (dist - L)

            fx = fs * (nodes[j][0] - nodes[i][0]) / max(dist, 1)
            res[i][0] += fx
            res[j][0] -= fx

            fy = fs * (nodes[j][1] - nodes[i][1]) / max(dist, 1)
            res[i][1] += fy
            res[j][1] -= fy
    
    return res

def updateLocation(nodes, edges, stride):
    kr, ks, L = getParameters()

    Fr = updateRepulsion(nodes, kr)
    Fs = updateSpring(nodes, edges, ks, L)
    Force = Fr + Fs
    
    displace = stride * Force
    newLoc = nodes + displace

    os.system('cls')
    print(Force)
    
    return newLoc


def prepareData(dim):
    nodes = np.random.randn(dim, 2)

    edges = np.random.randn(dim, dim)
    for i in range(dim):
        for j in range(dim):
            if (i <= j or edges[i][j] < 1.5):
                edges[i][j] = 0
            else:
                edges[i][j] = 1

    return nodes, edges


def drawData(nodes, edges, time=0.5):
    plt.cla()
    for i in range(nodes.shape[0]):
        plt.scatter(nodes[i][0], nodes[i][1])
        plt.annotate(str(i), (nodes[i][0], nodes[i][1] + 0.1))
        for j in range(edges.shape[0]):
            if (edges[i][j] == 0):
                continue
            x_list = [nodes[i][0], nodes[j][0]]
            y_list = [nodes[i][1], nodes[j][1]]
            plt.plot(x_list, y_list)

    if (time > 0):
        plt.pause(time)
    # plt.show()


def starTopo(edges):
    edges = np.zeros((edges.shape))
    for j in range(1, edges.shape[0]):
        edges[0][j] = 1
        edges[j][0] = 1
    return edges


def loopTopo(edges):
    edges = np.zeros((edges.shape))
    for i in range(edges.shape[0]):
        j = (i + 1) % edges.shape[0]
        edges[i][j] = 1
        edges[j][i] = 1
    return edges
import numpy as np
from force import *

nodes, edges = prepareData(15)
edges = starTopo(edges)

drawData(nodes, edges)
plt.pause(0.5)

for i in range(1000):
    nodes = updateLocation(nodes, edges, 0.003)
    drawData(nodes, edges, 0.3)
    print("iteration: " + str(i))

    if (np.mean(np.abs(nodes)) > 150):
        break

print("completed.")
plt.show()
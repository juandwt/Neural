import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator

def LJ():

    def lennard_jones(r, epsilon, sigma):
        return 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)
    
    epsilon = 1.0
    sigma = 1.0
    
    r = np.linspace(0.95, 3.0, 400)
    
    R, Theta = np.meshgrid(r, np.linspace(0, 2 * np.pi, 100))
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)
    Z = lennard_jones(R, epsilon, sigma)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_wireframe(X, Y, Z, color="black", alpha=0.4)
    #ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.contour(X, Y, Z, zdir='y', levels=1,  offset=ax.get_ylim()[0], colors="black", alpha=0.7)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('V(X, Y)')
    
    ax.set_title('$V(x, y) = 4 \\epsilon \\left[ \\left( \\frac{\\sigma}{\\sqrt{x^2 + y^2}} \\right)^{12} - \\left( \\frac{\\sigma}{\\sqrt{x^2 + y^2}} \\right)^{6} \\right]$')
    ax.view_init(elev=10, azim=135)
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(4))
    ax.zaxis.set_major_locator(MultipleLocator(4))
    
    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
 

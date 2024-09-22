import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator

def yukawa():
    def yukawa_potential(r, g, mu):
        return -g**2 * np.exp(-mu * r) / r
    
    g = 1.0
    mu = 1.0
    
    r = np.linspace(0.5, 5.0, 400)
    
    R, Theta = np.meshgrid(r, np.linspace(0, 2 * np.pi, 100))
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)
    Z = yukawa_potential(R, g, mu)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_wireframe(X, Y, Z, color='black', alpha=0.5)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('V(x, y)')
    
    ax.set_title('$V(x, y) = -g^2 \\frac{e^{-\\mu \\sqrt{x^2 + y^2}}}{\\sqrt{x^2 + y^2}}$')
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
 

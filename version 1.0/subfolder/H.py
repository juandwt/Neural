import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
import numpy as np

def H():
    
    e = 1.602e-19  # carga del electrón en Coulombs
    epsilon_0 = 8.854e-12  # permitividad del vacío en Faradios por metro
    
    def potential(x, y, z):
        r = np.sqrt(x**2 + y**2 + z**2)
        return -e**2 / (4 * np.pi * epsilon_0 * r)
    
    x = np.linspace(-1, 1, 50)
    y = np.linspace(-1, 1, 50)
    X, Y = np.meshgrid(x, y)
    
    z_val = 0
    Z = np.full_like(X, z_val)
    
    V = potential(X, Y, Z)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_wireframe(X, Y, V, color="black", alpha=0.5)
    ax.contour(X, Y, V, zdir='z',levels=30,  offset=ax.get_zlim()[0], colors="black", alpha=0.7)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('$V(x, y)$')
    ax.set_title(r"$V(x, y) = -\frac{e^2}{4 \pi \epsilon_0 \sqrt{x^2 + y^2}}$")
    
    ax.view_init(elev=25, azim=135)
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
 

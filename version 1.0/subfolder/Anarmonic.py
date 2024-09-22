import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
import numpy as np

def Anarmonic():   
    x = np.linspace(-1.79, 1.79, 50)
    y = np.linspace(-1.79, 1.79, 50)
    x, y = np.meshgrid(x, y)
    
    m, w, l = 1, 1, 1
    
    v = (1/2)*m*w*(x**2+y**2) + l*(x**4+y**4)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_wireframe(x, y, v, color="black", alpha=0.5)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('V(x)')
    ax.set_title(r"$V(x, y) = \frac{1}{2}m\omega (x^{2}+y^{2}) + \lambda (x^{4}+y^{4})$")
    
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
 

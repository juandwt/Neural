import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
import numpy as np

def Box():
  
    points = np.array([
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
        [1, 1, 1],
        [-1, 1, 1]
    ])
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Crear una malla de puntos
    r = [-1, 1]
    X, Y = np.meshgrid(r, r)
    
    # Definir Z como una matriz con valores constantes
    Z1 = np.ones_like(X)
    Z2 = -np.ones_like(X)
    
    # Dibujar los wireframes de las paredes
    ax.plot_surface(X, Y, Z1,color='black', alpha=0.2)
    ax.plot_surface(X, Y, Z2,color='black', alpha=0.2)
    ax.plot_surface(X, -1*Y, Z1, color='black', alpha=0.2)
    ax.plot_surface(X, -1*Y, Z2, color='black', alpha=0.2)
    ax.plot_surface(Z1, X, Y, color='black',alpha=0.2)
    ax.plot_surface(Z2, X, Y, color='black', alpha=0.2)
    
    # Graficar los puntos
    ax.scatter3D(points[:, 0], points[:, 1], points[:, 2], color="black", marker=".")
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_title('V(x, y, z) = 0 si 0 ≤ x ≤ L_x, 0 ≤ y ≤ L_y, 0 ≤ z ≤ L_z; ∞ en otro caso')
    ax.set_xlim(-0.96, 0.96)
    ax.set_ylim(-0.96, 0.96)
    ax.set_zlim(-0.96, 0.96)
    
    
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
 


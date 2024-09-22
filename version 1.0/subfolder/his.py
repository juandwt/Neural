import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator

plt.rcParams['toolbar'] = 'none'

def hist(E):
    
    colores = {"dark_green":"#4a6c65", "olive":"#7B904B", "black":"#000000",
          "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9", "blue":"#85fff8"}
    
    a = float(E)
    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)
    x, y = np.meshgrid(x, y)
    
    z = 1 / (a * (x**2 + y**2) + 1)**2
    V = 0.5*x**2 + 0.5*y**2
    Z = z**2
    
    probabilidades = Z.flatten() / Z.sum()  # Normalizar los valores de Z para que sumen 1
    indices = np.random.choice(np.arange(Z.size), size=500, replace=False, p=probabilidades)
    x_selected = x.flatten()[indices]
    y_selected = y.flatten()[indices]
    z_selected = Z.flatten()[indices]
    
    xbins = np.linspace(x_selected.min(), x_selected.max(), 30)
    ybins = np.linspace(y_selected.min(), y_selected.max(), 30)
    histvals, xedges, yedges = np.histogram2d(x_selected, y_selected, bins=[xbins, ybins])
    
    xcenter = np.convolve(xbins, np.ones(2), "valid") / 2
    ycenter = np.convolve(ybins, np.ones(2), "valid") / 2
    xpos, ypos = np.meshgrid(xcenter, ycenter)
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    dz = histvals.flatten() * 0.03
    
    my_cmap = plt.cm.inferno
    
    colors = my_cmap(z_selected / z_selected.max())
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(x_selected, y_selected, z_selected, c=colors, s=12, edgecolor="black", label=r'$|\Psi(r)|^{2}$')
    ax.plot_wireframe(x, y, V, color="black", alpha=0.3)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel(r'$INFO$')
    ax.set_title(r"$|\Psi(r)|^{2} \wedge  V(r)$", color=colores["dark_green"], fontsize=12)

    ax.view_init(elev=20, azim=135)
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.zaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4       

 

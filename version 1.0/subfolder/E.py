import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.ticker import MultipleLocator

def E():
        
    color = {"black":"#000000", "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9"}
    plt.rcParams['toolbar']     = 'none'
    
    def f(x, y):
        return np.sin(x) + np.cos(y)
        #return x**2 + y**2 + 10
    
    x    = np.linspace(-np.pi, 2*np.pi, 25)
    y    = np.linspace(-np.pi, 2*np.pi, 25)
    x, y = np.meshgrid(x, y)
    z    = f(x, y)
    
    def gradiente(x, y):
        df_dx =  np.cos(x) #2*x
        df_dy = -np.sin(y) #2*y
        return df_dx, df_dy
    
    #Desenso por gradiente 
    
    theta_x = 0.1 
    theta_y = 0.1
    lr = 0.8
    iters = 7
    
    # Listas para almacenar los últimos valores de las iteraciones
    last_thetas_x = []
    last_thetas_y = []
    
    for i in range(iters):
        df_dx, df_dy = gradiente(theta_x, theta_y)
        theta_x -= lr * df_dx 
        theta_y -= lr * df_dy
        if i >= iters - 13:  # Guardar los valores de las últimas 5 iteraciones
            last_thetas_x.append(theta_x)
            last_thetas_y.append(theta_y)
    
    
    fig = plt.figure(figsize=(10, 6))
    ax  = fig.add_subplot(111, projection="3d")
    
    
    colores = [(0.39, 0.02,  0.02) for i in np.linspace(0.1, 1, len(last_thetas_x))]    
    
    for i in range(iters):
        ax.scatter(last_thetas_x[i], last_thetas_y[i], f(last_thetas_x[i], last_thetas_y[i]), color=colores[i])
        #ax.scatter(last_thetas_x[i], last_thetas_y[i], f(last_thetas_x[i], last_thetas_y[i]))
        ax.scatter(theta_x, theta_y, f(theta_x, theta_y), color=color["purple"])
    
    
    
    #ax.plot_surface(x, y, z, cmap="Greens")
    ax.plot_wireframe(x, y, z, color=color["black"], linewidth=0.5, alpha=0.6)
    #ax.scatter(0, 0, 10, color=color["purple"])
    #ax.contourf(x, y, z, xdir="x", offset=ax.get_xlim()[0], cmap="bone")
    
    #XY
    #ax.contour(x, y, z, zdir='z', offset=ax.get_zlim()[0], colors=color["black"], alpha=0.7)
    #ZY
    #ax.contour(x, y, z, zdir='x', offset=ax.get_xlim()[0], colors=color["black"], alpha=0.7)
    
    # Añadir las líneas de nivel en el plano XZ
    #ax.contour(x, y, z, zdir='y', offset=ax.get_ylim()[0], colors=color["black"], alpha=0.7, lw=0.8)
    
    
    #YlGn
    
    ax.set_xlabel(r'$\alpha$')
    ax.set_ylabel(r'$\beta$')
    ax.set_zlabel(r'$E(\alpha, \beta)$')
    #ax.set_title(r'$E(\alpha, \beta) \longrightarrow E_{min}(\alpha, \beta)$', color=color["purple"]
    #            , fontsize=15)

    ax.set_title(r'$E = 0.25 \alpha m w^{2} + 0.5 \beta^{2} m w^{2} + \frac{h^{2}}{4 \alpha m}$')
    #ax.set_title('Gráfica de una Recta y una Esfera en 3D')
    
    #ax.text(x.min()*1.1, y.min()*1.1, z.max()*1.1, r'$Q(x_p,y_p)$')
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


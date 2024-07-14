import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.ticker import MultipleLocator


color = {"black":"#000000", "green":"#488c2e", "purple":"#6a0606", "gray":"#b9b9b9"}
# Configuración de estilo
#plt.rcParams['font.size']   = 15
#plt.rcParams['font.family'] = 'serif'
plt.rcParams['toolbar']     = 'none'


def f(x, y):
    return x**2 + y**2 + 10

x    = np.linspace(-5, 5, 50)
y    = np.linspace(-5, 5, 50)
x, y = np.meshgrid(x, y)
z    = f(x, y)

def gradiente(x, y):
    df_dx = 2*x
    df_dy = 2*y
    return df_dx, df_dy

#Desenso por gradiente 

theta_x = 15 
theta_y =-15
lr    = 0.1 
iter  = 10

for i in range(iter):
    df_dx, df_dy = gradiente(theta_x, theta_y)
    theta_x -= lr*df_dx 
    theta_y -= lr*df_dy

print(theta_x, theta_y, f(theta_x, theta_y))

fig = plt.figure(figsize=(10, 8))

ax  = fig.add_subplot(111, projection="3d")
#ax.plot_surface(x, y, z, cmap="Greens")
ax.plot_wireframe(x, y, z, color=color["gray"], linewidth=0.5, alpha=0.5)
ax.scatter(0, 0, 10, color=color["purple"])
ax.scatter(theta_x, theta_y, f(theta_x, theta_y), color=color["purple"])
#YlGn

ax.set_xlabel(r'$x_p$')
ax.set_ylabel(r'$y_p$')
ax.set_zlabel(r'$z_p$')
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

#plt.legend()
plt.savefig("graph.jpg")
plt.show()

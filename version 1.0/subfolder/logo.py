import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def logo():
    ruta_imagen = "logo.jpg"
    plt.rcParams['toolbar'] = 'none'
    
    imagen = mpimg.imread(ruta_imagen)
    plt.axis("off")
    plt.imshow(imagen)


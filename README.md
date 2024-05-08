# PINN
How's PINN work to solve DEO?

Imagine that you have the next DEO: 

$$\frac{dy}{dt}=-ky$$ 

with the intial condition $y(0)=1$

$$L = L_{DE} + L_{IC}$$

# Step 1, Define the Loss function 

$$L=\frac{1}{N}\sum_{i=1}^{N}{\frac{dy_{pred}}{dt}+ky_{pred}(t_{i})}+L_{IC}$$

# PINN
How's PINN work to solve DEO?

Imagine that you have the next DEO: 

$$\frac{dy}{dt}=-ky$$ 

with the intial condition $y(0)=1$

$$L = L_{DE} + L_{IC}$$

# Step 1, Define the Loss function 

$$L=\frac{1}{N}\sum_{i=1}^{N}{[\frac{dy_{pred}}{dt} \left. \right|_{i} +ky_{pred}(t_{i})}]^{2}+[y_{pred}(0)-1]^{2}$$

```python
import torch
import torch.nn as nn
import numpy as np

# Constant for the model
# dy/dt + ky = 0
# y(0)=1
k = 1


class NeuralNet(nn.Module):
    def __init__(self, hidden_size, output_size=1,input_size=1):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.relu1 = nn.Tanh()
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.relu2 = nn.Tanh()
        self.l3 = nn.Linear(hidden_size, hidden_size)
        self.relu3 = nn.Tanh()
        self.l4 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.l1(x)
        out = self.relu1(out)
        out = self.l2(out)
        out = self.relu2(out)
        out = self.l3(out)
        out = self.relu3(out)
        out = self.l4(out)
        return out


# t_time >> Ly1 (LF) >> Ly2 (LF) ... y_pred


#Error cuadratico medio definir clase
criterion = nn.MSELoss()

# Calculo cuadratico medio de los valores de y, y el valore objetivo
def initial_condition_loss(y, target_value):
    return nn.MSELoss()(y, target_value)

# Datos de prueba
t_numpy = np.arange(0, 5+0.01, 0.001, dtype=np.float32)
t = torch.from_numpy(t_numpy).reshape(len(t_numpy), 1)
t.requires_grad_(True)


# Crear una instancia en NeuralNet
# t >> 10 >> 10 >> 10 >> 10 >> y_pred
model = NeuralNet(hidden_size=10)

# Función de perdida y optimizador
learning_rate = 1.3e-1
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# Número de entrenamientos
num_epochs = 300

# Bucle de predicción o entrenamiento
for epoch in range(num_epochs):

    # perturvar los valores de tiempo
    epsilon = torch.normal(0,.1, size=(len(t),1)).float()
    t_train = t + epsilon

    # Forward pass
    y_pred = model(t_train)

    # Calculo de la primera de rivada de y_pred con respecto a t_train
    dy_dt = torch.autograd.grad(y_pred,
                                t_train,
                                grad_outputs=torch.ones_like(y_pred),
                                create_graph=True)[0]

    # L_DE
    loss_DE = criterion(dy_dt + k*y_pred, torch.zeros_like(dy_dt))

    # L_CI
    loss_IC = initial_condition_loss(model(torch.tensor([[0.0]])),
                                     torch.tensor([[1.0]]))

    loss = loss_DE + loss_IC

    optimizer.zero_grad() #Limpiar gradientes
    loss.backward() # Calcular el gradiente 
    optimizer.step() # Optimizar 

import matplotlib.pyplot as plt

#No realizar el algoritmo de retropropagación en el bucle

with torch.no_grad():
    y_solution = model(t)

# Solución analitica (AS)
# Solución (NNS)

plt.figure(figsize=(8, 6))
plt.plot(t.detach().numpy(), y_solution.detach().numpy(), label='NNS', color='black')
plt.plot(t.detach().numpy(), np.exp(-t.detach().numpy()) , label='AS', color='gray', ls='--')

plt.axhline(0, color='gray', linestyle='-', linewidth=1)  # Línea horizontal en y=0
plt.axvline(0, color='gray', linestyle='-', linewidth=1)  # Línea vertical en x=0

plt.xlabel('t')
plt.ylabel('y')
plt.legend()

#plt.savefig("grafica.png", format='png', dpi=100, bbox_inches='tight')
#plt.savefig("grafica.png", format='png', dpi=300)
plt.show()
```

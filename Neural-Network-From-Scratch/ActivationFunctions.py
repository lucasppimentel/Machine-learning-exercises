import numpy as np

x = 1

step_f = 1 if x>=0 else 0
sigmoid = 1/(1+np.exp(-x))

inputs = [0, 2, -1, 3.3, -2.7, 1.1, 2.2, -100]
# ----------------------- ReLU -----------------------
ReLU = 0 if x<=0 else x

# or
ReLU = list()
for i in inputs:
    if i > 0:
        ReLU.append(i)
    elif i <= 0:
        ReLU.append(0)
        
# or
ReLU = list()
for i in inputs:
    ReLU.append(max(0, i))
# ----------------------------------------------------


layer_outputs = [4.8, 1.21, 2.385]
# --------------------- Softmax ----------------------
# Overflow prevention
layer_outputs = layer_outputs - max(layer_outputs)

exp_values = np.exp(layer_outputs)
norm_values = exp_values / np.sum(exp_values)

# ----------------------------------------------------

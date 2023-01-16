import numpy as np

softmax_outputs = np.array([[0.7, 0.1, 0.2],
                            [0.1, 0.5, 0.4],
                            [0.02, 0.9, 0.08]])

class_targets = [0, 1, 1]

# Não podemos lidar com probabilidade igual a 0
softmax_outputs = np.clip(softmax_outputs, 1e-7, 1-1e-7)


# Pega os valores da predição dados para as classes corretas
neg_log = -np.log(softmax_outputs[[range(len(softmax_outputs))], 
                                  [class_targets]])
avg_loss = np.mean(neg_log)
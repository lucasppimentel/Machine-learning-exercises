# Learning the XOR table with machine learning
# This model is an adaptation of one model of https://github.com/fernandofeltrin
import numpy as np

entradas = np.array([[0,0], [0,1], [1,0], [1,1]]) # Values to be fed, each line
# corresponds to one possible combination of two binary values 

saidas = np.array([[0],[1],[1],[0]]) # Expected values in final layer

# Creates new arrays for weights, using numbers in between 1 and 0, and the
# required shape (note that the hiden layer has 3 neurons)
pesos0 = np.random.uniform(0, 1, (2, 3))
pesos1 = np.random.uniform(0, 1, (3, 1))

ntreinos = 50000
taxaAprendizado = 0.3
momentum = 1 

# Defining activation function
def sigmoid(soma):
    return 1/(1 + np.exp(-soma))

# Derivative of activation function (not sure why the "open" derivative formula
# doesn't work)
def sigmoideDerivada(sig):
    return sig * (1-sig)


for i in range(ntreinos):
    camadaEntrada = entradas
    somaSinapse0 = np.dot(camadaEntrada, pesos0)
    camadaOculta = sigmoid(somaSinapse0)
    
    somaSinapse1 = np.dot(camadaOculta, pesos1)
    camadaSaida = sigmoid(somaSinapse1) # End layer
    
    # Start of feedback operations
    erroCamadaSaida = saidas - camadaSaida
    mediaAbsoluta = np.mean(np.abs(erroCamadaSaida))
    
    derivadaSaida = sigmoideDerivada(camadaSaida) # Derivada da camada saida
    deltaSaida = erroCamadaSaida * derivadaSaida # Aproximação
    
    pesos1Transposta = pesos1.T
    deltaSaidaXpesos = deltaSaida.dot(pesos1Transposta)
    deltaCamadaOculta = deltaSaidaXpesos * sigmoideDerivada(camadaOculta)
    
    camadaOcultaTransposta = camadaOculta.T
    pesos3 = camadaOcultaTransposta.dot(deltaSaida)
    pesos1 = (pesos1 * momentum) + (pesos3 * taxaAprendizado)
    
    camadaEntradaTransposta = camadaEntrada.T
    pesos4 = camadaEntradaTransposta.dot(deltaCamadaOculta)
    pesos0 = (pesos0 * momentum) + (pesos4 * taxaAprendizado)
    
    print('Margem de erro: ' + str(mediaAbsoluta))

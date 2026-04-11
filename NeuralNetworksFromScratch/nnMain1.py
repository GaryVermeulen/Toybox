# nnClasses1.py
#
# Main script for "Neural Networks from Scratch"
#import numpy as np
import nnfs
from nnfs.datasets import spiral_data
import matplotlib.pyplot as plt

from nnClasses1 import Layer_Dense
from nnClasses1 import Activation_ReLU
from nnClasses1 import Activation_Softmax
from nnClasses1 import Loss_CategoricalCrossentropy

nnfs.init()


    
        
    
if __name__ == "__main__":

    # Crteate dataset
    X, y = spiral_data(samples=100, classes=3)

    # Create Dense layer with 2 input features and 3 output values
    dense1 = Layer_Dense(2, 3)

    # Create ReLU activation (to be used with dense layer)
    activation1 = Activation_ReLU()

    # Create second Dense layer with 3 input features (as we take output
    # of the previous layer here) and 3 output values
    dense2 = Layer_Dense(3, 3)

    # Create Softmax activation (to be used with Dense lyer)
    activation2 = Activation_Softmax()

    # Create loss function
    loss_function = Loss_CategoricalCrossentropy()

    # Make a forward pass of our training data through this layer
    dense1.forward(X)

    # Make a forward pass through activation function
    # it takes the output of the first dense layer here
    activation1.forward(dense1.output)

    # Make a forward pass through the second dense layer
    # it take outputs of the activation function of first layer as inputs
    dense2.forward(activation1.output)

    # Make a forward pass through activation function
    # it takes the output of the second dense layer here
    activation2.forward(dense2.output)

    # Output
    print(activation2.output[:5])

    loss = loss_function.calculate(activation2.output, y)

    print('loss: ', loss)
      

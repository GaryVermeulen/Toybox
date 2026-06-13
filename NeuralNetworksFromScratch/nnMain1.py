# nnClasses1.py
#
# Main script for "Neural Networks from Scratch"
#
import numpy as np
import nnfs
from nnfs.datasets import spiral_data
from nnfs.datasets import vertical_data
import matplotlib.pyplot as plt

from nnClasses1 import Layer_Dense
from nnClasses1 import Activation_ReLU
from nnClasses1 import Activation_Softmax
from nnClasses1 import Loss_CategoricalCrossentropy
from nnClasses1 import Activation_Softmax_Loss_CategoricalCrossentropy

nnfs.init()


    
        
    
if __name__ == "__main__":

    ## Create spiral dataset
    X, y = spiral_data(samples=100, classes=3)

    ## Create vertical dataset
    #X, y = vertical_data(samples=100, classes=3)

    ## Create model
    # Create Dense layer with 2 input features and 3 output values
    dense1 = Layer_Dense(2, 3)

    # Create ReLU activation (to be used with dense layer)
    activation1 = Activation_ReLU()

    # Create second Dense layer with 3 input features (as we take output
    # of the previous layer here) and 3 output values
    dense2 = Layer_Dense(3, 3)

    # Create Softmax classifier's combined loss and activation
    loss_activation = Activation_Softmax_Loss_CategoricalCrossentropy()

    # Perform a forward pass of our training data through this layer
    dense1.forward(X)

    # Perform a forward pass through activation function
    # takes the output of the first dense layer here
    activation1.forward(dense1.output)

    # Perform a forward pass through second Dense layer
    # takes outputs of activation function of first layer as inputs
    dense2.forward(activation1.output)

    # Perform a forward through the activation/loss function
    # takes the output of the second dense layer here and returns loss
    loss = loss_activation.forward(dense2.output, y)

    # Print output of first few samples
    print(loss_activation.output[:5])

    # Print loss value
    print('loss: ', loss)

    # Calculate accuracy from output of activation2 and targets
    # calculate values along first axis
    predictions = np.argmax(loss_activation.output, axis=1)
    if len(y.shape) == 2:
        y = np.argmax(y, axis=1)
    accuracy = np.mean(predictions==y)

    # print accuracy
    print('acc: ', accuracy)

    # Backward pass
    loss_activation.backward(loss_activation.output, y)
    dense2.backward(loss_activation.dinputs)
    activation1.backward(dense2.dinputs)
    dense1.backward(activation1.dinputs)

    # print gradients
    print(dense1.dweights)
    print(dense1.dbiases)
    print(dense2.dweights)
    print(dense2.dbiases)
    





"""
    ## Create loss function
    loss_function = Loss_CategoricalCrossentropy()

    ## Helper variables
    lowest_loss = 9999999
    best_dense1_weights = dense1.weights.copy()
    best_dense1_biases = dense1.biases.copy()
    best_dense2_weights = dense2.weights.copy()
    best_dense2_biases = dense2.biases.copy()

    for iteration in range(10000):
        # Update weights with some small random values
        dense1.weights += 0.05 * np.random.randn(2, 3)
        dense1.biases += 0.05 * np.random.randn(1, 3)
        dense2.weights += 0.05 * np.random.randn(3, 3)
        dense2.biases += 0.05 * np.random.randn(1, 3)
        
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

        # Perform a foward pass through the activation
        # it takes the output of second dense layer here and returns loss
        loss = loss_function.calculate(activation2.output, y)

        # Calculate accuracy from output of activation2 and targets
        # calculate values along first axis
        predictions = np.argmax(activation2.output, axis=1)
        accuracy = np.mean(predictions==y)

        # If loss is smaller - print and save weights and biases aside
        if loss < lowest_loss:
            print("New set of weights found, iteration: ", iteration, "loss: ", loss, "acc : ", accuracy)
            best_dense1_weights = dense1.weights.copy()
            best_dense1_biases = dense1.biases.copy()
            best_dense2_weights = dense2.weights.copy()
            best_dense2_biases = dense2.biases.copy()
            lowest_loss = loss
        else:
            # Revert weights and biases
            dense1.weights = best_dense1_weights.copy()
            dense1.biases = best_dense1_biases.copy()
            dense2.weights = best_dense2_weights.copy()
            dense2.biases = best_dense2_biases.copy()
            

"""

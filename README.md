# Curve-Fitting-and-Interpolation-Studio

Curve-Fitting-and-Interpolation-Studio is a PyQt application that allows users to fit signals to mathematical models and perform interpolation of signals. The application provides a user-friendly interface for data input, model selection, and signal visualization.

## Features

1. Data Input: Users can input signal data in CSV format.
2. Curve Fitting: Users can fit signal data to mathematical models including polynomial, exponential, and power models. The application uses numerical optimization techniques to find the optimal model parameters that minimize the error between the fitted model and the signal data.
3. Interpolation: Users can perform interpolation of signals using linear or cubic spline interpolation methods. The application interpolates the signal data using a set of interpolation points to estimate the value of the signal at intermediate points.
4. Signal Visualization: The application provides users with visual representations of the input signal data, the fitted models, and the interpolated signals.
5. Exporting: Users can export the fitted models and interpolated signals in CSV format.

## Tech Stack

* Python: The application is developed using Python, a popular programming language for scientific computing and data analysis.
* PyQt: The application uses PyQt, a Python binding for the Qt toolkit, to create the user interface.
* NumPy: The application uses NumPy, a Python library for numerical computing, to perform curve fitting and interpolation.
* SciPy: The application uses SciPy, a Python library for scientific computing, to optimize the model parameters.

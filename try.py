# from _future_ import division

import matplotlib.pyplot as plt
import numpy as np
from sympy import *

# from sympy import latex


# x = np.linspace(-10, 10, 100)
# fx = []
# for i in range(len(x)):
#     fx.append(x[i] ** 2 - 2 * x[i] + 5)
#
# # X = simplify(x ** 2)
# # print(X)
# # plt.subplot(2, 1, 1)
# plt.plot(x, fx)
#
# plt.show()


x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)

x = np.linspace(-10, 10, 100)
f_x = []
for i in range(len(x)):
    f_x.append(x[i] ** 2 - 2 * x[i] + 5)

str = ""
str += "({-5})+ 5x^{5} + y^{5}"
str = "$" + str + "$"


# plt.plot(x, f_x)
# plt.text(0.6, 80, r'$x^{4}+ 2x^{3}+3x^{2}+x+6$')
# plt.title(str)
# plt.show()

list_of_coefficients = [1, 2, 3]

full_equation_string = ""  # The resulting string
for i, a in enumerate(list_of_coefficients):
    if int(a) == a:  # Remove the trailing .0
        a = int(a)
    if i == 0:  # First coefficient, no need for X
        if a > 0:
            full_equation_string += "{a} + ".format(a=a)
        elif a < 0:  # Negative a is printed like (a)
            full_equation_string += "({a}) + ".format(a=a)
        # a = 0 is not displayed
    elif i == 1:  # Second coefficient, only X and not X**i
        if a == 1:  # a = 1 does not need to be displayed
            full_equation_string += "x + "
        elif a > 0:
            full_equation_string += "{a}x + ".format(a=a)
        elif a < 0:
            full_equation_string += "({a})x + ".format(a=a)
    else:
        if i == (len(list_of_coefficients) - 1):
            if a == 1:
                # A special care needs to be addressed to put the exponent in {..} in LaTeX
                full_equation_string += "x^{i}".format(i=i)
            elif a > 0:
                full_equation_string += "{a}x^{i}".format(a=a, i=i)
            elif a < 0:
                full_equation_string += "({a})x^{i}".format(a=a, i=i)
        else:
            if a == 1:
                # A special care needs to be addressed to put the exponent in {..} in LaTeX
                full_equation_string += "x^{i} + ".format(i=i)
            elif a > 0:
                full_equation_string += "{a}x^{i} + ".format(a=a, i=i)
            elif a < 0:
                full_equation_string += "({a})x^{i} + ".format(a=a, i=i)
full_equation_string = "$"+full_equation_string+"$"
plt.plot(x, f_x)
plt.text(0.6, 80, r'$x^{4}+ 2x^{3}+3x^{2}+x+6$')
plt.title(full_equation_string)
plt.show()

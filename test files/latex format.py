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

plt.plot(x, f_x)
plt.text(0.6, 80, r'$x^{4}+ 2x^{3}+3x^{2}+x+6$')
plt.title(r'$x^{3}+ 2x^{2}+3$')
plt.show()



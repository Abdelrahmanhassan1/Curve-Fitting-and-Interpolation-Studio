import matplotlib.pyplot as plt
import numpy as np
# from sklearn.utils import check_array
from scipy.integrate import quad

x = np.linspace(0, 10, num=10)      # time domain input
y = np.sin(x)

coeff = np.polyfit(x, y, 1)
print(coeff)
print(coeff[::-1])
# xnew = np.linspace(0, 10, num=31)       # new time domain
ynew = np.polyval(coeff, x)

# plt.plot(x, y, "r", x, ynew, "b")
# plt.show()
#
#
#
# #########################
# # Calculating the percentage error using integration
#
# def percentage_error(actual, predicted):
#     res = np.empty(actual.shape)
#     for j in range(actual.shape[0]):
#         if actual[j] != 0:
#             res[j] = (actual[j] - predicted[j]) / actual[j]
#         else:
#             res[j] = predicted[j] / np.mean(actual)
#     return res
#
# def mean_absolute_percentage_error(y_true, y_pred):
#     return np.mean(np.abs(percentage_error(np.asarray(y_true), np.asarray(y_pred)))) * 100
#
# print(mean_absolute_percentage_error(y, ynew))
#
#
# # def mean_absolute_percentage_error(y_true, y_pred):
# #     y_true, y_pred = check_array(y_true, y_pred)
# #
# #     ## Note: does not handle mix 1d representation
# #     #if _is_1d(y_true):
# #     #    y_true, y_pred = _check_1d_array(y_true, y_pred)
# #
# #     return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
#
# # print(np.mean(np.abs((y - ynew) / y)) * 100)
# # print(mean_absolute_percentage_error(y, ynew))
#

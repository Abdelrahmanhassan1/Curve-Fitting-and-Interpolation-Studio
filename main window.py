import sys
from sklearn.metrics import mean_absolute_error
import matplotlib.patches as mpatches
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from maingui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ####################################################################
        # Variables:
        self.main_graph_figure = Figure()
        self.main_graph_canvas = FigureCanvas(self.main_graph_figure)
        self.ui.main_graph_layout.addWidget(self.main_graph_canvas)

        self.error_map_figure = Figure()
        self.error_map_canvas = FigureCanvas(self.error_map_figure)
        self.ui.verticalLayout.addWidget(self.error_map_canvas)

        # To make the text box take only numbers
        # self.onlyInt = QIntValidator()
        # self.ui.lineEdit.setValidator(self.onlyInt)
        # self.ui.lineEdit_2.setValidator(self.onlyInt)
        # self.ui.lineEdit_3.setValidator(self.onlyInt)
        # self.ui.lineEdit_4.setValidator(self.onlyInt)
        # self.ui.lineEdit_5.setValidator(self.onlyInt)

        # setting slider ranges:
        # one main chunk poly degree
        self.ui.horizontalSlider.setMinimum(1)
        self.ui.horizontalSlider.setMaximum(10)

        self.ui.poly_degree_slider.setMinimum(1)
        self.ui.poly_degree_slider.setMaximum(10)

        self.ui.num_of_chunks_slider.setMinimum(2)
        self.ui.num_of_chunks_slider.setMaximum(15)

        self.ui.extrapolation_slider.setMinimum(50)
        self.ui.extrapolation_slider.setMaximum(99)

        self.ui.overlap_slider.setMinimum(1)
        self.ui.overlap_slider.setMaximum(25)

        self.time_value = []
        self.amplitude_value = []
        self.number_of_chunks = 0
        self.degree_of_polynomial = 0
        self.overlap_percentage = 0
        self.extrapolation_percentage = 0
        self.degree_of_polynomial_of_one_main_chunk = 0
        self.full_signal_array_divided = []
        self.full_matrix_error_map = []
        self.row_of_error_map = []
        self.latex_equations_for_each_chunk = {}

        self.ui.tableWidget.setRowCount(6)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setColumnWidth(0, 300)

        self.ui.tableWidget.setHorizontalHeaderLabels("Variable;Value".split(";"))
        self.set_table_rows()
        #####################################################################
        # Buttons' Functions
        self.set_combo_box_items_for_error_map()
        # self.ui.lineEdit.setText("0")
        # self.ui.lineEdit_2.setText("0")
        # self.ui.lineEdit_3.setText("0")
        # self.ui.lineEdit_4.setText("0")
        self.ui.browse_button.clicked.connect(self.browse_signal_file)
        # self.ui.chunks_button.clicked.connect(self.set_number_of_chunks)
        # self.ui.degree_button.clicked.connect(self.set_degree_of_polynomial)
        self.ui.one_main_chunk_button.clicked.connect(self.display_one_main_chunk)
        self.ui.pushButton_3.clicked.connect(self.plot_data_splitted_with_chunks)
        self.ui.pushButton.clicked.connect(self.error_map)
        self.ui.pushButton_2.clicked.connect(self.reset)
        self.ui.pushButton_4.clicked.connect(self.display_latex_equation_for_each_chunk)
        self.ui.pushButton_5.clicked.connect(self.clipping_signal_and_applying_extrapolation)

        self.ui.num_of_chunks_slider.valueChanged.connect(self.set_number_of_chunks)
        self.ui.poly_degree_slider.valueChanged.connect(self.set_degree_of_polynomial)
        self.ui.overlap_slider.valueChanged.connect(self.set_overlap_percentage)
        self.ui.horizontalSlider.valueChanged.connect(self.set_degree_of_polynomial_of_one_main_chunk)
        self.ui.extrapolation_slider.valueChanged.connect(self.set_extrapolation_percentage)

    def set_table_rows(self):
        self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("Number OF Chunks"))
        self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem("Degree Of Polynomial"))
        self.ui.tableWidget.setItem(5, 0, QtWidgets.QTableWidgetItem("Overlap Percentage"))
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Degree Of Polynomial of One Main Chunk"))
        self.ui.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem("Extrapolation Percentage"))
        self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem("Error Percentage Of Polynomial"))

    def browse_signal_file(self):
        try:
            file_name = QFileDialog.getOpenFileName(filter="CSV (*.csv)")[0]
            data_frame = pd.read_csv(file_name)
            self.time_value = data_frame.iloc[:, 0].values
            self.amplitude_value = data_frame.iloc[:, 1].values
            print(len(self.amplitude_value))
            # Plot the signal
            self.plot_browsed_signal()
        except Exception as e:
            print(e)

    def plot_browsed_signal(self):
        try:
            axes = self.main_graph_figure.gca()
            axes.cla()
            axes.grid(True)
            axes.set_facecolor((1, 1, 1))
            axes.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            axes.set_xlabel("Time Value")
            axes.set_ylabel("Amplitude Value")
            axes.set_title("BioSignal")
            axes.legend()
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
        except Exception as e:
            print(e)

    def set_number_of_chunks(self):
        try:
            # if 0 < int(self.ui.lineEdit.text()) < 20:
            #     self.number_of_chunks = int(self.ui.lineEdit.text())
            #     self.ui.lineEdit.clear()
            #     # print(self.number_of_chunks)
            #     self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Number OF Chunks"))
            #     self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.number_of_chunks)))
            #     # self.ui.label_10.setText(str(self.number_of_chunks))
            # else:
            #     self.ui.lineEdit.clear()
            #     print("Invalid Number of Chunks")
            self.number_of_chunks = self.ui.num_of_chunks_slider.value()
            self.ui.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem(str(self.number_of_chunks)))

        except Exception as e:
            print(e)

    def set_degree_of_polynomial(self):
        try:
            # if 0 < int(self.ui.lineEdit_3.text()) < 10:
            #     self.degree_of_polynomial = int(self.ui.lineEdit_3.text())
            #     self.ui.lineEdit_3.clear()
            #     # print(self.degree_of_polynomial)
            #     self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("Degree Of Polynomial"))
            #     self.ui.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem(str(self.degree_of_polynomial)))
            #     # self.ui.label_11.setText(str(self.degree_of_polynomial))
            # else:
            #     self.ui.lineEdit_3.clear()
            #     print("Poor Conditioned Polynomial Degree choose between 1 ~ 9")
            self.degree_of_polynomial = self.ui.poly_degree_slider.value()
            self.ui.tableWidget.setItem(2, 1, QtWidgets.QTableWidgetItem(str(self.degree_of_polynomial)))

        except Exception as e:
            print(e)

    def set_overlap_percentage(self):
        try:
            # if self.ui.lineEdit_4.text() != "":
            #     if 0 <= int(self.ui.lineEdit_4.text()) < 26:
            #         self.overlap_percentage = int(self.ui.lineEdit_4.text()) / 100.0
            #         self.ui.lineEdit_4.clear()
            #         # print(self.overlap_percentage)
            #         self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem("Overlap Percentage"))
            #         self.ui.tableWidget.setItem(2, 1, QtWidgets.QTableWidgetItem(str(self.overlap_percentage)))
            #         # self.ui.label_12.setText(str(self.overlap_percentage))
            #     else:
            #         self.ui.lineEdit_4.clear()
            #         print("Enter Number between 0 ~ 25")
            self.overlap_percentage = self.ui.overlap_slider.value()
            self.ui.tableWidget.setItem(5, 1, QtWidgets.QTableWidgetItem(str(self.overlap_percentage)))

        except Exception as e:
            print(e)

    def set_extrapolation_percentage(self):
        try:
            # if self.ui.lineEdit_4.text() != "":
            #     if 0 <= int(self.ui.lineEdit_4.text()) < 26:
            #         self.overlap_percentage = int(self.ui.lineEdit_4.text()) / 100.0
            #         self.ui.lineEdit_4.clear()
            #         # print(self.overlap_percentage)
            #         self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem("Overlap Percentage"))
            #         self.ui.tableWidget.setItem(2, 1, QtWidgets.QTableWidgetItem(str(self.overlap_percentage)))
            #         # self.ui.label_12.setText(str(self.overlap_percentage))
            #     else:
            #         self.ui.lineEdit_4.clear()
            #         print("Enter Number between 0 ~ 25")
            self.extrapolation_percentage = self.ui.extrapolation_slider.value()
            self.ui.tableWidget.setItem(4, 1, QtWidgets.QTableWidgetItem(str(self.extrapolation_percentage)))

        except Exception as e:
            print(e)

    def set_degree_of_polynomial_of_one_main_chunk(self):
        try:
            # if 0 < int(self.ui.lineEdit_3.text()) < 10:
            #     self.degree_of_polynomial = int(self.ui.lineEdit_3.text())
            #     self.ui.lineEdit_3.clear()
            #     # print(self.degree_of_polynomial)
            #     self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("Degree Of Polynomial"))
            #     self.ui.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem(str(self.degree_of_polynomial)))
            #     # self.ui.label_11.setText(str(self.degree_of_polynomial))
            # else:
            #     self.ui.lineEdit_3.clear()
            #     print("Poor Conditioned Polynomial Degree choose between 1 ~ 9")
            self.degree_of_polynomial_of_one_main_chunk = self.ui.horizontalSlider.value()
            self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.degree_of_polynomial_of_one_main_chunk)))

        except Exception as e:
            print(e)

    def display_one_main_chunk(self):
        try:
            # self.degree_of_polynomial_of_one_main_chunk = int(self.ui.lineEdit_2.text())
            # self.ui.lineEdit_2.clear()
            coefficients_of_fitted_eqn = np.polyfit(self.time_value, self.amplitude_value,
                                                    self.degree_of_polynomial_of_one_main_chunk )
            # Coefficients from higher power
            amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, self.time_value)

            error_percentage = round(mean_absolute_error(self.amplitude_value, amplitude_fitted_values) * 100, 5)
            self.ui.label_14.setText(str(error_percentage) + "%")

            # self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem("Error Percentage Of Polynomial"))
            self.ui.tableWidget.setItem(3, 1, QtWidgets.QTableWidgetItem(str(error_percentage)))

            latex_equation_format = self.polynomial_to_latex(coefficients_of_fitted_eqn)
            # print(latex_equation_format)
            # print(error_percentage)

            ax_2 = self.main_graph_figure.gca()
            ax_2.cla()
            ax_2.grid(True)
            ax_2.set_facecolor((1, 1, 1))
            ax_2.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            ax_2.plot(self.time_value, amplitude_fitted_values, "r--",
                      label=f"Fitted Signal with polynomial of degree { self.degree_of_polynomial_of_one_main_chunk }.")
            ax_2.set_xlabel("Time Value")
            ax_2.set_ylabel("Amplitude Value")
            ax_2.set_title("BioSignal")
            leg_1 = ax_2.legend(loc="lower center")
            red_patch = mpatches.Patch(color='red', label=latex_equation_format)
            leg_2 = ax_2.legend(handles=[red_patch], loc="upper center")
            ax_2.add_artist(leg_1)
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
        except Exception as e:
            print(e)

    def chunks_divider(self):
        try:
            self.full_signal_array_divided = []
            self.latex_equations_for_each_chunk = {}
            length_of_data = len(self.time_value)
            self.set_combo_box_items_for_multiple_chunks()
            for i in range(self.number_of_chunks):
                start = int((i * length_of_data / self.number_of_chunks))
                end = int(((i + 1) * length_of_data / self.number_of_chunks))
                # print(start)
                # print(end)
                coefficients = np.polyfit(self.time_value[start: end], self.amplitude_value[start: end],
                                   self.degree_of_polynomial)
                fitted_data = np.polyval(coefficients, self.time_value[start:end])
                latex_equation = self.polynomial_to_latex(coefficients)
                self.latex_equations_for_each_chunk[f"{i+1}"] = latex_equation
                # print(latex_equations_for_each_chunk)
                self.full_signal_array_divided.extend(fitted_data)
                # print(len(self.full_signal_array))
        except Exception as e:
            print(e)

    def plot_data_splitted_with_chunks(self):
        try:
            self.chunks_divider()
            ax_3 = self.main_graph_figure.gca()
            ax_3.cla()
            ax_3.grid(True)
            ax_3.set_facecolor((1, 1, 1))
            ax_3.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            ax_3.plot(self.time_value, self.full_signal_array_divided, "r--",
                      label=f"Fitted Signal with {self.number_of_chunks} Chunks and polynomial of degree {self.degree_of_polynomial}.")
            ax_3.legend(loc="best")
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
            self.ui.label_14.setText("0")
        except Exception as e:
            print(e)

    def polynomial_to_latex(self, list_of_coefficients):
        # Note In the code Below I want the coefficients to be from x to the power 0 and increasing through degrees
        # So i need to reverse my coefficients as it was collected in decreasing order
        list_of_coefficients = list_of_coefficients[::-1]
        full_equation_string = ""  # The resulting string
        for index, index_value in enumerate(list_of_coefficients):

            if int(index_value) == index_value:  # Remove the trailing .0
                index_value = int(index_value)

            index_value = round(index_value, 5)

            if index == 0:  # First coefficient, no need for X
                if index_value > 0:
                    full_equation_string += "{a} + ".format(a=index_value)
                elif index_value < 0:  # Negative a is printed like (a)
                    full_equation_string += "({a}) + ".format(a=index_value)
                # a = 0 is not displayed

            elif index == 1:  # Second coefficient, only X and not X**i
                if index_value == 1:  # a = 1 does not need to be displayed
                    full_equation_string += "x + "
                elif index_value > 0:
                    full_equation_string += "{a}x + ".format(a=index_value)
                elif index_value < 0:
                    full_equation_string += "({a})x + ".format(a=index_value)

            else:
                if index == (len(list_of_coefficients) - 1):
                    if index_value == 1:
                        # A special care needs to be addressed to put the exponent in {..} in LaTeX
                        full_equation_string += "x^{i}".format(i=index)
                    elif index_value > 0:
                        full_equation_string += "{a}x^{i}".format(a=index_value, i=index)
                    elif index_value < 0:
                        full_equation_string += "({a})x^{i}".format(a=index_value, i=index)
                else:
                    if index_value == 1:
                        # A special care needs to be addressed to put the exponent in {..} in LaTeX
                        full_equation_string += "x^{i} + ".format(i=index)
                    elif index_value > 0:
                        full_equation_string += "{a}x^{i} + ".format(a=index_value, i=index)
                    elif index_value < 0:
                        full_equation_string += "({a})x^{i} + ".format(a=index_value, i=index)
        full_equation_string = "$" + full_equation_string + "$"
        return full_equation_string

    def set_combo_box_items_for_error_map(self):
        self.ui.comboBox.addItems(["Number Of Chunks", "Degree of Polynomial", "Overlap Percentage"])
        self.ui.comboBox_2.addItems(["Degree of Polynomial", "Number Of Chunks", "Overlap Percentage"])

    # def dividing_chunks_using_overlap_percentage(self):
    #     try:
    #         # self.set_overlap_percentage()
    #         chunks_overall_data = []
    #         time_overall_data = []
    #         chunk_data = []
    #         time_data = []
    #         start = 0
    #         length_of_data = len(self.time_value)
    #         chunk_length = abs(int(length_of_data / (self.number_of_chunks - (self.number_of_chunks - 1) * self.overlap_percentage)))
    #         # print(chunk_length)
    #         moving_step = int(chunk_length * (1 - self.overlap_percentage) + 0.5)
    #         # print(moving_step)
    #         for i in range(0, self.number_of_chunks):
    #             chunk_data = list(self.amplitude_value[start: start + chunk_length])
    #             time_data = list(self.time_value[start: start + chunk_length])
    #             chunks_overall_data.append(chunk_data)
    #             time_overall_data.append(time_data)
    #             start += moving_step
    #             # print(chunk_data)
    #         # print(chunks_overall_data)
    #         # print(chunks_overall_data)
    #         # print(time_overall_data)
    #         return time_overall_data, chunks_overall_data
    #     except Exception as e:
    #         print(e)

    def error_map(self):
        try:
            progress_bar_value = 0
            time_overall_data = []
            chunks_overall_data = []
            self.full_matrix_error_map = []
            x_axis_element = self.ui.comboBox.currentIndex()
            y_axis_element = self.ui.comboBox_2.currentIndex()
            # print(x_axis_element, y_axis_element)

            if (x_axis_element == 1) and (y_axis_element == 1):
                # Number Of Chunks is on Y_axis, Polynomial Degree is on X-axis, overlap_percentage remains constant:
                time_overall_data, chunks_overall_data = \
                    self.dividing_chunks_using_overlap_percentage_for_error_map(self.overlap_percentage,
                                                                                self.number_of_chunks)
                for chunk_number in range(0, self.number_of_chunks):
                    chunk_data = chunks_overall_data[chunk_number]
                    time_data = time_overall_data[chunk_number]
                    self.row_of_error_map = []
                    for degree in range(1, self.degree_of_polynomial + 1):
                        coefficients_of_fitted_eqn = np.polyfit(time_data, chunk_data,
                                                                degree)
                        amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
                        error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
                        self.row_of_error_map.append(error_percentage)

                    progress_bar_value += chunk_number * 5
                    self.ui.progressBar.setValue(progress_bar_value)
                    self.full_matrix_error_map.append(self.row_of_error_map)

                # Plotting the Error Map:
                self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
                self.plot_error_map(self.full_matrix_error_map, "Polynomial Degree", "Number Of Chunks")
                self.ui.progressBar.setValue(100)

            elif (x_axis_element == 0) and (y_axis_element == 0):
                # Number Of Chunks is on X_axis, Polynomial Degree is on Y-axis, overlap_percentage is constant:
                time_overall_data, chunks_overall_data = \
                    self.dividing_chunks_using_overlap_percentage_for_error_map(self.overlap_percentage,
                                                                                self.number_of_chunks)
                for degree in range(1, self.degree_of_polynomial + 1):
                    self.row_of_error_map = []
                    for chunk_number in range(0, self.number_of_chunks):
                        chunk_data = chunks_overall_data[chunk_number]
                        time_data = time_overall_data[chunk_number]
                        coefficients_of_fitted_eqn = np.polyfit(time_data, chunk_data,
                                                                degree)
                        amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
                        error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
                        self.row_of_error_map.append(error_percentage)

                    progress_bar_value += degree * 5
                    self.ui.progressBar.setValue(progress_bar_value)
                    self.full_matrix_error_map.append(self.row_of_error_map)

                # Plotting the Error Map:
                self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
                self.plot_error_map(self.full_matrix_error_map, "Number Of Chunks", "Polynomial Degree")
                self.ui.progressBar.setValue(100)

            elif (x_axis_element == 0) and (y_axis_element == 2):
                # X_axis is Number of chunks and Y_axis is overlap Percentage and poly_degree is constant:
                for percentage in range(1, self.overlap_percentage+1):
                    self.row_of_error_map = []
                    percentage /= 100
                    time_overall_data, chunks_overall_data = \
                        self.dividing_chunks_using_overlap_percentage_for_error_map(percentage,
                                                                                    self.number_of_chunks)
                    for chunk_number in range(0, self.number_of_chunks):
                        chunk_data = chunks_overall_data[chunk_number]
                        time_data = time_overall_data[chunk_number]
                        coefficients_of_fitted_eqn = np.polyfit(time_data, chunk_data,
                                                                self.degree_of_polynomial)
                        amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
                        error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
                        self.row_of_error_map.append(error_percentage)

                    progress_bar_value += int(percentage*100) * 3
                    self.ui.progressBar.setValue(progress_bar_value)
                    self.full_matrix_error_map.append(self.row_of_error_map)

                # Plotting the Error Map:
                self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
                self.plot_error_map(self.full_matrix_error_map, "Number of Chunks", "Overlap Percentage")
                self.ui.progressBar.setValue(100)

            elif (x_axis_element == 1) and (y_axis_element == 2):   # Check
                # X_axis is Degree of polynomial and Y_axis is overlap Percentage and number of chunks is constant:
                for percentage in range(1, self.overlap_percentage+1):
                    percentage /= 100
                    time_overall_data, chunks_overall_data = \
                        self.dividing_chunks_using_overlap_percentage_for_error_map(percentage,
                                                                                    self.number_of_chunks)
                    for degree in range(1, self.degree_of_polynomial+1):
                        self.row_of_error_map = []
                        for chunk_number in range(0, self.number_of_chunks):
                            chunk_data = chunks_overall_data[chunk_number]
                            time_data = time_overall_data[chunk_number]
                            coefficients_of_fitted_eqn = np.polyfit(time_data, chunk_data,
                                                                    degree)
                            amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
                            error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
                            self.row_of_error_map.append(error_percentage)

                    self.full_matrix_error_map.append(self.row_of_error_map)
                    progress_bar_value += int(percentage * 100) * 3
                    self.ui.progressBar.setValue(progress_bar_value)

                # Plotting the Error Map:
                self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
                self.plot_error_map(self.full_matrix_error_map, "Degree Of Polynomial", "Overlap Percentage")
                self.ui.progressBar.setValue(100)

            elif (x_axis_element == 2) and (y_axis_element == 0):
                # X_axis is Overlap Percentage and Y_axis is degree of polynomial and number of chunks is constant
                for degree in range(1, self.degree_of_polynomial+1):
                    for percentage in range(1, self.overlap_percentage+1):
                        percentage /= 100
                        self.row_of_error_map = []
                        time_overall_data, chunks_overall_data = \
                            self.dividing_chunks_using_overlap_percentage_for_error_map(percentage,
                                                                                        self.number_of_chunks)
                        for chunk_number in range(0, self.number_of_chunks):
                            chunk_data = chunks_overall_data[chunk_number]
                            time_data = time_overall_data[chunk_number]
                            coefficients_of_fitted_eqn = np.polyfit(time_data, chunk_data,
                                                                    degree)
                            amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
                            error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
                            self.row_of_error_map.append(error_percentage)

                    self.full_matrix_error_map.append(self.row_of_error_map)
                    progress_bar_value += degree * 3
                    self.ui.progressBar.setValue(progress_bar_value)

                # Plotting the Error Map:
                self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
                self.plot_error_map(self.full_matrix_error_map, "Overlap Percentage", "Degree Of Polynomial")
                self.ui.progressBar.setValue(100)

            elif (x_axis_element == 2) and (y_axis_element == 1):
                # X_axis is Overlap Percentage and y_axis is number of chunks and degree of polynomial is constant:
                for chunk_number in range(0, self.number_of_chunks):
                    self.row_of_error_map = []
                    for percentage in range(1, self.overlap_percentage + 1):
                        percentage /= 100
                        time_overall_data, chunks_overall_data = \
                            self.dividing_chunks_using_overlap_percentage_for_error_map(percentage,
                                                                                        self.number_of_chunks)
                        chunk_data = chunks_overall_data[chunk_number]
                        time_data = time_overall_data[chunk_number]
                        coefficients_of_fitted_eqn = np.polyfit(time_data, chunk_data,
                                                                self.degree_of_polynomial)
                        amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
                        error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
                        self.row_of_error_map.append(error_percentage)

                    self.full_matrix_error_map.append(self.row_of_error_map)
                    progress_bar_value += chunk_number * 3
                    self.ui.progressBar.setValue(progress_bar_value)

                # Plotting the Error Map:
                self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
                self.plot_error_map(self.full_matrix_error_map, "Overlap Percentage", "Number Of Chunks")
                self.ui.progressBar.setValue(100)
                pass

            else:
                print("Invalid Axes Elements! Choose Two different elements from each combo box")

        except Exception as e:
            print(e)

    def dividing_chunks_using_overlap_percentage_for_error_map(self, overlap_percentage, number_of_chunks):
        try:
            # self.set_overlap_percentage()
            chunks_overall_data = []
            time_overall_data = []
            chunk_data = []
            time_data = []
            start = 0
            length_of_data = len(self.time_value)
            chunk_length = abs(int(length_of_data / (number_of_chunks - (number_of_chunks - 1) * overlap_percentage)))
            # print(chunk_length)
            moving_step = int(chunk_length * (1 - overlap_percentage) + 0.5)
            # print(moving_step)
            for i in range(0, number_of_chunks):
                chunk_data = list(self.amplitude_value[start: start + chunk_length])
                time_data = list(self.time_value[start: start + chunk_length])
                chunks_overall_data.append(chunk_data)
                time_overall_data.append(time_data)
                start += moving_step
                # print(chunk_data)
            # print(chunks_overall_data)
            # print(chunks_overall_data)
            # print(time_overall_data)
            return time_overall_data, chunks_overall_data
        except Exception as e:
            print(e)

    def plot_error_map(self, matrix, x_label, y_label):
        error_ax = self.error_map_figure.gca()
        error_ax.imshow(matrix)
        error_ax.set_ylabel(y_label)
        error_ax.set_xlabel(x_label)
        error_ax.set_title("Error Map!")
        error_ax.set_xticks([])
        error_ax.set_yticks([])
        self.error_map_canvas.draw()
        self.error_map_canvas.flush_events()

    def reset(self):
        try:
            axes = self.error_map_figure.gca()
            axes.cla()
            axes_1 = self.main_graph_figure.gca()
            axes_1.cla()
            self.time_value = 0
            self.amplitude_value = 0
            self.overlap_percentage = 0
            self.number_of_chunks = 0
            self.degree_of_polynomial = 0
            # self.ui.lineEdit.setText("0")
            # self.ui.lineEdit_2.setText("0")
            # self.ui.lineEdit_3.setText("0")
            # self.ui.lineEdit_4.setText("0")
            self.ui.comboBox_3.clear()
            self.ui.progressBar.setValue(0)
            self.ui.horizontalSlider.setValue(1)
            self.ui.poly_degree_slider.setValue(1)
            self.ui.num_of_chunks_slider.setValue(2)
            self.ui.extrapolation_slider.setValue(50)
            self.ui.overlap_slider.setValue(1)
            self.ui.tableWidget.clear()
            self.set_table_rows()
            self.error_map_canvas.draw()
            self.error_map_canvas.flush_events()
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
        except Exception as e:
            print(e)

    def set_combo_box_items_for_multiple_chunks(self):
        try:
            self.ui.comboBox_3.clear()
            for i in range(self.number_of_chunks):
                self.ui.comboBox_3.addItem(f"Chunk {i+1}")
        except Exception as e:
            print(e)

    def display_latex_equation_for_each_chunk(self):
        try:
            combo_box_index = self.ui.comboBox_3.currentIndex()
            latex_equation = self.latex_equations_for_each_chunk[f"{combo_box_index+1}"]
            ax_4 = self.main_graph_figure.gca()
            ax_4.cla()
            ax_4.grid(True)
            ax_4.set_facecolor((1, 1, 1))
            ax_4.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            ax_4.plot(self.time_value, self.full_signal_array_divided, "r--",
                      label=f"Fitted Signal with {self.number_of_chunks} Chunks and polynomial of degree {self.degree_of_polynomial}.")
            leg_1 = ax_4.legend(loc="lower center")
            red_patch = mpatches.Patch(color='red', label=latex_equation)
            leg_2 = ax_4.legend(handles=[red_patch], loc="upper center")
            ax_4.add_artist(leg_1)
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
        except Exception as e:
            print(e)

    def clipping_signal_and_applying_extrapolation(self):
        try:
            full_signal = []
            # if 49 < int(self.ui.lineEdit_5.text()) < 100:
            clipped_percentage = self.extrapolation_percentage / 100
            length_of_data = len(self.time_value)
            end = int(clipped_percentage * length_of_data)

            coefficients_of_fitted_eqn = np.polyfit(self.time_value[0:end], self.amplitude_value[0:end],
                                                    self.degree_of_polynomial_of_one_main_chunk)
            # Coefficients from higher power
            amplitude_fitted_values_for_the_left_clip = np.polyval(coefficients_of_fitted_eqn, self.time_value[0:end])
            # Represent the extrapolation part:
            full_signal.extend(amplitude_fitted_values_for_the_left_clip)

            amplitude_fitted_values_for_the_right_clip = np.polyval(coefficients_of_fitted_eqn,
                                                                    self.time_value[end:length_of_data])
            full_signal.extend(amplitude_fitted_values_for_the_right_clip)

            latex_equation = self.polynomial_to_latex(coefficients_of_fitted_eqn)

            ax_5 = self.main_graph_figure.gca()
            ax_5.cla()
            ax_5.grid(True)
            ax_5.set_facecolor((1, 1, 1))
            ax_5.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            ax_5.plot(self.time_value, full_signal, "r--",
                      label="Signal With Extrapolation.")
            # leg_1 = ax_5.legend(loc="lower center")
            red_patch = mpatches.Patch(color='red', label="latex Equation of fitted part:"+latex_equation)
            leg_2 = ax_5.legend(handles=[red_patch], loc="best")
            # ax_5.add_artist(leg_1)
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
            # else:
            #     print("Invalid Clipping Percentage 50 ~ 99 %")
        except Exception as e:
            print(e)

    # def create_combo_box_chunks_names(self, number_of_chunks):
    #     try:
    #         self.ui.chunks_combo_box.clear()
    #         for chunk_number in range(1, int(number_of_chunks)+1):
    #             self.ui.chunks_combo_box.addItem(f"chunk: {chunk_number}")
    #     except Exception as e:
    #         print(e)

    # def polynomial_interpolation(self, time_value, amplitude_value, order_of_polynomial):
    #     try:
    #         coefficients_of_fitted_eqn = np.polyfit(time_value, amplitude_value, order_of_polynomial)
    #         amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_value)
    #         return amplitude_fitted_values
    #     except Exception as e:
    #         print(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Curve Fitting and Interpolation")
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

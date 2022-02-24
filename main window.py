import sys
# from sklearn.metrics import mean_absolute_error
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
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
        self.x_axes_text = [
            "Number of Chunks",
            "Polynomial Degree",
            "Overlap Percentage"
        ]
        self.y_axes_text = [
            "Polynomial Degree",
            "Number of Chunks",
            "Overlap Percentage"
        ]

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
            main_graph_axes = self.main_graph_figure.gca()
            main_graph_axes.cla()
            main_graph_axes.grid(True)
            main_graph_axes.set_facecolor((1, 1, 1))
            main_graph_axes.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            main_graph_axes.set_xlabel("Time Value")
            main_graph_axes.set_ylabel("Amplitude Value")
            main_graph_axes.set_title("BioSignal")
            main_graph_axes.legend()
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
        except Exception as e:
            print(e)

    def set_number_of_chunks(self):
        try:
            self.number_of_chunks = self.ui.num_of_chunks_slider.value()
            self.ui.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem(str(self.number_of_chunks)))
        except Exception as e:
            print(e)

    def set_degree_of_polynomial(self):
        try:
            self.degree_of_polynomial = self.ui.poly_degree_slider.value()
            self.ui.tableWidget.setItem(2, 1, QtWidgets.QTableWidgetItem(str(self.degree_of_polynomial)))
        except Exception as e:
            print(e)

    def set_overlap_percentage(self):
        try:
            self.overlap_percentage = self.ui.overlap_slider.value()
            self.ui.tableWidget.setItem(5, 1, QtWidgets.QTableWidgetItem(str(self.overlap_percentage)))
        except Exception as e:
            print(e)

    def set_extrapolation_percentage(self):
        try:
            self.extrapolation_percentage = self.ui.extrapolation_slider.value()
            self.ui.tableWidget.setItem(4, 1, QtWidgets.QTableWidgetItem(str(self.extrapolation_percentage)))
        except Exception as e:
            print(e)

    def set_degree_of_polynomial_of_one_main_chunk(self):
        try:
            self.degree_of_polynomial_of_one_main_chunk = self.ui.horizontalSlider.value()
            self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.degree_of_polynomial_of_one_main_chunk)))
        except Exception as e:
            print(e)

    def get2DErrorArray(self, polynomialOrderVals, overlappingSizePercentageVals, numberOfChunksVals):

        if (len(polynomialOrderVals) != 1 and len(numberOfChunksVals) != 1):
            errorMap = np.zeros((len(polynomialOrderVals),len(numberOfChunksVals)))
        elif (len(polynomialOrderVals) != 1):
            errorMap = np.zeros((len(polynomialOrderVals),len(overlappingSizePercentageVals)))
        else:
            errorMap = np.zeros((len(overlappingSizePercentageVals),len(numberOfChunksVals)))

        for polynomialOrder in polynomialOrderVals:
            for overlappingSizePercentage in overlappingSizePercentageVals:
                for numberOfChunks in numberOfChunksVals:
                    
                    xAxesChunksValues = np.array_split(self.time_value,numberOfChunks)
                    yAxesChunksValues = np.array_split(self.amplitude_value,numberOfChunks)

                    chunkSize = int(len(self.time_value) / numberOfChunks)
                    overlappedPointsNumber = int(chunkSize * overlappingSizePercentage /100)
                    resError = 0

                    for chunkIndex in range(numberOfChunks):

                        chunkStartIndex = (chunkIndex)*len(xAxesChunksValues[chunkIndex])
                        chunkEndIndex = chunkStartIndex + len(xAxesChunksValues[chunkIndex])

                        if (numberOfChunks > 1):
                            
                            # case 1: we want append to the first chunk
                            if (chunkIndex == 0):
                                chunkEndIndex += overlappedPointsNumber
                            # case 2: we want to append to the last chunk
                            elif (chunkIndex == (numberOfChunks - 1)):
                                chunkStartIndex -= overlappedPointsNumber
                            # case 3: we want to append to a mid chunk
                            else:
                                chunkStartIndex -= int(overlappedPointsNumber/2)
                                chunkEndIndex += int(np.ceil(overlappedPointsNumber/2))

                        xAxesChunksValues[chunkIndex] = self.time_value[chunkStartIndex:chunkEndIndex]
                        yAxesChunksValues[chunkIndex] = self.amplitude_value[chunkStartIndex:chunkEndIndex]
                        polynomial = np.polyfit(xAxesChunksValues[chunkIndex], yAxesChunksValues[chunkIndex], polynomialOrder)  
                        resError += np.sum((np.polyval(polynomial, xAxesChunksValues[chunkIndex]) - yAxesChunksValues[chunkIndex])**2)
                    
                    resError /= numberOfChunks
                    error = np.sqrt(resError/(len(self.time_value)-2)) 
                    
                    if (len(polynomialOrderVals) != 1 and len(numberOfChunksVals) != 1):
                        errorMap[polynomialOrder - 1][numberOfChunks - 1] = error
                    elif (len(polynomialOrderVals) != 1):
                        errorMap[polynomialOrder - 1][int(overlappingSizePercentage)] = error
                    else:
                        errorMap[int(overlappingSizePercentage/5)][numberOfChunks - 1] = error

        return errorMap

    def error_map(self):
        try:
            progress_bar_value = 0
            time_overall_data = []
            chunks_overall_data = []
            self.full_matrix_error_map = []
            x_axis_element = self.ui.comboBox.currentIndex()
            y_axis_element = self.ui.comboBox_2.currentIndex()

            # print(x_axis_element, y_axis_element)

            polynomialArray = [5] if x_axis_element or y_axis_element else range(1, self.degree_of_polynomial+1)

            degree_of_polynomial_indexed = range(1,self.degree_of_polynomial + 1) if x_axis_element == 1 or y_axis_element == 0 else [self.degree_of_polynomial]
            overlap_percentage_indexed = range(0,self.overlap_percentage) if x_axis_element == 2 or y_axis_element == 2 else [self.overlap_percentage]
            number_of_chunks_indexed = range(1,self.number_of_chunks) if x_axis_element == 0 or y_axis_element == 1 else [self.number_of_chunks]
            
            errorMap = self.get2DErrorArray(degree_of_polynomial_indexed, overlap_percentage_indexed, number_of_chunks_indexed)

            if (y_axis_element == 1) or (x_axis_element == 1) or (y_axis_element == 2 and x_axis_element == 1):
                errorMap = np.transpose(errorMap) 
            # swap  prio: number of chunks-yaxes  -> poly-xaxex -> over-poly
            
            # errorMap = np.flip(errorMap,0)
            self.plot_error_map(errorMap, self.x_axes_text[x_axis_element], self.y_axes_text[y_axis_element])

            # for deg

            # if x_axis_element == 1:
            #     if y_axis_element == 1:
            #         # Number Of Chunks is on Y_axis, Polynomial Degree is on X-axis, overlap_percentage remains constant:
            #         time_overall_data, chunks_overall_data = \
            #             self.dividing_chunks_using_overlap_percentage_for_error_map(self.overlap_percentage,
            #                                                                         self.number_of_chunks)
            #         for chunk_number in range(0, self.number_of_chunks):
            #             chunk_data = chunks_overall_data[chunk_number]
            #             time_data = time_overall_data[chunk_number]
            #             self.row_of_error_map = []
            #             for degree in range(1, self.degree_of_polynomial + 1):
            #                 coefficients_of_fitted_eqn = np.around(np.polyfit(time_data, chunk_data,
            #                                                         degree),2)
            #                 amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
            #                 error_percentage = round(self.calculate_error_percentage(chunk_data, amplitude_fitted_values), 4)
            #                 self.row_of_error_map.append(error_percentage)

            #             progress_bar_value += chunk_number * 5
            #             self.ui.progressBar.setValue(progress_bar_value)
            #             self.full_matrix_error_map.append(self.row_of_error_map)

            #         # Plotting the Error Map:
            #         # self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
            #         self.plot_error_map(self.full_matrix_error_map, "Polynomial Degree", "Number Of Chunks")
            #         self.ui.progressBar.setValue(100)
            #     if y_axis_element == 2:
            #         # X_axis is Degree of polynomial and Y_axis is overlap Percentage and number of chunks is constant:
            #         for percentage in range(1, self.overlap_percentage + 1):
            #             percentage /= 100
            #             time_overall_data, chunks_overall_data = \
            #                 self.dividing_chunks_using_overlap_percentage_for_error_map(percentage,
            #                                                                             self.number_of_chunks)
            #             for degree in range(1, self.degree_of_polynomial + 1):
            #                 self.row_of_error_map = []
            #                 for chunk_number in range(0, self.number_of_chunks):
            #                     chunk_data = chunks_overall_data[chunk_number]
            #                     time_data = time_overall_data[chunk_number]
            #                     coefficients_of_fitted_eqn = np.around(np.polyfit(time_data, chunk_data,
            #                                                                       degree), 2)
            #                     amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
            #                     # error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
            #                     error_percentage = round(
            #                         self.calculate_error_percentage(chunk_data, amplitude_fitted_values), 4)
            #                     self.row_of_error_map.append(error_percentage)

            #             self.full_matrix_error_map.append(self.row_of_error_map)
            #             progress_bar_value += int(percentage * 100) * 3
            #             self.ui.progressBar.setValue(progress_bar_value)

            #         # Plotting the Error Map:
            #         # self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
            #         self.plot_error_map(self.full_matrix_error_map, "Degree Of Polynomial", "Overlap Percentage")
            #         self.ui.progressBar.setValue(100)

            # elif x_axis_element == 0:
            #     if y_axis_element == 0:
            #         # Number Of Chunks is on X_axis, Polynomial Degree is on Y-axis, overlap_percentage is constant:
            #         time_overall_data, chunks_overall_data = \
            #             self.dividing_chunks_using_overlap_percentage_for_error_map(self.overlap_percentage,
            #                                                                         self.number_of_chunks)
            #         for degree in range(1, self.degree_of_polynomial + 1):
            #             self.row_of_error_map = []
            #             for chunk_number in range(0, self.number_of_chunks):
            #                 chunk_data = chunks_overall_data[chunk_number]
            #                 time_data = time_overall_data[chunk_number]
            #                 coefficients_of_fitted_eqn = np.around(np.polyfit(time_data, chunk_data,
            #                                                         degree),2)
            #                 amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
            #                 # error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
            #                 error_percentage = round(self.calculate_error_percentage(chunk_data, amplitude_fitted_values), 4)
            #                 self.row_of_error_map.append(error_percentage)

            #             progress_bar_value += degree * 5
            #             self.ui.progressBar.setValue(progress_bar_value)
            #             self.full_matrix_error_map.append(self.row_of_error_map)

            #         # Plotting the Error Map:
            #         # self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
            #         self.plot_error_map(self.full_matrix_error_map, "Number Of Chunks", "Polynomial Degree")
            #         self.ui.progressBar.setValue(100)
            #     if y_axis_element == 2:
            #         # X_axis is Number of chunks and Y_axis is overlap Percentage and poly_degree is constant:
            #         for percentage in range(1, self.overlap_percentage + 1):
            #             self.row_of_error_map = []
            #             percentage /= 100
            #             time_overall_data, chunks_overall_data = \
            #                 self.dividing_chunks_using_overlap_percentage_for_error_map(percentage,
            #                                                                             self.number_of_chunks)
            #             for chunk_number in range(0, self.number_of_chunks):
            #                 chunk_data = chunks_overall_data[chunk_number]
            #                 time_data = time_overall_data[chunk_number]
            #                 coefficients_of_fitted_eqn = np.around(np.polyfit(time_data, chunk_data,
            #                                                                   self.degree_of_polynomial), 2)
            #                 amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
            #                 # error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
            #                 error_percentage = round(
            #                     self.calculate_error_percentage(chunk_data, amplitude_fitted_values), 4)
            #                 self.row_of_error_map.append(error_percentage)

            #             progress_bar_value += int(percentage * 100) * 3
            #             self.ui.progressBar.setValue(progress_bar_value)
            #             self.full_matrix_error_map.append(self.row_of_error_map)

            #         # Plotting the Error Map:
            #         # self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
            #         self.plot_error_map(self.full_matrix_error_map, "Number of Chunks", "Overlap Percentage")
            #         self.ui.progressBar.setValue(100)

            # elif x_axis_element == 2:
            #     if y_axis_element == 0:
            #         # X_axis is Overlap Percentage and Y_axis is degree of polynomial and number of chunks is constant
            #         for degree in range(1, self.degree_of_polynomial+1):
            #             for percentage in range(1, self.overlap_percentage+1):
            #                 percentage /= 100
            #                 self.row_of_error_map = []
            #                 time_overall_data, chunks_overall_data = \
            #                     self.dividing_chunks_using_overlap_percentage_for_error_map(percentage,
            #                                                                                 self.number_of_chunks)
            #                 for chunk_number in range(0, self.number_of_chunks):
            #                     chunk_data = chunks_overall_data[chunk_number]
            #                     time_data = time_overall_data[chunk_number]
            #                     coefficients_of_fitted_eqn = np.around(np.polyfit(time_data, chunk_data,
            #                                                             degree),2)
            #                     amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
            #                     error_percentage = round(self.calculate_error_percentage(chunk_data, amplitude_fitted_values), 4)
            #                     self.row_of_error_map.append(error_percentage)

            #             self.full_matrix_error_map.append(self.row_of_error_map)
            #             progress_bar_value += degree * 3
            #             self.ui.progressBar.setValue(progress_bar_value)

            #         # Plotting the Error Map:
            #         # self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
            #         self.plot_error_map(self.full_matrix_error_map, "Overlap Percentage", "Degree Of Polynomial")
            #         self.ui.progressBar.setValue(100)
            #     if y_axis_element == 1:
            #         # X_axis is Overlap Percentage and y_axis is number of chunks and degree of polynomial is constant:
            #         for chunk_number in range(0, self.number_of_chunks):
            #             self.row_of_error_map = []
            #             for percentage in range(1, self.overlap_percentage + 1):
            #                 percentage /= 100
            #                 time_overall_data, chunks_overall_data = \
            #                     self.dividing_chunks_using_overlap_percentage_for_error_map(percentage,
            #                                                                                 self.number_of_chunks)
            #                 chunk_data = chunks_overall_data[chunk_number]
            #                 time_data = time_overall_data[chunk_number]
            #                 coefficients_of_fitted_eqn = np.around(np.polyfit(time_data, chunk_data,
            #                                                                   self.degree_of_polynomial), 2)
            #                 amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
            #                 # error_percentage = mean_absolute_error(chunk_data, amplitude_fitted_values) * 100
            #                 error_percentage = round(
            #                     self.calculate_error_percentage(chunk_data, amplitude_fitted_values), 4)
            #                 self.row_of_error_map.append(error_percentage)

            #             self.full_matrix_error_map.append(self.row_of_error_map)
            #             progress_bar_value += chunk_number * 3
            #             self.ui.progressBar.setValue(progress_bar_value)

            #         # Plotting the Error Map:
            #         # self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
            #         self.plot_error_map(self.full_matrix_error_map, "Overlap Percentage", "Number Of Chunks")
            #         self.ui.progressBar.setValue(100)
            # else:
            #     print("Invalid Axes Elements! Choose Two different elements from each combo box")

        except Exception as e:
            print(e)

    def display_one_main_chunk(self):
        try:
            coefficients_of_fitted_eqn = np.around(np.polyfit(self.time_value, self.amplitude_value,
                                                    self.degree_of_polynomial_of_one_main_chunk), 2)
            # Coefficients from higher power
            amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, self.time_value)

            # error_percentage = round(mean_absolute_error(self.amplitude_value, amplitude_fitted_values) * 100, 2)
            error_percentage = round(self.calculate_error_percentage(self.amplitude_value, amplitude_fitted_values), 2)
            self.ui.label_14.setText(str(error_percentage) + "%")

            self.ui.tableWidget.setItem(3, 1, QtWidgets.QTableWidgetItem(str(error_percentage)))

            latex_equation_format = self.polynomial_to_latex(coefficients_of_fitted_eqn)

            main_graph_axes = self.main_graph_figure.gca()
            main_graph_axes.cla()
            main_graph_axes.grid(True)
            main_graph_axes.set_facecolor((1, 1, 1))
            main_graph_axes.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            main_graph_axes.plot(self.time_value, amplitude_fitted_values, "r--",
                      label=f"Fitted Signal with polynomial of degree { self.degree_of_polynomial_of_one_main_chunk }.")
            main_graph_axes.set_xlabel("Time Value")
            main_graph_axes.set_ylabel("Amplitude Value")
            main_graph_axes.set_title("BioSignal")
            main_graph_legend = main_graph_axes.legend(loc="lower center")
            red_patch_for_equation_latex = mpatches.Patch(color='red', label=latex_equation_format)
            main_graph_legend_2 = main_graph_axes.legend(handles=[red_patch_for_equation_latex], loc="upper center")
            main_graph_axes.add_artist(main_graph_legend)
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
        except Exception as e:
            print(e)

    def chunks_divider(self):
        try:
            self.full_signal_array_divided = []
            # self.time_array_signal_divided = []
            self.latex_equations_for_each_chunk = {}
            length_of_data = len(self.time_value)
            self.set_combo_box_items_for_multiple_chunks()
            for i in range(self.number_of_chunks):
                start = int((i * length_of_data / self.number_of_chunks))
                end = int(((i + 1) * length_of_data / self.number_of_chunks))
                coefficients = np.around(np.polyfit(self.time_value[start: end], self.amplitude_value[start: end],
                                   self.degree_of_polynomial), 2)
                fitted_data = np.polyval(coefficients, self.time_value[start:end])
                latex_equation = self.polynomial_to_latex(coefficients)
                self.latex_equations_for_each_chunk[f"{i+1}"] = latex_equation
                self.full_signal_array_divided.extend(fitted_data)
        except Exception as e:
            print(e)

    def plot_data_splitted_with_chunks(self):
        try:
            self.chunks_divider()
            main_graph_axes = self.main_graph_figure.gca()
            main_graph_axes.cla()
            main_graph_axes.grid(True)
            main_graph_axes.set_facecolor((1, 1, 1))
            main_graph_axes.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            main_graph_axes.plot(self.time_value, self.full_signal_array_divided, "r--",
                      label=f"Fitted Signal with {self.number_of_chunks} Chunks and polynomial of degree {self.degree_of_polynomial}.")
            main_graph_axes.legend(loc="best")
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
                if index_value == 1:
                    # A special care needs to be addressed to put the exponent in {..} in LaTeX
                    full_equation_string += "x^{i}".format(i=index)
                elif index_value > 0:
                    full_equation_string += "{a}x^{i}".format(a=index_value, i=index)
                elif index_value < 0:
                    full_equation_string += "({a})x^{i}".format(a=index_value, i=index)
                if index != (len(list_of_coefficients) - 1):
                    full_equation_string += " + "
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
        error_map_figure = self.error_map_figure.get_figure()
        error_map_figure.clear()
        error_ax = self.error_map_figure.gca()
        error_ax.cla()
        errormap_plot = plt.imshow(matrix)
        error_ax.imshow(matrix, origin = 'lower')
        error_ax.set_ylabel(y_label)
        error_ax.set_xlabel(x_label)
        error_ax.set_title("Error Map!")
        # error_ax.set_xticks([])
        # error_ax.set_yticks([])
        error_map_figure.colorbar(errormap_plot, ax=error_ax)
        error_map_figure.tight_layout()
        self.error_map_canvas.draw()
        self.error_map_canvas.flush_events()

    def reset(self):
        try:
            error_map_axes = self.error_map_figure.gca()
            error_map_axes.cla()
            main_graph_axes = self.main_graph_figure.gca()
            main_graph_axes.cla()
            self.time_value = 0
            self.amplitude_value = 0
            self.overlap_percentage = 0
            self.number_of_chunks = 0
            self.degree_of_polynomial = 0
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
            main_graph_axes = self.main_graph_figure.gca()
            main_graph_axes.cla()
            main_graph_axes.grid(True)
            main_graph_axes.set_facecolor((1, 1, 1))
            main_graph_axes.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            main_graph_axes.plot(self.time_value, self.full_signal_array_divided, "r--",
                      label=f"Fitted Signal with {self.number_of_chunks} Chunks and polynomial of degree {self.degree_of_polynomial}.")
            main_graph_legend = main_graph_axes.legend(loc="lower center")
            red_patch_for_equation_latex = mpatches.Patch(color='red', label=latex_equation)
            main_graph_legend_2 = main_graph_axes.legend(handles=[red_patch_for_equation_latex], loc="upper center")
            main_graph_axes.add_artist(main_graph_legend)
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
        except Exception as e:
            print(e)

    def clipping_signal_and_applying_extrapolation(self):
        try:
            amplitude_fitted_values_for_the_left_clip = []
            amplitude_fitted_values_for_the_right_clip = []
            full_signal = []
            max_y_value = max(self.amplitude_value) + 0.7
            min_y_value = min(self.amplitude_value) - 0.7
            clipped_percentage = self.extrapolation_percentage / 100
            length_of_data = len(self.time_value)
            end = int(clipped_percentage * length_of_data)

            coefficients_of_fitted_eqn = np.around(np.polyfit(self.time_value[0:end], self.amplitude_value[0:end],
                                                    self.degree_of_polynomial_of_one_main_chunk), 2)
            # Coefficients from higher power
            amplitude_fitted_values_for_the_left_clip = np.polyval(coefficients_of_fitted_eqn, self.time_value[0:end])
            # Represent the extrapolation part:
            full_signal.extend(amplitude_fitted_values_for_the_left_clip)

            amplitude_fitted_values_for_the_right_clip = np.polyval(coefficients_of_fitted_eqn,
                                                                    self.time_value[end:length_of_data])

            for index in range(len(amplitude_fitted_values_for_the_right_clip)):
                if amplitude_fitted_values_for_the_right_clip[index] > max_y_value:
                    indices = range(index, len(amplitude_fitted_values_for_the_right_clip))
                    amplitude_fitted_values_for_the_right_clip = np.delete(amplitude_fitted_values_for_the_right_clip, indices)
                    break
                elif amplitude_fitted_values_for_the_right_clip[index] < min_y_value:
                    indices = range(index, len(amplitude_fitted_values_for_the_right_clip))
                    amplitude_fitted_values_for_the_right_clip = np.delete(amplitude_fitted_values_for_the_right_clip, indices)
                    break

            full_signal.extend(amplitude_fitted_values_for_the_right_clip)

            latex_equation = self.polynomial_to_latex(coefficients_of_fitted_eqn)

            main_graph_axes = self.main_graph_figure.gca()
            main_graph_axes.cla()
            main_graph_axes.grid(True)
            main_graph_axes.set_facecolor((1, 1, 1))
            main_graph_axes.plot(self.time_value, self.amplitude_value, "b", label="Original Signal")
            main_graph_axes.plot(self.time_value[0:len(full_signal)], full_signal, "r--",
                      label="Signal With Extrapolation.")
            # line shows the location of extrapolation
            main_graph_axes.axvline(x=self.time_value[end], color='orange', linestyle='--')
            red_patch_for_equation_latex = mpatches.Patch(color='red', label="latex Equation of fitted part:"+latex_equation)
            main_graph_legend_2 = main_graph_axes.legend(handles=[red_patch_for_equation_latex], loc="best")
            self.main_graph_canvas.draw()
            self.main_graph_canvas.flush_events()
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

    def calculate_error_percentage(self, original, fitted):
        sum_of_differences = 0
        original_sum = 0
        for i in range(len(original)):
            sum_of_differences += abs(fitted[i] - original[i])
            original_sum += abs(original[i])

        error_percentage =(sum_of_differences / original_sum) * 100
        return error_percentage

    def error_map_with_no_overlap(self):
        try:
            progress_bar_value = 0
            time_overall_data = []
            chunks_overall_data = []
            self.full_matrix_error_map = []
            x_axis_element = self.ui.comboBox.currentIndex()
            y_axis_element = self.ui.comboBox_2.currentIndex()
            time_overall_data, chunks_overall_data = self.chunks_divider_for_error_map()

            if x_axis_element == 1:
                if y_axis_element == 1:
                    # Number Of Chunks is on Y_axis, Polynomial Degree is on X-axis, overlap_percentage remains constant:
                    for chunk_number in range(0, self.number_of_chunks):
                        chunk_data = chunks_overall_data[chunk_number]
                        time_data = time_overall_data[chunk_number]
                        self.row_of_error_map = []
                        for degree in range(1, self.degree_of_polynomial + 1):
                            coefficients_of_fitted_eqn = np.around(np.polyfit(time_data, chunk_data,
                                                                              degree), 2)
                            amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
                            error_percentage = round(self.calculate_error_percentage(chunk_data, amplitude_fitted_values),
                                                     4)
                            self.row_of_error_map.append(error_percentage)

                        progress_bar_value += chunk_number * 5
                        self.ui.progressBar.setValue(progress_bar_value)
                        self.full_matrix_error_map.append(self.row_of_error_map)
                    # Plotting the Error Map:
                    # self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
                    self.plot_error_map(self.full_matrix_error_map, "Polynomial Degree", "Number Of Chunks")
                    self.ui.progressBar.setValue(100)

            elif x_axis_element == 0:
                if y_axis_element == 0:
                    # Number Of Chunks is on X_axis, Polynomial Degree is on Y-axis, overlap_percentage is constant:
                    for degree in range(1, self.degree_of_polynomial + 1):
                        self.row_of_error_map = []
                        for chunk_number in range(0, self.number_of_chunks):
                            chunk_data = chunks_overall_data[chunk_number]
                            time_data = time_overall_data[chunk_number]
                            coefficients_of_fitted_eqn = np.around(np.polyfit(time_data, chunk_data,
                                                                              degree), 2)
                            amplitude_fitted_values = np.polyval(coefficients_of_fitted_eqn, time_data)
                            error_percentage = round(
                                self.calculate_error_percentage(chunk_data, amplitude_fitted_values), 4)
                            self.row_of_error_map.append(error_percentage)
                        progress_bar_value += degree * 5
                        self.ui.progressBar.setValue(progress_bar_value)
                        self.full_matrix_error_map.append(self.row_of_error_map)
                    # Plotting the Error Map:
                    # self.full_matrix_error_map = np.flip(self.full_matrix_error_map, 0)
                    self.plot_error_map(self.full_matrix_error_map, "Number Of Chunks", "Polynomial Degree")
                    self.ui.progressBar.setValue(100)

        except Exception as e:
            print(e)

    def chunks_divider_for_error_map(self):
        try:
            amplitude_signal_array_divided = []
            time_array_signal_divided = []
            length_of_data = len(self.time_value)
            for i in range(self.number_of_chunks):
                start = int((i * length_of_data / self.number_of_chunks))
                end = int(((i + 1) * length_of_data / self.number_of_chunks))
                time_array_signal_divided.append(self.time_value[start:end])
                amplitude_signal_array_divided.append(self.amplitude_value[start:end])
            return time_array_signal_divided, amplitude_signal_array_divided
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Curve Fitting and Interpolation")
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

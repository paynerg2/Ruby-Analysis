# Libraries
from pylab import *
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# from lmfit import minimize, Parameters


# Helper Functions


def read_time_counts(file_name):
    """
    :param file_name: String
    :return: List of the first and second column in the file, which correspond to time and counts, values
    converted to floats.
    """
    time_column = [x.split(' ')[0] for x in open(file_name).readlines()]
    counts_column = [x.split(' ')[1].replace('\n', '') for x in open(file_name).readlines()]
    time = [float(i) for i in time_column]
    counts = [float(i) for i in counts_column]
    return [time, counts]


def get_file_information(file_name):
    """
    :param file_name: String
    :return: Returns [LED Wavelength, Ruby Thickness in mm, Monochromator Wavelength an A, up/down, date(mm/dd)]
    """
    return file_name.split('-')


def add_to_ruby_dictionary(d, file_info, ruby_dict):
    """
    :param d: List
    [time, counts] for a given monochromator wavelength. Where time and counts are both lists of floats.
    :param file_info: List
    Expects a list in the form [LED Wavelength, Ruby Thickness, Monochromator Wavelength, up/down, date(mm/dd)]
    where each entry is a string.
    :return: None. Modifies the dictionary in place.
    """
    led = file_info[0]
    thickness = file_info[1]
    wavelength = file_info[2]
    direction = file_info[3]

    if led not in ruby_dict:
        ruby_dict[led] = {}
    if thickness not in ruby_dict[led]:
        ruby_dict[led][thickness] = {}
    if direction not in ruby_dict[led][thickness]:
        ruby_dict[led][thickness][direction] = {}

    ruby_dict[led][thickness][direction][wavelength] = d


def build_ruby_dictionary(directory, ruby_dict):
    """
    Takes all .asc files in the current working directory and creates a dictionary structure containing all of the
    relevant Ruby data with each of the relevant parameters as keys.
    :return: None
    """
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_path = f'{directory}/{filename}'
        if filename.endswith(".txt"):
            data = read_time_counts(file_path)
            file_information = get_file_information(filename)
            add_to_ruby_dictionary(data, file_information, ruby_dict)


# def make_thickness_plots():
#     """
#     Makes a plot for each ruby thickness. Plots counts vs. time for each of the associated Monochromator wavelengths.
#     Labels each plot with the ruby thickness, and provides a legend to discern each wavelength.
#     :return: None.
#     """
#     for led, thickness in ruby_dict.items():
#         for thickness, wavelength in thickness.items():
#             for wavelength, direction in wavelength.items():
#                 for key in direction:
#                     # Add plot attributes here
#                     plot(direction[key][0], direction[key][1], label=f"{key}")
#                 xlabel('Time(s)')
#                 ylabel('Counts')
#                 legend(loc="best", prop={'size': 10})
#                 title(f"{thickness} Ruby Response")
#                 savefig(f"{thickness}-RubyResponse")
#                 show()


# def single_exponential_residual(params, x, data, eps_data):
#     """
#     :param params: lmfit Parameter object, should contain parameters which match the model being used.
#     :param x: x-axis array
#     :param data: y-axis array
#     :param eps_data: weighting array
#     :return: returns the weighted residual between the data and the model to be minimized by lmfit
#     """
#     amp = params['amp']
#     freq = params['freq']
#     offset = params['offset']
#     model = amp * exp(freq * x) + offset
#     return (data - model) / eps_data
#
#
# def double_exponential_residual(params, x, data, eps_data):
#     """
#     :param params: lmfit Parameter object, should contain parameters which match the model being used.
#     :param x: x-axis array
#     :param data: y-axis array
#     :param eps_data: weighting array
#     :return: returns the weighted residual between the data and the model to be minimized by lmfit
#     """
#     amp = params['amp']
#     amp2 = params['amp2']
#     freq = params['freq']
#     freq2 = params['freq2']
#     offset = params['offset']
#     model = amp * exp(freq * x) + amp2 * exp(freq2 * x) + offset
#     return (data - model) / eps_data


def index_after_pulse(count):
    """
    Returns the start index for usable data in the array of counts. This should be after the pulse
    has subsided entirely.
    :param count: array
    :return: index at which to start the analysis. Expect int.
    """
    for i in range(1, len(count)):
        if abs(count[i] - count[i-1]) > 1000:
            # +3 to ensure that the starting point is after the pulse has subsided
            return i + 3


# def create_fit_lines(time_data, count_data):
#     """
#     :param time_data: x-axis data from Easy-MCS. Expects array.
#     :param count_data: y-axis data from Easy-MCS. Expects array.
#     :return: out, out2 objects from lmfit. Contains all of the information about the curve fit.
#     """
#     eps_data = 1/count_data
#     out = minimize(single_exponential_residual, params, args=(time_data, count_data, eps_data))
#     out2 = minimize(double_exponential_residual, params, args=(time_data, count_data, eps_data))
#     return out, out2
#
#
# def plot_fit(out, num):
#     """
#     :param num: Number of exponential terms to include. Expects either 1 or 2 as int.
#     :param out: out object from lmfit. Contains all of the information about the
#     curve fit. We use the params object, which contains all of the fit parameters.
#     :return:
#     """
#     a = out.params['amp'].value
#     b = out.params['freq'].value
#     c = out.params['offset'].value
#     if num == 1:
#         plot(time_data, single_exponential_fit_func(time_data, a, b, c), '-', label="Fit")
#     elif num == 2:
#         d = out.params['amp2'].value
#         e = out.params['freq2'].value
#         plot(time_data, double_exponential_fit_func(x, a, b, c, d, e), '-', label="Fit")
#     else:
#         pass
#         # Stub for error handling


def extract_data(wavelength):
    """
    :param wavelength: Dictionary containing specific wavelengths as keys-value pairs
    with the individual Easy-MCS datasets.
    :return: x-axis and y-axis data in the form of arrays.
    """
    for key in wavelength:
        start_index = index_after_pulse(wavelength[key][1])
        time_data = array(wavelength[key][0][start_index:])
        count_data = array(wavelength[key][1][start_index:])
        return time_data, count_data


def plot_data(x, y):
    """
    Takes x-axis and y-axis data and plots with labels and legend.
    :param x: Array
    :param y: Array
    :return: None
    """
    plot(x, y, 'o', label="Data")
    xlabel('Time(s)')
    ylabel('Counts')
    legend(loc="best", prop={'size': 10})


# def make_fit_plots():
#     """
#     Creates plots for each set of wavelength data and adds a fit line to it
#     Does this for both the single and double exponential fit models.
#     :return: None
#     """
#     for led, thickness in ruby_dict.items():
#         for thickness, wavelength in thickness.items():
#             for wavelength, direction in wavelength.items():
#                 for key in direction:
#                     time_data, count_data = extract_data(direction)
#                     out, out2 = create_fit_lines(time_data, count_data)
#
#                     # Create plot for single exponential fit.
#                     plot_data(time_data, count_data)
#                     plot_fit(out, 1)
#                     plot_id = f"{thickness} Ruby Response for {led_wavelength}nm LED and {key} Monochromator Pulse"
#                     title(plot_id)
#                     legend(['Data', 'Single Exp Fit'])
#                     savefig(plot_id)
#                     show()
#
#                     # Create plot for double exponential fit.
#                     plot_data(time_data, count_data)
#                     plot_fit(out2, 2)
#                     plot_id = f"{thickness} Ruby Response for {led_wavelength}nm LED and {key} Monochromator Pulse"
#                     title(plot_id)
#                     legend(['Data', 'Double Exp Fit'])
#                     savefig(plot_id)
#                     show()


def single_exponential_fit_func(x, a, b, c):
    return a * np.exp(b * x) + c


def double_exponential_fit_func(x, a, b, c, d, e):
    return a * np.exp(b * x) + c * np.exp(d * x) + e


# def create_parameters():
#     """
#     Creates the Parameters object for lmfit containing all of the fit params and
#     initial values
#     :return: Parameter object
#     """
#     parameters = Parameters()
#     parameters.add('amp', value=100)
#     parameters.add('freq', value=0.001)
#     parameters.add('offset', value=200)
#     parameters.add('amp2', value=100)
#     parameters.add('freq2', value=0.001)
#     return parameters


# # Run the script
# if __name__ == '__main__':
#
#     # Initialize necessary data structures
#     # ruby_dict = {}
#     thickness_data = {}
#     wavelength_data = {}
#     time_data = {}
#     # params = create_parameters()
#
#     container_directory = os.getcwd()
#     for entry in os.listdir(container_directory):
#         if os.path.isdir(entry):
#             build_ruby_dictionary(entry)
#     # make_thickness_plots()
#     # make_fit_plots()


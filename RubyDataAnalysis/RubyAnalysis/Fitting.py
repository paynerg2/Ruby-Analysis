import numpy as np
from lmfit import Parameters, minimize


def single_exponential(x, a, b, c):
    return a * np.exp(b * x) + c


def double_exponential(x, a, b, c, d, e):
    return a * np.exp(b * x) + c * np.exp(d * x) + e


def create_parameters():
    """
    Creates the Parameters object for lmfit containing all of the fit params and
    initial values
    :return: Parameter object
    """
    parameters = Parameters()
    parameters.add('amp', value=100)
    parameters.add('freq', value=0.001)
    parameters.add('offset', value=200)
    parameters.add('amp2', value=100)
    parameters.add('freq2', value=0.001)
    return parameters


def single_exponential_residual(parameters, x, data, eps_data):
    """
    :param parameters: lmfit Parameter object, should contain parameters which match the model being used.
    :param x: x-axis array
    :param data: y-axis array
    :param eps_data: weighting array
    :return: returns the weighted residual between the data and the model to be minimized by lmfit
    """
    amp = parameters['amp']
    freq = parameters['freq']
    offset = parameters['offset']
    model = amp * np.exp(freq * x) + offset
    return (data - model) / eps_data


def double_exponential_residual(parameters, x, data, eps_data):
    """
    :param parameters: lmfit Parameter object, should contain parameters which match the model being used.
    :param x: x-axis array
    :param data: y-axis array
    :param eps_data: weighting array
    :return: returns the weighted residual between the data and the model to be minimized by lmfit
    """
    amp = parameters['amp']
    amp2 = parameters['amp2']
    freq = parameters['freq']
    freq2 = parameters['freq2']
    offset = parameters['offset']
    model = amp * np.exp(freq * x) + amp2 * np.exp(freq2 * x) + offset
    return (data - model) / eps_data


def create_fit_lines(time_data, count_data, parameters):
    """
    :param parameters:
    :param time_data: x-axis data from Easy-MCS. Expects array.
    :param count_data: y-axis data from Easy-MCS. Expects array.
    :return: out, out2 objects from lmfit. Contains all of the information about the curve fit.
    """
    eps_data = 1/count_data
    out = minimize(single_exponential_residual, parameters, args=(time_data, count_data, eps_data))
    out2 = minimize(double_exponential_residual, parameters, args=(time_data, count_data, eps_data))
    return out, out2


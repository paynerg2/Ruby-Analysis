import numpy as np
from RubyAnalysis import Fitting, Plotting


# TODO: np.std() returns 0.00 - create custom standard deviation function
# TODO: Also want Chi-squared values.
def calculate(decay_values):
    decay_array = np.array(decay_values)
    decay_average = average_reasonable_values(decay_array)
    decay_standard_deviation = np.std(decay_array)
    print(decay_array)
    return [decay_average, decay_standard_deviation]


def average_reasonable_values(array):
    # Some fits produce wildly incorrect slope values, which
    # are excluded from the average
    accumulator = 0
    exclusions = 0
    for x in array:
        if -1 < x < 0:
            accumulator += x
        else:
            exclusions += 1
    if len(array) == exclusions:
        return 0
    else:
        return accumulator / (len(array) - exclusions)


def retrieve_averages(decay_statistics):
    return [x[0] for x in decay_statistics.values() if -1 < x[0] < -0.1]


def get_thickness_key_values(dictionary):
    return [int(x.replace('mm', '')) for x in list(dictionary.keys())]


def get_slope_values(dictionary):
    return [x[0] for x in list(dictionary.values())]


def get(ruby_dict):
    parameters = Fitting.create_parameters()
    decay_statistics = {}
    for led, thickness_data in ruby_dict.items():
        for thickness_value, wavelength_data in thickness_data.items():
            decay_values = []
            for direction, data in wavelength_data.items():
                for wavelength in data:
                    time_data, count_data = Plotting.extract_data(data)
                    out, out2 = Fitting.create_fit_lines(time_data, count_data, parameters)
                    decay_values.append(out.params['freq'].value)
            decay_statistics[thickness_value] = calculate(decay_values)

    return decay_statistics


def match_data_sets(x_values, y_values):
    zero_indexes = [i for i, x in enumerate(y_values) if x == 0]
    # Reversed so that deleting indices doesn't mess with indexing in the loop
    for i in sorted(zero_indexes, reverse=True):
        del x_values[i]
        del y_values[i]
    return x_values, y_values

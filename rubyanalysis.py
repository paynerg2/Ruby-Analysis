# Libraries
from pylab import *

# Helper Functions
def read_time_counts(file_name):
    """
    :param file_name: String
    :return: List of the first and second column in the file, which correspond to time and counts, values
    converted to floats.
    """
    time_column = [x.split(' ')[0] for x in open(file_name).readlines()]
    counts_column = [x.split(' ')[1].replace('\n','') for x in open(file_name).readlines()]
    time = [float(i) for i in time_column]
    counts = [float(i) for i in counts_column]
    return [time,counts]

def get_file_information(file_name):
    """
    :param file_name: String
    :return: Returns [LED Wavelength, Ruby Thickness in mm, Monochromator Wavelength an A, up/down, date(mm/dd)]
    """
    return file_name.split('-')


def add_to_ruby_dictionary(d, file_info):
    """
    :param d: List
    [time, counts] for a given monochromator wavelength. Where time and counts are both lists of floats.
    :param file_info: List
    Expects a list in the form [LED Wavelength, Ruby Thickness, Monochromator Wavelength, up/down, date(mm/dd)]
    where each entry is a string.
    :return: None. Modifies the dictionary in place.
    """
    wavelength_data[file_info[2]] = d

    if file_info[1] in thickness_data:
        thickness_data[file_info[1]].update(wavelength_data)
    else:
        thickness_data[file_info[1]] = wavelength_data

    if file_info[0] in ruby_dict:
        ruby_dict[file_info[0]].update(thickness_data)
    else:
        ruby_dict[file_info[0]] = thickness_data

def build_ruby_dictionary():
    """
    Takes all .asc files in the current working directory and creates a dictionary structure containing all of the
    relevant Ruby data with each of the relevant parameters as keys.
    :return: None
    """
    directory = os.getcwd()
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            data = read_time_counts(filename)
            file_information = get_file_information(filename)
            add_to_ruby_dictionary(data, file_information)

def plot_data():
    """
    Makes a plot for each ruby thickness. Plots counts vs. time for each of the associated Monochromator wavelengths.
    Labels each plot with the ruby thickness, and provides a legend to discern each wavelength.
    :return: None.
    """
    for led, thickness in ruby_dict.items():
        for thickness, wavelength in thickness.items():
            for key in wavelength:
                print(thickness, key)
                # Add plot attributes here
                plot(wavelength[key][0], wavelength[key][1], label=f"{key}")
            xlabel('Time(s)')
            ylabel('Counts')
            legend(loc="best", prop={'size': 10})
            title(f"{thickness} Ruby Response")
            savefig(f"{thickness}-RubyResponse")
            show()


# Run the script
if __name__ == '__main__':

    # Initialize necessary data structures
    # TODO: Refactor such that this is unnecessary by separating out each of the dictionary building operations.
    ruby_dict = {}
    thickness_data = {}
    wavelength_data = {}

    build_ruby_dictionary()
    plot_data()

    # TODO: Set the program up to be able to iterate through an entire folder of directories containing Ruby data sets.
    # TODO: For each wavelength data-set, perform a weighted non-linear least squares regression with
    #       two different functions. Plot fit-line on graphs & snag the reduced Chi-squared

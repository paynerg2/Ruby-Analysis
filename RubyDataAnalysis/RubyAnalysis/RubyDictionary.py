import os


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


def build(directory, ruby_dict):
    """
    Takes all .asc files in the current working directory and creates a dictionary structure containing all of the
    relevant Ruby data with each of the relevant parameters as keys.
    :return: None
    """
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_path = f'{directory}/{filename}'
        if filename.endswith(".txt") and filename[:3] == "LED":
            data = read_time_counts(file_path)
            file_information = get_file_information(filename)
            add_to_ruby_dictionary(data, file_information, ruby_dict)
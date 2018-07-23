from pylab import *
from RubyAnalysis import Fitting, FitStatistics

# ===========================================
#       Thickness Plot Methods
# ===========================================


def make_thickness_plots(ruby_dict, save_directory):
    """
    Makes a plot for each ruby thickness. Plots counts vs. time for each of the associated Monochromator wavelengths.
    Labels each plot with the ruby thickness, and provides a legend to discern each wavelength.
    :return: None.
    """

    for led, thickness_data in ruby_dict.items():
        led_wavelength = led.replace("LED", '')
        for thickness_value, wavelength_data in thickness_data.items():
            for direction, data in wavelength_data.items():
                for wavelength in data:
                    # Add plot attributes here
                    time_data = data[wavelength][0]
                    counts = data[wavelength][1]
                    plot(time_data, counts, label=f"{wavelength}")
                xlabel('Time(s)')
                ylabel('Counts')
                legend(loc="best", prop={'size': 10})
                plot_title = f"{thickness_value} Ruby Response for {led_wavelength}nm LED {direction}"
                title(plot_title)
                savefig(f'{save_directory}/{plot_title}')
                clf()
                print(f"plot created : {plot_title}")
    print("All plots created")
# ===========================================
#           Fit Plot Methods
# ===========================================


def make_fit_plots(ruby_dict, save_directory):
    """
    Creates plots for each set of wavelength data and adds a fit line to it
    Does this for both the single and double exponential fit models.
    :return: None
    """
    parameters = Fitting.create_parameters()
    for led, thickness_data in ruby_dict.items():
        led_wavelength = led.replace("LED", '')
        decay_statistics = {}
        for thickness_value, wavelength_data in thickness_data.items():
            decay_values = []
            for direction, data in wavelength_data.items():
                for wavelength in data:
                    time_data, count_data = extract_data(data)
                    out, out2 = Fitting.create_fit_lines(time_data, count_data, parameters)
                    decay_values.append(out.params['freq'].value)

                    # Create plot for single exponential fit.
                    plot_data(time_data, count_data)
                    plot_fit(out, 1, time_data)
                    plot_title = f"{thickness_value} Ruby Response for {led_wavelength}nm LED {wavelength} Pulse"
                    title(plot_title)
                    legend(['Data', 'Single Exp Fit'])
                    savefig(f'{save_directory}/{plot_title}.png')
                    clf()
                    print(f'plot created : {plot_title}')

                    # TODO: Get double exponential fit working
                    # # Create plot for double exponential fit.
                    # plot_data(time_data, count_data)
                    # plot_fit(out2, 2, time_data)
                    # plot_title = f"{thickness_value} Ruby Response for {led_wavelength}nm LED {wavelength} Pulse"
                    # title(plot_title)
                    # legend(['Data', 'Double Exp Fit'])
                    # savefig(f'{save_directory}/{plot_title}.png')
            decay_statistics[thickness_value] = FitStatistics.calculate(decay_values)
        print(decay_statistics)
    clf()
    print("All plots created")


def plot_fit(out, num, time_data):
    """
    :param time_data:
    :param num: Number of exponential terms to include. Expects either 1 or 2 as int.
    :param out: out object from lmfit. Contains all of the information about the
    curve fit. We use the params object, which contains all of the fit parameters.
    :return:
    """
    a = out.params['amp'].value
    b = out.params['freq'].value
    c = out.params['offset'].value
    if num == 1:
        plot(time_data, Fitting.single_exponential(time_data, a, b, c), '-', label="Fit")
    elif num == 2:
        d = out.params['amp2'].value
        # Alphabet is hard - something about shadowing a name from an outer scope, so g replaces e
        g = out.params['freq2'].value
        plot(time_data, Fitting.double_exponential(time_data, a, b, c, d, g), '-', label="Fit")
    else:
        pass
        # Stub for error handling


def find_index_after_pulse(count):
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


def extract_data(data_set):
    """
    :param data_set: Dictionary containing specific wavelengths as keys-value pairs
    with the individual Easy-MCS datasets.
    :return: x-axis and y-axis data in the form of arrays.
    """
    for wavelength in data_set:
        start_index = find_index_after_pulse(data_set[wavelength][1])
        time_data = array(data_set[wavelength][0][start_index:])
        count_data = array(data_set[wavelength][1][start_index:])
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


# ===========================================
#           Slope Plot Methods
# ===========================================

# TODO: Add error bars to the plots.
def make_slope_plots(ruby_dict, save_directory):
    print("Creating plot...")
    print("This one takes a while...")
    fit_statistics = FitStatistics.get(ruby_dict)
    thickness_values = FitStatistics.get_thickness_key_values(fit_statistics)
    slope_values = FitStatistics.get_slope_values(fit_statistics)
    # Remove the any 0's in from both arrays
    thickness_values, slope_values = FitStatistics.match_data_sets(thickness_values, slope_values)
    plot(thickness_values, slope_values, 'o')
    xlabel('Thickness(mm)')
    ylabel('Decay Constant (1/s)')
    plot_title = "Average Decay Values for Given Ruby Thickness"
    title(plot_title)
    savefig(f'{save_directory}/{plot_title}')
    clf()
    print(f"plot created : {plot_title}")

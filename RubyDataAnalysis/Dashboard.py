# ===========================================
#           Libraries
# ===========================================
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

# ===========================================
#           Custom Modules
# ===========================================
from RubyAnalysis import RubyDictionary, Plotting


# ===========================================
#           UI Initialization
# ===========================================


root = Tk()
root.title('Ruby Data Analysis')
for x in range(4):
    Grid.columnconfigure(root, x, weight=1)

for y in range(4):
    Grid.rowconfigure(root, y, weight=1)


# ===========================================
#               Globals
# ===========================================
ruby_dict = {}
folder_path = StringVar()
save_directory = None


# ===========================================
#               Callback Functions
# ===========================================


def change_icon(label, icon):
    clear_import_label()
    label.configure(image=icon)
    label.image = icon


def clear_import_label():
    import_success_label['text'] = ""


def browse_button_click():
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    folder_text.insert(END, filename)
    folder_text.see(END)

    if filename != "":
        import_button['state'] = 'normal'

    return filename


def import_button_click():
    old_data = dict(ruby_dict)
    directory = folder_path.get()

    RubyDictionary.build(directory, ruby_dict)
    check_import_status(old_data, ruby_dict)
    old_data.clear()

    set_plot_button_state()
    reset_plot_icons()


def check_save_directory():
    global save_directory
    if save_directory is None or save_directory == "":
        save_directory = filedialog.askdirectory()
    return save_directory


def create_thickness_plots():
    global save_directory
    save_directory = check_save_directory()
    if save_directory != "":
        Plotting.make_thickness_plots(ruby_dict, save_directory)
        change_icon(create_plot_icon, success_icon)


def create_fit_plots():
    global save_directory
    save_directory = check_save_directory()
    if save_directory != "":
        Plotting.make_fit_plots(ruby_dict, save_directory)
        change_icon(fit_plot_icon, success_icon)


def create_slope_plots():
    global save_directory
    save_directory = check_save_directory()
    if save_directory != "":
        Plotting.make_slope_plots(ruby_dict, save_directory)
        change_icon(slope_plot_icon, success_icon)


def set_plot_button_state():
    if ruby_dict != {}:
        plot_button['state'] = 'normal'
        fit_button['state'] = 'normal'
        slope_button['state'] = 'normal'


def check_import_status(old_data, new_data):
    # TODO: Bug: if the keys of the dictionaries are equal, it thinks nothing has changed - fix this conditional
    if old_data != new_data:
        import_success_label['text'] = "Data successfully imported"
        import_success_label['fg'] = '#6AC259'
    else:
        import_success_label['text'] = "Data not successfully imported"
        import_success_label['fg'] = '#B33A3A'


def reset_plot_icons():
    change_icon(create_plot_icon, incomplete_icon)
    change_icon(fit_plot_icon, incomplete_icon)
    change_icon(slope_plot_icon, incomplete_icon)


# ===========================================
#           Folder Text Widget
# ===========================================
folder_text = Text(root, height=1, width=30)
folder_text.grid(row=0, column=0, pady=10, padx=(35, 0))

# ===========================================
#           Folder Browse Button
# ===========================================
folder_button = Button(text="Browse", command=browse_button_click, state=ACTIVE)
folder_button.grid(row=0, column=1, padx=(0, 10))

# ===========================================
#           Import Data Button
# ===========================================
import_button = Button(text="Import", command=import_button_click, state=DISABLED)
import_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky=W)

ttk.Separator(root, orient='horizontal').grid(row=3, column=0, columnspan=4, sticky='EW', padx=10)

# ===========================================
#           Import Success Message Label
# ===========================================
import_success_label = Label(text="")
import_success_label.grid(row=1, column=0, padx=(60, 0), pady=(0, 10), sticky=W)

# ===========================================
#           Create Plots Button
# ===========================================
plot_button = Button(text="Create Thickness Plots", command=create_thickness_plots, state=DISABLED)
plot_button.grid(row=4, column=0, padx=10, pady=(10, 0), sticky=N+S+E+W)

# ===========================================
#           Create Fits Button
# ===========================================
fit_button = Button(text="Create Fit Plots", state=DISABLED, command=create_fit_plots)
fit_button.grid(row=5, column=0, padx=10, sticky=N+S+E+W)

# ===========================================
#           Create Slope Plot Button
# ===========================================
slope_button = Button(text="Create Slope Plots", state=DISABLED, command=create_slope_plots)
slope_button.grid(row=6, column=0, padx=10, pady=(0, 10), sticky=N+S+E+W)

# ===========================================
#               Icons
# ===========================================
folder_icon = PhotoImage(file="./Assets/user-blue-home-icon.png")

incomplete_icon = PhotoImage(file="./Assets/checked-concrete.png")
incomplete_icon = incomplete_icon.zoom(1, 1)
success_icon = PhotoImage(file="./Assets/checked.png")
success_icon = success_icon.zoom(1, 1)

folder_browser_icon = Label(root, image=folder_icon, height=24, width=24)
folder_browser_icon.grid(row=0, column=0, padx=(10, 0), sticky=W)

create_plot_icon = Label(root, image=incomplete_icon, height=20, width=20)
create_plot_icon.grid(row=4, column=1, pady=(10, 0), sticky=W)

fit_plot_icon = Label(root, image=incomplete_icon, height=20, width=20)
fit_plot_icon.grid(row=5, column=1, sticky=W)

slope_plot_icon = Label(root, image=incomplete_icon, height=20, width=20)
slope_plot_icon.grid(row=6, column=1, pady=(0, 10), sticky=W)


mainloop()

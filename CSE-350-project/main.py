import threading
import pytz
import csv
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedTk
import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Create a Tkinter window
window = ThemedTk(theme='adapta')
window.configure(bg='white')
window.geometry('1280x720')
window.title('OneADay')

# Custom TTK Styling (ttkstyle)
window.style = ttk.Style(window)
window.style.configure('TLabel', font=('Roboto', 11))
window.style.configure('TButton', font=('Helvetica', 13))
window.style.configure('TFrame', font=('Roboto', 20))
window.attributes("-fullscreen", True)
window.bind("<F11>", lambda event: window.attributes("-fullscreen", not window.attributes("-fullscreen")))
window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

# Create TabController To Add Tabs to
tabControl = ttk.Notebook(window)

# Create Tabs as Frames and add them to TabController
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Graphs 1')
tabControl.add(tab2, text='Graphs 2')
tabControl.pack(expand=True, fill="both")

# Globals
df = None
start_time = None
end_time = None

#-------------------------------------------------------------------GRAPH 1 TAB 1--------------------------------------------------------------------------#
#INIT TAB1 COMPONENTS -------------------------------------------------------------------------------------------------------------------------------------#
# Create a Matplotlib figure and axis
# figureTab1, axisTab1 = plt.subplots()
figureTab1 = Figure(figsize=(5, 4), dpi=100)
((axisTab1, axis1Tab1), (axis2Tab1, axis3Tab1)) = figureTab1.subplots(2,2)
figureTab1.subplots_adjust(left=0.055, bottom=0.09, right=0.979, top=0.92, wspace=0.145, hspace=0.236)
canvasTab1 = FigureCanvasTkAgg(figureTab1, master=tab1)# master='what tab you want the canvas to show on'

filledGraphsTab1 = 0
print("Filled Graphs Tab1 0:", filledGraphsTab1)

# toolbarTab1
toolbarTab1 = NavigationToolbar2Tk(canvasTab1, tab1)
toolbarTab1.update()
canvasTab1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
graphWidgetTab1 = canvasTab1.get_tk_widget()

#INIT TAB2 COMPONENTS------------------------------------------------------------------------------------------------------------------------------------#
figureTab2 = Figure(figsize=(5, 4), dpi=100)
((axisTab2, axis1Tab2), (axis2Tab2, axis3Tab2)) = figureTab2.subplots(2,2)
figureTab2.subplots_adjust(left=0.055, bottom=0.09, right=0.979, top=0.92, wspace=0.145, hspace=0.236)
canvasTab2 = FigureCanvasTkAgg(figureTab2, master=tab2)# master='what tab you want the canvas to show on'

filledGraphsTab2 = 0
print("Filled Graphs Tab2 0:", filledGraphsTab2)

# toolbarTab2
toolbarTab2 = NavigationToolbar2Tk(canvasTab2, tab2)
toolbarTab2.update()
canvasTab2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
graphWidgetTab2 = canvasTab2.get_tk_widget()


################### UTC/Local Machine Time ###################
x = 'Local Machine Time (M-D H)'
local_time = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

def time_slection():
    global x
    global local_time
    global start_time
    global end_time

    def on_utc():
        # nonlocal x
        global x
        x = 'Unix Timestamp (UTC) (M-D H)'
        root.quit()
        root.destroy()

    def on_local():
        # nonlocal x
        global x
        x = 'Local Machine Time (M-D H)'
        root.quit()
        root.destroy()

    root = tk.Tk()

    question_label = tk.Label(root, text="X Axis in UTC or Local Time?")
    question_label.pack()

    button_frame = tk.Frame(root)
    button_frame.pack()

    yes_button = tk.Button(button_frame, text="UTC", command=on_utc)
    yes_button.pack(side=tk.LEFT)

    no_button = tk.Button(button_frame, text="Local Time", command=on_local)
    no_button.pack(side=tk.LEFT)

    root.mainloop()

    def to_timestamp(value, index):
        x = df['Unix Timestamp (UTC)']
        return '{}'.format(x[index])
        # return '{}'.format(df['Unix Timestamp (UTC)'])
        # return '{}'.format(int(x))

    def to_local(value, index):
        x = df['Unix Timestamp (UTC)']
        return '{}'.format(pd.to_datetime(x[index], unit='ms').tz_localize(pytz.utc).astimezone(local_time).strftime('%m-%d %H'))
        # return '{}'.format(df['Unix Timestamp (UTC)'])
        # return '{}'.format(int(x))

    if(x == 'Unix Timestamp (UTC) (M-D H)'):
        axisTab1.xaxis.set_major_locator(ticker.AutoLocator())
        axisTab1.xaxis.set_major_formatter(plt.FuncFormatter(to_timestamp))
        axisTab1.set_xlabel("{}".format('Unix Timestamp (UTC) (M-D H)'))
        axis1Tab1.xaxis.set_major_locator(ticker.AutoLocator())
        axis1Tab1.xaxis.set_major_formatter(plt.FuncFormatter(to_timestamp))
        axis2Tab1.xaxis.set_major_locator(ticker.AutoLocator())
        axis2Tab1.xaxis.set_major_formatter(plt.FuncFormatter(to_timestamp))
        axis3Tab1.xaxis.set_major_locator(ticker.AutoLocator())
        axis3Tab1.xaxis.set_major_formatter(plt.FuncFormatter(to_timestamp))
        canvasTab1.draw()

        axisTab2.xaxis.set_major_locator(ticker.AutoLocator())
        axisTab2.xaxis.set_major_formatter(plt.FuncFormatter(to_timestamp))
        axisTab2.set_xlabel("{}".format('Unix Timestamp (UTC) (M-D H)'))
        axis1Tab2.xaxis.set_major_locator(ticker.AutoLocator())
        axis1Tab2.xaxis.set_major_formatter(plt.FuncFormatter(to_timestamp))
        axis2Tab2.xaxis.set_major_locator(ticker.AutoLocator())
        axis2Tab2.xaxis.set_major_formatter(plt.FuncFormatter(to_timestamp))
        axis3Tab2.xaxis.set_major_locator(ticker.AutoLocator())
        axis3Tab2.xaxis.set_major_formatter(plt.FuncFormatter(to_timestamp))
        canvasTab2.draw()
    else:
        x = 'Local Machine Time (M-D H)'
        axisTab1.xaxis.set_major_locator(ticker.AutoLocator())
        axisTab1.xaxis.set_major_formatter(plt.FuncFormatter(to_local))
        axisTab1.set_xlabel("{}".format('Local Machine Time (M-D H)'))
        axis1Tab1.xaxis.set_major_locator(ticker.AutoLocator())
        axis1Tab1.xaxis.set_major_formatter(plt.FuncFormatter(to_local))
        axis2Tab1.xaxis.set_major_locator(ticker.AutoLocator())
        axis2Tab1.xaxis.set_major_formatter(plt.FuncFormatter(to_local))
        axis3Tab1.xaxis.set_major_locator(ticker.AutoLocator())
        axis3Tab1.xaxis.set_major_formatter(plt.FuncFormatter(to_local))
        canvasTab1.draw()

        axisTab2.xaxis.set_major_locator(ticker.AutoLocator())
        axisTab2.xaxis.set_major_formatter(plt.FuncFormatter(to_local))
        axisTab2.set_xlabel("{}".format('Local Machine Time (M-D H)'))
        axis1Tab2.xaxis.set_major_locator(ticker.AutoLocator())
        axis1Tab2.xaxis.set_major_formatter(plt.FuncFormatter(to_local))
        axis2Tab2.xaxis.set_major_locator(ticker.AutoLocator())
        axis2Tab2.xaxis.set_major_formatter(plt.FuncFormatter(to_local))
        axis3Tab2.xaxis.set_major_locator(ticker.AutoLocator())
        axis3Tab2.xaxis.set_major_formatter(plt.FuncFormatter(to_local))
        canvasTab2.draw()
################### UTC/Local Machine Time ###################

# Choose import folder and graph it TAB1
def btn_importFolderTab1():
    global filledGraphsTab1

    excluded_widgets = [Tab1BtnFrame, Tab1importBtn, Tab1NewGraphBtn,
                        Tab1TimeBtn, figureTab1, canvasTab1, graphWidgetTab1, 
                        toolbarTab1]
    for widget in tab1.winfo_children():
        if(widget not in excluded_widgets):
            widget.destroy()
    axis1Tab1.clear()
    axis2Tab1.clear()
    axis3Tab1.clear()
    filledGraphsTab1 = 0

    global local_time
    global df
    global x
    global start_time
    global end_time
    # Create a file dialog
    # file_dialog = filedialog.askopen(title="Select a folder")
    import_dialog = filedialog.askdirectory(title="Select a folder")
    # Get the selected file
    selected_folder = import_dialog
    # Print the selected file
    print(selected_folder)

    # Import metadata
    print('Metadata:')
    fileMeta = selected_folder + '/metadata.csv'
    with open(fileMeta, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

    # Plot data
    print('Graph of summary: (opening in new window)')
    fileSum = selected_folder + '/summary.csv'
    # columns = ['Unix Timestamp (UTC)', 'Movement intensity']
    df = pd.read_csv(fileSum)
    columns = df.columns
    columns = [element for element in columns if element is not None]
    # df = pd.read_csv(fileSum, usecols=columns)
    axisTab1.clear()
    print("Columns: ", columns)

    ################### select y ###################
    def get_y(columns):
        def submit_selection():
            nonlocal y
            y = combo.get()
            root.quit()
            root.destroy()

        root = tk.Tk()

        y = None

        # title text
        title = tk.Label(root, text='Select Y axis')
        title.pack(pady=10)

        # combo box
        combo = tk.ttk.Combobox(root, values=columns)
        combo.current(0)
        combo.pack(pady=10)

        # Submit btn
        submit_btn = ttk.Button(root, text='Submit', command=submit_selection)
        submit_btn.pack()

        root.mainloop()

        return y
    y = get_y(columns)
    print(y)
    ################### select y ###################

    ################### select date/time range ###################
    timestamp_column = 'Unix Timestamp (UTC)'
    df['converted_timestamp'] = pd.to_datetime(
        df[timestamp_column], unit='ms').dt.tz_localize(pytz.utc).dt.tz_convert(local_time)
    start = None

    def get_start():
        global start_time
        global end_time

        def get_selected_datetime():
            nonlocal start
            year = year_picker.get()
            month = month_picker.get()
            day = day_picker.get()
            hour = hour_picker.get()
            minute = minute_picker.get()

            datetime_str = f"{year}-{month}-{day} {hour}:{minute}"
            start = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            root.quit()
            root.destroy()

        root = tk.Tk()
        root.title("Date and Time Picker")

        # min date and time
        default_datetime = df['converted_timestamp'].min()
        default_year = str(default_datetime.year)
        default_month = str(default_datetime.month).zfill(2)
        default_day = str(default_datetime.day).zfill(2)
        default_hour = str(default_datetime.hour).zfill(2)
        default_minute = str(default_datetime.minute).zfill(2)

        # year
        year_label = ttk.Label(root, text="Year (YYYY):")
        year_label.pack(pady=5)
        year_picker = ttk.Entry(root, width=10)
        year_picker.insert(0, default_year)
        year_picker.pack()

        # month
        month_label = ttk.Label(root, text="Month (MM):")
        month_label.pack(pady=5)
        month_picker = ttk.Entry(root, width=10)
        month_picker.insert(0, default_month)
        month_picker.pack()

        # day
        day_label = ttk.Label(root, text="Day (DD):")
        day_label.pack(pady=5)
        day_picker = ttk.Entry(root, width=10)
        day_picker.insert(0, default_day)
        day_picker.pack()

        # hour
        hour_label = ttk.Label(root, text="Hour (HH):")
        hour_label.pack(pady=5)
        hour_picker = ttk.Entry(root, width=10)
        hour_picker.insert(0, default_hour)
        hour_picker.pack()

        # minute
        minute_label = ttk.Label(root, text="Minute (MM):")
        minute_label.pack(pady=5)
        minute_picker = ttk.Entry(root, width=10)
        minute_picker.insert(0, default_minute)
        minute_picker.pack()

        # button
        select_button = ttk.Button(
            root, text="Select", command=get_selected_datetime)
        select_button.pack(pady=10)

        root.mainloop()

        return start
    start_time = get_start().astimezone(local_time)
    print(start_time)

    end = None

    def get_end():
        def get_selected_datetime():
            nonlocal end
            year = year_picker.get()
            month = month_picker.get()
            day = day_picker.get()
            hour = hour_picker.get()
            minute = minute_picker.get()

            datetime_str = f"{year}-{month}-{day} {hour}:{minute}"
            end = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            root.quit()
            root.destroy()

        root = tk.Tk()
        root.title("Date and Time Picker")

        # max date and time
        default_datetime = df['converted_timestamp'].max()
        default_year = str(default_datetime.year)
        default_month = str(default_datetime.month).zfill(2)
        default_day = str(default_datetime.day).zfill(2)
        default_hour = str(default_datetime.hour).zfill(2)
        default_minute = str(default_datetime.minute).zfill(2)

        # year
        year_label = ttk.Label(root, text="Year (YYYY):")
        year_label.pack(pady=5)
        year_picker = ttk.Entry(root, width=10)
        year_picker.insert(0, default_year)
        year_picker.pack()

        # month
        month_label = ttk.Label(root, text="Month (MM):")
        month_label.pack(pady=5)
        month_picker = ttk.Entry(root, width=10)
        month_picker.insert(0, default_month)
        month_picker.pack()

        # day
        day_label = ttk.Label(root, text="Day (DD):")
        day_label.pack(pady=5)
        day_picker = ttk.Entry(root, width=10)
        day_picker.insert(0, default_day)
        day_picker.pack()

        # hour
        hour_label = ttk.Label(root, text="Hour (HH):")
        hour_label.pack(pady=5)
        hour_picker = ttk.Entry(root, width=10)
        hour_picker.insert(0, default_hour)
        hour_picker.pack()

        # minute
        minute_label = ttk.Label(root, text="Minute (MM):")
        minute_label.pack(pady=5)
        minute_picker = ttk.Entry(root, width=10)
        minute_picker.insert(0, default_minute)
        minute_picker.pack()

        # button
        select_button = ttk.Button(
            root, text="Select", command=get_selected_datetime)
        select_button.pack(pady=10)

        root.mainloop()

        return end
    end_time = get_end().astimezone(local_time)
    print(end_time)
    ################### select date/time range ###################

    ################### Chart Type ###################
    def chart_selection():
        def on_plot():
            nonlocal chart
            chart = 'connected'
            root.quit()
            root.destroy()

        def on_scatter():
            nonlocal chart
            chart = 'scatter'
            root.quit()
            root.destroy()

        root = tk.Tk()

        question_label = tk.Label(root, text="Connected or Scatter Chart?")
        question_label.pack()

        button_frame = tk.Frame(root)
        button_frame.pack()

        plot_button = tk.Button(
            button_frame, text="Connected", command=on_plot)
        plot_button.pack(side=tk.LEFT)

        scatter_button = tk.Button(
            button_frame, text="Scatter", command=on_scatter)
        scatter_button.pack(side=tk.LEFT)

        root.mainloop()
        return chart
    chart = chart_selection()
    ################### Chart Type ###################

    ################### Plot ###################
    axisTab1.set_xlabel("{}".format(x))
    axisTab1.set_ylabel("{}".format(y))

    df_filtered = df[(df['converted_timestamp'] >= start_time)
                     & (df['converted_timestamp'] <= end_time)]
    if(chart == 'scatter'):
        axisTab1.scatter(
            df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
        filledGraphsTab1 += 1
    else:
        axisTab1.plot(df_filtered['converted_timestamp'],
                      df_filtered['{}'.format(y)])
        filledGraphsTab1 += 1

    # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
    graphWidgetTab1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvasTab1.draw()

    # statistics
    stats = tk.Label(tab1, text="{y}: Mean: {mean}, Median: {median}, Min: {min}, Max: {max}".format(y=y, mean=round(df_filtered['{}'.format(y)].mean(), 2), median=round(
        df_filtered['{}'.format(y)].median(), 2), min=round(df_filtered['{}'.format(y)].min(), 2), max=round(df_filtered['{}'.format(y)].max(), 2), font=("Roboto", 12), bg="white"))
    stats.pack()

    # filledGraphsTab1 += 1 ## for some reason this one doesn't always work
    print("Filled Graphs Tab1 1:", filledGraphsTab1)

    ################### Plot ###################
# Choose New Graphs and graph it TAB1
def btn_newGraphTab1():
    global filledGraphsTab1
    global local_time
    global df
    global x
    global start_time
    global end_time

    if(filledGraphsTab1 == 0):
        tk.messagebox.showinfo("Warning", "Please import a folder first.")
        return

    # file dialog
    import_dialog = filedialog.askdirectory(title="Select a folder")
    selected_folder = import_dialog
    print(selected_folder)

    # Import metadata
    print('Metadata:')
    fileMeta = selected_folder + '/metadata.csv'
    with open(fileMeta, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

    # Plot data
    print('Graph of summary: (opening in new window)')
    fileSum = selected_folder + '/summary.csv'
    # columns = ['Unix Timestamp (UTC)', 'Movement intensity']
    df = pd.read_csv(fileSum)
    columns = df.columns
    columns = [element for element in columns if element is not None]
    # df = pd.read_csv(fileSum, usecols=columns)
    # axis1Tab1.clear()
    print("Columns: ", columns)

    ################### select y ###################
    def get_y(columns):
        def submit_selection():
            nonlocal y
            y = combo.get()
            root.quit()
            root.destroy()

        root = tk.Tk()

        y = None

        # title text
        title = tk.Label(root, text='Select Y axis')
        title.pack(pady=10)

        # combo box
        combo = tk.ttk.Combobox(root, values=columns)
        combo.current(0)
        combo.pack(pady=10)

        # Submit btn
        submit_btn = ttk.Button(root, text='Submit', command=submit_selection)
        submit_btn.pack()

        root.mainloop()

        return y
    y = get_y(columns)
    print(y)
    ################### select y ###################

    ################### select date/time range ###################
    timestamp_column = 'Unix Timestamp (UTC)'
    df['converted_timestamp'] = pd.to_datetime(
        df[timestamp_column], unit='ms').dt.tz_localize(pytz.utc).dt.tz_convert(local_time)
    start = None

    ################### Chart Type ###################
    def chart_selection():
        def on_plot():
            nonlocal chart
            chart = 'connected'
            root.quit()
            root.destroy()

        def on_scatter():
            nonlocal chart
            chart = 'scatter'
            root.quit()
            root.destroy()

        root = tk.Tk()

        question_label = tk.Label(root, text="Connected or Scatter Chart?")
        question_label.pack()

        button_frame = tk.Frame(root)
        button_frame.pack()

        plot_button = tk.Button(
            button_frame, text="Connected", command=on_plot)
        plot_button.pack(side=tk.LEFT)

        scatter_button = tk.Button(
            button_frame, text="Scatter", command=on_scatter)
        scatter_button.pack(side=tk.LEFT)

        root.mainloop()
        return chart
    chart = chart_selection()
    ################### Chart Type ###################
    # plot stuff
    if(filledGraphsTab1 == 1):
        ################### Plot ###################
        axis1Tab1.set_xlabel("{}".format(x))
        axis1Tab1.set_ylabel("{}".format(y))

        df_filtered = df[(df['converted_timestamp'] >= start_time)
                         & (df['converted_timestamp'] <= end_time)]
        # if(chart == 'scatter'):
        #     axis1Tab1.scatter(
        #         df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
        # else:
        #     axis1Tab1.plot(df_filtered['converted_timestamp'],
        #                    df_filtered['{}'.format(y)])
        if(x=='Unix Timestamp (UTC) (M-D H)'):
            if(chart == 'scatter'):
                axis1Tab1.scatter(
                    df_filtered['converted_timestamp'].to_timestamp(), df_filtered['{}'.format(y)])
            else:
                axis1Tab1.plot(df_filtered['converted_timestamp'].to_timestamp(),
                            df_filtered['{}'.format(y)])
        else:
            if(chart == 'scatter'):
                axis1Tab1.scatter(
                    df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
            else:
                axis1Tab1.plot(df_filtered['converted_timestamp'],
                            df_filtered['{}'.format(y)])

        # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
        graphWidgetTab1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvasTab1.draw()

        # statistics
        stats = tk.Label(tab1, text="{y}: Mean: {mean}, Median: {median}, Min: {min}, Max: {max}".format(y=y, mean=round(df_filtered['{}'.format(y)].mean(), 2), median=round(
            df_filtered['{}'.format(y)].median(), 2), min=round(df_filtered['{}'.format(y)].min(), 2), max=round(df_filtered['{}'.format(y)].max(), 2), font=("Roboto", 12), bg="white"))
        stats.pack()
        filledGraphsTab1 += 1
        print("Filled Graphs 2:", filledGraphsTab1)
        return

    elif(filledGraphsTab1 == 2):
        ################### Plot ###################
        axis2Tab1.set_xlabel("{}".format(x))
        axis2Tab1.set_ylabel("{}".format(y))

        df_filtered = df[(df['converted_timestamp'] >= start_time)
                         & (df['converted_timestamp'] <= end_time)]
        # if(chart == 'scatter'):
        #     axis2Tab1.scatter(
        #         df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
        # else:
        #     axis2Tab1.plot(df_filtered['converted_timestamp'],
        #                    df_filtered['{}'.format(y)])
        if(x=='Unix Timestamp (UTC) (M-D H)'):
            if(chart == 'scatter'):
                axis2Tab1.scatter(
                    df_filtered['converted_timestamp'].to_timestamp(), df_filtered['{}'.format(y)])
            else:
                axis2Tab1.plot(df_filtered['converted_timestamp'].to_timestamp(),
                            df_filtered['{}'.format(y)])
        else:
            if(chart == 'scatter'):
                axis2Tab1.scatter(
                    df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
            else:
                axis2Tab1.plot(df_filtered['converted_timestamp'],
                            df_filtered['{}'.format(y)])

        # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
        graphWidgetTab1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvasTab1.draw()

        # statistics
        stats = tk.Label(tab1, text="{y}: Mean: {mean}, Median: {median}, Min: {min}, Max: {max}".format(y=y, mean=round(df_filtered['{}'.format(y)].mean(), 2), median=round(
            df_filtered['{}'.format(y)].median(), 2), min=round(df_filtered['{}'.format(y)].min(), 2), max=round(df_filtered['{}'.format(y)].max(), 2), font=("Roboto", 12), bg="white"))
        stats.pack()
        filledGraphsTab1 += 1
        print("Filled Graphs Tab1 3:", filledGraphsTab1)
        return
    elif(filledGraphsTab1 == 3):
        ################### Plot ###################
        axis3Tab1.set_xlabel("{}".format(x))
        axis3Tab1.set_ylabel("{}".format(y))

        df_filtered = df[(df['converted_timestamp'] >= start_time)
                         & (df['converted_timestamp'] <= end_time)]
        # if(chart == 'scatter'):
        #     axis2Tab1.scatter(
        #         df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
        # else:
        #     axis2Tab1.plot(df_filtered['converted_timestamp'],
        #                    df_filtered['{}'.format(y)])
        if(x=='Unix Timestamp (UTC) (M-D H)'):
            if(chart == 'scatter'):
                axis3Tab1.scatter(
                    df_filtered['converted_timestamp'].to_timestamp(), df_filtered['{}'.format(y)])
            else:
                axis3Tab1.plot(df_filtered['converted_timestamp'].to_timestamp(),
                            df_filtered['{}'.format(y)])
        else:
            if(chart == 'scatter'):
                axis3Tab1.scatter(
                    df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
            else:
                axis3Tab1.plot(df_filtered['converted_timestamp'],
                            df_filtered['{}'.format(y)])

        # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
        graphWidgetTab1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvasTab1.draw()

        # statistics
        stats = tk.Label(tab1, text="{y}: Mean: {mean}, Median: {median}, Min: {min}, Max: {max}".format(y=y, mean=round(df_filtered['{}'.format(y)].mean(), 2), median=round(
            df_filtered['{}'.format(y)].median(), 2), min=round(df_filtered['{}'.format(y)].min(), 2), max=round(df_filtered['{}'.format(y)].max(), 2), font=("Roboto", 12), bg="white"))
        stats.pack()
        filledGraphsTab1 += 1
        print("Filled Graphs Tab1 3:", filledGraphsTab1)
        return    
    
    elif(filledGraphsTab1 > 3):
        tk.messagebox.showinfo("Warning", "You have reached the limit of graphs to be displayed on one screen. Please import new folder to continue.")
        return

    ################### Plot ###################
# Choose import folder and graph it TAB2
def btn_importFolderTab2():
    global filledGraphsTab2

    excluded_widgets = [Tab2BtnFrame, Tab2importBtn, Tab2NewGraphBtn,
                        Tab2TimeBtn, figureTab2, canvasTab2, graphWidgetTab2, 
                        toolbarTab2]
    for widget in tab2.winfo_children():
        if(widget not in excluded_widgets):
            widget.destroy()
    axis1Tab2.clear()
    axis2Tab2.clear()
    axis3Tab2.clear()
    filledGraphsTab2 = 0

    global local_time
    global df
    global x
    global start_time
    global end_time
    # Create a file dialog
    # file_dialog = filedialog.askopen(title="Select a folder")
    import_dialog = filedialog.askdirectory(title="Select a folder")
    # Get the selected file
    selected_folder = import_dialog
    # Print the selected file
    print(selected_folder)

    # Import metadata
    print('Metadata:')
    fileMeta = selected_folder + '/metadata.csv'
    with open(fileMeta, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

    # Plot data
    print('Graph of summary: (opening in new window)')
    fileSum = selected_folder + '/summary.csv'
    # columns = ['Unix Timestamp (UTC)', 'Movement intensity']
    df = pd.read_csv(fileSum)
    columns = df.columns
    columns = [element for element in columns if element is not None]
    # df = pd.read_csv(fileSum, usecols=columns)
    axisTab2.clear()
    print("Columns: ", columns)

    ################### select y ###################
    def get_y(columns):
        def submit_selection():
            nonlocal y
            y = combo.get()
            root.quit()
            root.destroy()

        root = tk.Tk()

        y = None

        # title text
        title = tk.Label(root, text='Select Y axis')
        title.pack(pady=10)

        # combo box
        combo = tk.ttk.Combobox(root, values=columns)
        combo.current(0)
        combo.pack(pady=10)

        # Submit btn
        submit_btn = ttk.Button(root, text='Submit', command=submit_selection)
        submit_btn.pack()

        root.mainloop()

        return y
    y = get_y(columns)
    print(y)
    ################### select y ###################

    ################### select date/time range ###################
    timestamp_column = 'Unix Timestamp (UTC)'
    df['converted_timestamp'] = pd.to_datetime(
        df[timestamp_column], unit='ms').dt.tz_localize(pytz.utc).dt.tz_convert(local_time)
    start = None

    def get_start():
        global start_time
        global end_time

        def get_selected_datetime():
            nonlocal start
            year = year_picker.get()
            month = month_picker.get()
            day = day_picker.get()
            hour = hour_picker.get()
            minute = minute_picker.get()

            datetime_str = f"{year}-{month}-{day} {hour}:{minute}"
            start = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            root.quit()
            root.destroy()

        root = tk.Tk()
        root.title("Date and Time Picker")

        # min date and time
        default_datetime = df['converted_timestamp'].min()
        default_year = str(default_datetime.year)
        default_month = str(default_datetime.month).zfill(2)
        default_day = str(default_datetime.day).zfill(2)
        default_hour = str(default_datetime.hour).zfill(2)
        default_minute = str(default_datetime.minute).zfill(2)

        # year
        year_label = ttk.Label(root, text="Year (YYYY):")
        year_label.pack(pady=5)
        year_picker = ttk.Entry(root, width=10)
        year_picker.insert(0, default_year)
        year_picker.pack()

        # month
        month_label = ttk.Label(root, text="Month (MM):")
        month_label.pack(pady=5)
        month_picker = ttk.Entry(root, width=10)
        month_picker.insert(0, default_month)
        month_picker.pack()

        # day
        day_label = ttk.Label(root, text="Day (DD):")
        day_label.pack(pady=5)
        day_picker = ttk.Entry(root, width=10)
        day_picker.insert(0, default_day)
        day_picker.pack()

        # hour
        hour_label = ttk.Label(root, text="Hour (HH):")
        hour_label.pack(pady=5)
        hour_picker = ttk.Entry(root, width=10)
        hour_picker.insert(0, default_hour)
        hour_picker.pack()

        # minute
        minute_label = ttk.Label(root, text="Minute (MM):")
        minute_label.pack(pady=5)
        minute_picker = ttk.Entry(root, width=10)
        minute_picker.insert(0, default_minute)
        minute_picker.pack()

        # button
        select_button = ttk.Button(
            root, text="Select", command=get_selected_datetime)
        select_button.pack(pady=10)

        root.mainloop()

        return start
    start_time = get_start().astimezone(local_time)
    print(start_time)

    end = None

    def get_end():
        def get_selected_datetime():
            nonlocal end
            year = year_picker.get()
            month = month_picker.get()
            day = day_picker.get()
            hour = hour_picker.get()
            minute = minute_picker.get()

            datetime_str = f"{year}-{month}-{day} {hour}:{minute}"
            end = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            root.quit()
            root.destroy()

        root = tk.Tk()
        root.title("Date and Time Picker")

        # max date and time
        default_datetime = df['converted_timestamp'].max()
        default_year = str(default_datetime.year)
        default_month = str(default_datetime.month).zfill(2)
        default_day = str(default_datetime.day).zfill(2)
        default_hour = str(default_datetime.hour).zfill(2)
        default_minute = str(default_datetime.minute).zfill(2)

        # year
        year_label = ttk.Label(root, text="Year (YYYY):")
        year_label.pack(pady=5)
        year_picker = ttk.Entry(root, width=10)
        year_picker.insert(0, default_year)
        year_picker.pack()

        # month
        month_label = ttk.Label(root, text="Month (MM):")
        month_label.pack(pady=5)
        month_picker = ttk.Entry(root, width=10)
        month_picker.insert(0, default_month)
        month_picker.pack()

        # day
        day_label = ttk.Label(root, text="Day (DD):")
        day_label.pack(pady=5)
        day_picker = ttk.Entry(root, width=10)
        day_picker.insert(0, default_day)
        day_picker.pack()

        # hour
        hour_label = ttk.Label(root, text="Hour (HH):")
        hour_label.pack(pady=5)
        hour_picker = ttk.Entry(root, width=10)
        hour_picker.insert(0, default_hour)
        hour_picker.pack()

        # minute
        minute_label = ttk.Label(root, text="Minute (MM):")
        minute_label.pack(pady=5)
        minute_picker = ttk.Entry(root, width=10)
        minute_picker.insert(0, default_minute)
        minute_picker.pack()

        # button
        select_button = ttk.Button(
            root, text="Select", command=get_selected_datetime)
        select_button.pack(pady=10)

        root.mainloop()

        return end
    end_time = get_end().astimezone(local_time)
    print(end_time)
    ################### select date/time range ###################

    ################### Chart Type ###################
    def chart_selection():
        def on_plot():
            nonlocal chart
            chart = 'connected'
            root.quit()
            root.destroy()

        def on_scatter():
            nonlocal chart
            chart = 'scatter'
            root.quit()
            root.destroy()

        root = tk.Tk()

        question_label = tk.Label(root, text="Connected or Scatter Chart?")
        question_label.pack()

        button_frame = tk.Frame(root)
        button_frame.pack()

        plot_button = tk.Button(
            button_frame, text="Connected", command=on_plot)
        plot_button.pack(side=tk.LEFT)

        scatter_button = tk.Button(
            button_frame, text="Scatter", command=on_scatter)
        scatter_button.pack(side=tk.LEFT)

        root.mainloop()
        return chart
    chart = chart_selection()
    ################### Chart Type ###################

    ################### Plot ###################
    axisTab2.set_xlabel("{}".format(x))
    axisTab2.set_ylabel("{}".format(y))

    df_filtered = df[(df['converted_timestamp'] >= start_time)
                     & (df['converted_timestamp'] <= end_time)]
    if(chart == 'scatter'):
        axisTab2.scatter(
            df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
        filledGraphsTab2 += 1
    else:
        axisTab2.plot(df_filtered['converted_timestamp'],
                      df_filtered['{}'.format(y)])
        filledGraphsTab2 += 1

    # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
    graphWidgetTab2.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvasTab2.draw()

    # statistics
    stats = tk.Label(tab2, text="{y}: Mean: {mean}, Median: {median}, Min: {min}, Max: {max}".format(y=y, mean=round(df_filtered['{}'.format(y)].mean(), 2), median=round(
        df_filtered['{}'.format(y)].median(), 2), min=round(df_filtered['{}'.format(y)].min(), 2), max=round(df_filtered['{}'.format(y)].max(), 2), font=("Roboto", 12), bg="white"))
    stats.pack()

    # filledGraphsTab2 += 1 ## for some reason this one doesn't always work
    print("Filled Graphs Tab2 1:", filledGraphsTab2)
# Choose New Graphs and graph it TAB2
def btn_newGraphTab2():
    global filledGraphsTab2
    global local_time
    global df
    global x
    global start_time
    global end_time

    if(filledGraphsTab2 == 0):
        tk.messagebox.showinfo("Warning", "Please import a folder first.")
        return

    # file dialog
    import_dialog = filedialog.askdirectory(title="Select a folder")
    selected_folder = import_dialog
    print(selected_folder)

    # Import metadata
    print('Metadata:')
    fileMeta = selected_folder + '/metadata.csv'
    with open(fileMeta, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

    # Plot data
    print('Graph of summary: (opening in new window)')
    fileSum = selected_folder + '/summary.csv'
    # columns = ['Unix Timestamp (UTC)', 'Movement intensity']
    df = pd.read_csv(fileSum)
    columns = df.columns
    columns = [element for element in columns if element is not None]
    # df = pd.read_csv(fileSum, usecols=columns)
    # axis1Tab2.clear()
    print("Columns: ", columns)

    ################### select y ###################
    def get_y(columns):
        def submit_selection():
            nonlocal y
            y = combo.get()
            root.quit()
            root.destroy()

        root = tk.Tk()

        y = None

        # title text
        title = tk.Label(root, text='Select Y axis')
        title.pack(pady=10)

        # combo box
        combo = tk.ttk.Combobox(root, values=columns)
        combo.current(0)
        combo.pack(pady=10)

        # Submit btn
        submit_btn = ttk.Button(root, text='Submit', command=submit_selection)
        submit_btn.pack()

        root.mainloop()

        return y
    y = get_y(columns)
    print(y)
    ################### select y ###################

    ################### select date/time range ###################
    timestamp_column = 'Unix Timestamp (UTC)'
    df['converted_timestamp'] = pd.to_datetime(
        df[timestamp_column], unit='ms').dt.tz_localize(pytz.utc).dt.tz_convert(local_time)
    start = None

    ################### Chart Type ###################
    def chart_selection():
        def on_plot():
            nonlocal chart
            chart = 'connected'
            root.quit()
            root.destroy()

        def on_scatter():
            nonlocal chart
            chart = 'scatter'
            root.quit()
            root.destroy()

        root = tk.Tk()

        question_label = tk.Label(root, text="Connected or Scatter Chart?")
        question_label.pack()

        button_frame = tk.Frame(root)
        button_frame.pack()

        plot_button = tk.Button(
            button_frame, text="Connected", command=on_plot)
        plot_button.pack(side=tk.LEFT)

        scatter_button = tk.Button(
            button_frame, text="Scatter", command=on_scatter)
        scatter_button.pack(side=tk.LEFT)

        root.mainloop()
        return chart
    chart = chart_selection()
    ################### Chart Type ###################
    # plot stuff
    if(filledGraphsTab2 == 1):
        ################### Plot ###################
        axis1Tab2.set_xlabel("{}".format(x))
        axis1Tab2.set_ylabel("{}".format(y))

        df_filtered = df[(df['converted_timestamp'] >= start_time)
                         & (df['converted_timestamp'] <= end_time)]
        # if(chart == 'scatter'):
        #     axis1Tab2.scatter(
        #         df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
        # else:
        #     axis1Tab2.plot(df_filtered['converted_timestamp'],
        #                    df_filtered['{}'.format(y)])
        if(x=='Unix Timestamp (UTC) (M-D H)'):
            if(chart == 'scatter'):
                axis1Tab2.scatter(
                    df_filtered['converted_timestamp'].to_timestamp(), df_filtered['{}'.format(y)])
            else:
                axis1Tab2.plot(df_filtered['converted_timestamp'].to_timestamp(),
                            df_filtered['{}'.format(y)])
        else:
            if(chart == 'scatter'):
                axis1Tab2.scatter(
                    df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
            else:
                axis1Tab2.plot(df_filtered['converted_timestamp'],
                            df_filtered['{}'.format(y)])

        # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
        graphWidgetTab2.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvasTab2.draw()

        # statistics
        stats = tk.Label(tab2, text="{y}: Mean: {mean}, Median: {median}, Min: {min}, Max: {max}".format(y=y, mean=round(df_filtered['{}'.format(y)].mean(), 2), median=round(
            df_filtered['{}'.format(y)].median(), 2), min=round(df_filtered['{}'.format(y)].min(), 2), max=round(df_filtered['{}'.format(y)].max(), 2), font=("Roboto", 12), bg="white"))
        stats.pack()
        filledGraphsTab2 += 1
        print("Filled Graphs 2:", filledGraphsTab2)
        return

    elif(filledGraphsTab2 == 2):
        ################### Plot ###################
        axis2Tab2.set_xlabel("{}".format(x))
        axis2Tab2.set_ylabel("{}".format(y))

        df_filtered = df[(df['converted_timestamp'] >= start_time)
                         & (df['converted_timestamp'] <= end_time)]
        # if(chart == 'scatter'):
        #     axis2Tab2.scatter(
        #         df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
        # else:
        #     axis2Tab2.plot(df_filtered['converted_timestamp'],
        #                    df_filtered['{}'.format(y)])
        if(x=='Unix Timestamp (UTC) (M-D H)'):
            if(chart == 'scatter'):
                axis2Tab2.scatter(
                    df_filtered['converted_timestamp'].to_timestamp(), df_filtered['{}'.format(y)])
            else:
                axis2Tab2.plot(df_filtered['converted_timestamp'].to_timestamp(),
                            df_filtered['{}'.format(y)])
        else:
            if(chart == 'scatter'):
                axis2Tab2.scatter(
                    df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
            else:
                axis2Tab2.plot(df_filtered['converted_timestamp'],
                            df_filtered['{}'.format(y)])

        # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
        graphWidgetTab2.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvasTab2.draw()

        # statistics
        stats = tk.Label(tab2, text="{y}: Mean: {mean}, Median: {median}, Min: {min}, Max: {max}".format(y=y, mean=round(df_filtered['{}'.format(y)].mean(), 2), median=round(
            df_filtered['{}'.format(y)].median(), 2), min=round(df_filtered['{}'.format(y)].min(), 2), max=round(df_filtered['{}'.format(y)].max(), 2), font=("Roboto", 12), bg="white"))
        stats.pack()
        filledGraphsTab2 += 1
        print("Filled Graphs Tab2 3:", filledGraphsTab2)
        return
    elif(filledGraphsTab2 == 3):
        ################### Plot ###################
        axis3Tab2.set_xlabel("{}".format(x))
        axis3Tab2.set_ylabel("{}".format(y))

        df_filtered = df[(df['converted_timestamp'] >= start_time)
                         & (df['converted_timestamp'] <= end_time)]
        # if(chart == 'scatter'):
        #     axis2Tab2.scatter(
        #         df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
        # else:
        #     axis2Tab2.plot(df_filtered['converted_timestamp'],
        #                    df_filtered['{}'.format(y)])
        if(x=='Unix Timestamp (UTC) (M-D H)'):
            if(chart == 'scatter'):
                axis3Tab2.scatter(
                    df_filtered['converted_timestamp'].to_timestamp(), df_filtered['{}'.format(y)])
            else:
                axis3Tab2.plot(df_filtered['converted_timestamp'].to_timestamp(),
                            df_filtered['{}'.format(y)])
        else:
            if(chart == 'scatter'):
                axis3Tab2.scatter(
                    df_filtered['converted_timestamp'], df_filtered['{}'.format(y)])
            else:
                axis3Tab2.plot(df_filtered['converted_timestamp'],
                            df_filtered['{}'.format(y)])

        # Create a tkinter canvas and add the FigureCanvasTkAgg widget to it
        graphWidgetTab2.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvasTab2.draw()

        # statistics
        stats = tk.Label(tab2, text="{y}: Mean: {mean}, Median: {median}, Min: {min}, Max: {max}".format(y=y, mean=round(df_filtered['{}'.format(y)].mean(), 2), median=round(
            df_filtered['{}'.format(y)].median(), 2), min=round(df_filtered['{}'.format(y)].min(), 2), max=round(df_filtered['{}'.format(y)].max(), 2), font=("Roboto", 12), bg="white"))
        stats.pack()
        filledGraphsTab2 += 1
        print("Filled Graphs Tab2 3:", filledGraphsTab2)
        return    
    elif(filledGraphsTab2 > 3):
        tk.messagebox.showinfo("Warning", "You have reached the limit of graphs to be displayed on one screen. Please import new folder to continue.")
        return

#TAB1 BUTTONS ------------------------------------------------------------------------------------------------------------#
Tab1BtnFrame = ttk.Frame(tab1)
Tab1BtnFrame.pack(side='top')

# import folder button
Tab1importBtn = ttk.Button(
    Tab1BtnFrame, text='Import folder', command=btn_importFolderTab1, style='')
Tab1importBtn.pack(side='left')

# new graph button
Tab1NewGraphBtn = ttk.Button(
    Tab1BtnFrame, text='New Graph', command=btn_newGraphTab1, style='')
Tab1NewGraphBtn.pack(side='left')

# change time button  (UTC/Local Machine Time)
Tab1TimeBtn = ttk.Button(
    Tab1BtnFrame, text='UTC/Local Machine Time', command=time_slection, style='')
Tab1TimeBtn.pack(side='left')

#TAB2 BUTTONS -----------------------------------------------------------------------------------------------------------#
Tab2BtnFrame = ttk.Frame(tab2)
Tab2BtnFrame.pack(side='top')

# import folder button
Tab2importBtn = ttk.Button(
    Tab2BtnFrame, text='Import folder', command=btn_importFolderTab2, style='')
Tab2importBtn.pack(side='left')

# new graph button
Tab2NewGraphBtn = ttk.Button(
    Tab2BtnFrame, text='New Graph', command=btn_newGraphTab2, style='')
Tab2NewGraphBtn.pack(side='left')

# change time button  (UTC/Local Machine Time)
Tab2TimeBtn = ttk.Button(
    Tab2BtnFrame, text='UTC/Local Machine Time', command=time_slection, style='')
Tab2TimeBtn.pack(side='left')

# Start the Tkinter event loop
window.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, StringVar, PhotoImage, Button, Text, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from Functions import check_for_copies

filename = ' '
serials = []
uName = []
uNames = []
Measurements = []
Selected_Names = []
uName_selected = []
Serials_selected = []
Measurements_selected = []
Dates_selected = []
number_of_plots = 0

class Window(tk.Tk):
    def __init__(self):
        self.LabelDevice = tk.Label(window, text="Select Sensor")
        self.LabelDevice.place(x = 50, y = 450)
        self.name_combo_var = StringVar()
        self.name_combo = ttk.Combobox(window, textvariable = self.name_combo_var, values = None)
        self.name_combo.grid(column = 1, row = 1)
        self.name_combo.place(x = 50, y = 470)
        self.name_combo.bind("<<ComboboxSelected>>", self.uNameSelection)

        self.LabelSerial = tk.Label(window, text="Select Serial Number")
        self.LabelSerial.place(x = 220, y = 450)
        self.serial_combo_var = StringVar()
        self.serial_combo = ttk.Combobox(window, textvariable = self.serial_combo_var, values = None)
        self.serial_combo.grid(column = 1, row = 1)
        self.serial_combo.place(x = 220, y = 470)

        self.LabelSerial = tk.Label(window, text="Select Measurement")
        self.LabelSerial.place(x=390, y=450)
        self.measurement_combo_var = StringVar()
        self.measurement_combo = ttk.Combobox(window, values=None)
        self.measurement_combo.grid(column=1, row=1)
        self.measurement_combo.place(x=390, y=470)

        self.file_explorer_img = PhotoImage(file=r"C:\Users\Yura\PycharmProjects\PlotKing1.0\file_explorer_40x30.png")
        self.button_explore = Button(window, image = self.file_explorer_img, command= self.BrowseFiles)
        self.button_explore.grid(column = 1, row = 1)
        self.button_explore.place(height = 40, width = 50)
        self.button_explore.place(x = 850)

        self.plot_img = PhotoImage(file=r"C:\Users\Yura\PycharmProjects\PlotKing1.0\3169872-200_40x30.png")
        self.button_plot = Button(window, image = self.plot_img, command = self.PlotPressed, state = "disabled")
        self.button_plot.grid(column = 1, row = 1)
        self.button_plot.place(height = 40, width = 150)
        self.button_plot.place(x = 665, y = 470)

        self.recycle_img = PhotoImage(file = r"C:\Users\Yura\PycharmProjects\PlotKing1.0\Recycle-Bin_2_30x30.png")
        self.button_clear = Button(window, image = self.recycle_img, command = self.clear_pressed)
        self.button_clear.grid(column = 1, row = 1)
        self.button_clear.place(height = 40, width = 40)
        self.button_clear.place(x = 815, y = 470)

        self.button_confirm = Button(window, text = "Confirm", command = self.confirm_pressed)
        self.button_confirm.grid(column = 1, row = 1)
        self.button_confirm.place(height = 30, width = 80)
        self.button_confirm.place(x = 250, y = 520)

        self.terminal_clear = Button(window, text = "Clear", command = self.ClearTerminal)
        self.terminal_clear.grid(column = 1, row = 1)
        self.terminal_clear.place(x = 80, y = 8)
        self.terminal_clear.place(width = 60)

        self.terminal_label = tk.Label(window, text = "Terminal")
        self.terminal_label.place(x = 20, y = 10)

        self.log_text = Text(window, height = 25, width = 75)
        self.log_text.config(state='disabled')
        self.log_text.place(x = 20, y = 30)

        self.border_label1 = tk.Label(window, text = "   ", borderwidth = 2, relief = 'solid')
        self.border_label1.grid(column = 1, row = 1)
        self.border_label1.place(height = 180, width = 220)
        self.border_label1.place(x = 650, y = 80)

        self.border_label2 = tk.Label(window, text="   ", borderwidth=2, relief='solid')
        self.border_label2.grid(column=1, row=1)
        self.border_label2.place(height=180, width=220)
        self.border_label2.place(x=650, y=255)

        self.date1_label = tk.Label(window, text = "Enter starting date:")
        self.date1_label.grid(column=1, row=1)
        self.date1_label.place(x=658, y=100)

        self.date1 = Text(window, height = 1, width = 25)
        self.date1.grid(column = 1, row = 1)
        self.date1.place(x = 658, y = 120)
        self.date1.insert('1.0', "YYYY-MM-DD hh:mm:ss")
        self.date1.bind('<KeyRelease>', self.date1_limiter)

        self.date2_label = tk.Label(window, text = "Enter ending date:")
        self.date2_label.grid(column=1, row=1)
        self.date2_label.place(x=658, y=180)

        self.date2 = Text(window, height=1, width=25, )
        self.date2.grid(column=1, row=1)
        self.date2.place(x=658, y=200)
        self.date2.insert('1.0', "YYYY-MM-DD hh:mm:ss")
        self.date2.bind('<KeyRelease>', self.date2_limiter)

        self.LabelAveraging = tk.Label(window, text="Averaging")
        self.LabelAveraging.place(x=657, y=265)
        self.averaging_combo_var = StringVar()
        self.averaging_combo_var.set('default')
        self.averaging_combo = ttk.Combobox(window, values= ['default', 'per hour', 'per 3 hours', 'per day'], width = 30)
        self.averaging_combo.grid(column=1, row=1)
        self.averaging_combo.place(x=658, y=285)

        self.LabelPlotType = tk.Label(window, text="Plot Type")
        self.LabelPlotType.place(x=657, y=315)
        self.plot_type_combo_var = StringVar()
        self.plot_type_combo_var.set('default')
        self.plot_type_combo = ttk.Combobox(window, values=['linear', 'dots', 'bars'], width = 30)
        self.plot_type_combo.grid(column=1, row=1)
        self.plot_type_combo.place(x=658, y=335)

        self.LabelPlotting = tk.Label(window, text="Plotting settings")
        self.LabelPlotting.place(x=657, y=365)
        self.plotting_combo_var = StringVar()
        self.plotting_combo = ttk.Combobox(window, values=['same coordinate plane', 'separately'], width = 30)
        self.plotting_combo.grid(column=1, row=1)
        self.plotting_combo.place(x=658, y=385)

    def uNameSelection(self, uName):
        global uNames
        global serials
        if (self.name_combo.get() == "Hydra-L" or self.name_combo.get() == "Hydra-L1" or self.name_combo.get() == "Тест воздуха"):
            self.measurement_combo["values"] = ['system_RSSI', 'BME280_temp', 'BME280_humidity', 'BME280_pressure']
            self.serial_combo.set('')
            self.measurement_combo.set('')
        elif (self.name_combo.get() == "Опорный барометр" or self.name_combo.get() == "Паскаль" or self.name_combo.get() == "РОСА К-2"):
            self.measurement_combo["values"] = ['system_RSSI', 'weather_temp', 'weather_pressure']
            self.serial_combo.set('')
            self.measurement_combo.set('')
        elif (self.name_combo.get() == "Тест Студии"):
            self.measurement_combo["values"] = ['system_RSSI', 'TCS34725_colorTempCT', 'TCS34725_lux', 'BH1750_lux',
                                                'BH1750_blinkmin', 'BH1750_blinkmax', 'BH1750_blink', 'AM2321_temp', 'AM2321_humidity',
                                                'BME280_temp', 'BME280_humidity', 'BME280_pressure', 'DS18B20_temp']
            self.serial_combo.set('')
            self.measurement_combo.set('')
        elif (self.name_combo.get() == "Сервер K3edu"):
            self.measurement_combo["values"] = 'system_RSSI'
            self.serial_combo.set('')
            self.measurement_combo.set('')
        else:
            self.measurement_combo["values"] = ''
            self.serial_combo.set('')
            self.measurement_combo.set('')
        for i in range(0, len(uNames)):
            if uNames[i] == self.name_combo.get():
                break
        if (serials[i][0] == 0):
            serials[i].remove(0)
        self.serial_combo["values"] = serials[i]

    def date1_limiter(self, value):
        str = self.date1.get('1.0', 'end-1c')
        breaks = str.count('\n')
        chars = len(str) - breaks
        if (chars > 19):
            self.date1.delete('end-2c')

    def date2_limiter(self, value):
        str = self.date2.get('1.0', 'end-1c')
        breaks = str.count('\n')
        chars = len(str) - breaks
        if (chars > 19):
            self.date2.delete('end-2c')

    def ClearTerminal(self):
        self.log_text.config(state = "normal")
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state = "disabled")

    def confirm_pressed(self):
        global number_of_plots
        global uName_selected
        global Serials_selected
        global Measurements_selected
        if (number_of_plots < 3):
            if (len(self.name_combo.get()) > 1):
                if (len(self.serial_combo.get()) != 0):
                    if (len(self.measurement_combo.get()) != 0):
                        if ((self.date1.get('1.0', 'end-1c') in self.df.values[0]) and (self.date2.get('1.0', 'end-1c') in self.df.values[0])):
                            if (list(self.df.values[0]).index(str(self.date1.get('1.0', 'end-1c')))) < (list(self.df.values[0]).index(str(self.date2.get('1.0', 'end-1c')))):
                                uName_selected.append(self.name_combo.get())
                                Serials_selected.append(self.serial_combo.get())
                                Measurements_selected.append(self.measurement_combo.get())
                                Dates_selected.append(self.date1.get('1.0', 'end-1c'))
                                Dates_selected.append(self.date2.get('1.0', 'end-1c'))
                                temp_string = "Selected " + self.measurement_combo.get() + " from " + self.name_combo.get() + " sensor with serial number " + self.serial_combo.get() + \
                                              " (" + str(number_of_plots + 1) + "/3)" + "\n"
                                temp_string_date = "Time interval: from " + Dates_selected[len(Dates_selected) - 2] + " to " + Dates_selected[len(Dates_selected) - 1]
                                self.log_text.config(state='normal')
                                self.log_text.insert('1.0', "\n")
                                self.log_text.insert('1.0', "\n")
                                self.log_text.insert('1.0', temp_string_date)
                                self.log_text.insert('1.0', temp_string)
                                self.log_text.config(state='disabled')
                                self.button_plot.config(state = "normal")
                                number_of_plots += 1
                            else:
                                messagebox.showerror("Error", "Please select correct date")
                        else:
                            messagebox.showerror("Error", "Please select correct date")
                    else:
                        messagebox.showerror("Error", "Please select Measurement")
                else:
                    messagebox.showerror("Error", "Please select Serial Number")
            else:
                messagebox.showerror("Error", "Please select Sensor")
        else:
            messagebox.showerror("Error", "Reached maximal number of plots")

    def clear_pressed(self):
        global number_of_plots
        global uName_selected
        global Serials_selected
        global Measurements_selected
        if (number_of_plots != 0):
            number_of_plots = 0
            uName_selected.clear()
            Serials_selected.clear()
            Measurements_selected.clear()
            Dates_selected.clear()
            self.log_text.config(state='normal')
            self.log_text.insert('1.0', "\n")
            self.log_text.insert('1.0', "\n")
            self.log_text.insert('1.0', "Plot memory cleared: plots selected 0/3")
            self.log_text.config(state='disabled')
        else:
            self.log_text.config(state='normal')
            self.log_text.insert('1.0', "\n")
            self.log_text.insert('1.0', "\n")
            self.log_text.insert('1.0', "Plot memory is empty")
            self.log_text.config(state='disabled')
        self.button_plot.config(state = "disabled")

    def BrowseFiles(self):
        global number_of_plots
        self.name_combo.set('')
        self.serial_combo.set('')
        self.measurement_combo.set('')
        if (number_of_plots != 0):
            number_of_plots = 0
            uName_selected.clear()
            Serials_selected.clear()
            Measurements_selected.clear()
            Dates_selected.clear()
            self.log_text.config(state='normal')
            self.log_text.insert('1.0', "\n")
            self.log_text.insert('1.0', "\n")
            self.log_text.insert('1.0', "Plot memory cleared: plots selected 0/3")
            self.log_text.config(state='disabled')
        global filename
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("JSON Files", "*.json*"),("all files", "*.*")))
        if (len(filename) > 1):
            self.log_text.config(state='normal')
            self.log_text.insert('1.0', "\n")
            self.log_text.insert('1.0', "\n")
            self.log_text.insert('1.0', "Loaded: " + filename)
            self.log_text.config(state='disabled')
            self.df = pd.read_json(filename)
            global uName
            for i in range(0, len(self.df.values[1])):
                if (check_for_copies(uName, str(self.df.values[1][i])) == True):
                    uNames.append(self.df.values[1][i])
                    uName.append(self.df.values[1][i])
            global serials
            serials = [[0 for x in range(1)] for y in range(len(uName))]
            for i in range(0, len(uName)):
                for j in range(0, len(self.df.values[2])):
                    if (self.df.values[1][j] == uName[i]):
                        if (self.df.values[2][j] not in serials[i]):
                            serials[i].append(self.df.values[2][j])
            self.name_combo["values"] = uName
            self.data_df = pd.DataFrame()
            self.date1.delete('1.0', tk.END)
            self.date2.delete('1.0', tk.END)
            self.date1.insert(tk.END, str(self.df.values[0][0]))
            self.date2.insert(tk.END, str(self.df.values[0][len(self.df.columns)-1]))
            s = self.df.values[3][0]
            self.data_df = pd.json_normalize(s)

    def PlotPressed(self):
        if (self.plot_type_combo.get() != 'linear' and self.plot_type_combo.get() != 'dots' and self.plot_type_combo.get() != 'bars'):
            messagebox.showerror("Error", "Please select Plot Type")
            return
        elif (len(self.plotting_combo.get()) < 2):
            messagebox.showerror("Error", "Please select plotting settings")
            return
        xes = []
        yes = []
        for l in range(0, len(uName_selected)):
            date_int = 0
            global number_of_plots
            xaxis = []
            yaxis = []
            self.yaxis_df = pd.DataFrame()
            d1 = 0; d2 = 0
            if (self.averaging_combo.get() == 'per hour' or self.averaging_combo.get() == 'per 3 hours'):
                d1 = 11; d2 = 12
            elif (self.averaging_combo.get() == 'per day'):
                d1 = 8; d2 = 9
            x = 1; summ = 0;
            date = Dates_selected[date_int]; date_var = int(date[d1]+date[d2])
            k = list(self.df.values[0]).index(date)
            if (self.averaging_combo.get() == 'per hour' or self.averaging_combo.get() == 'per day' or self.averaging_combo.get() == 'per 3 hours'):
                while (self.df.values[0][k] != Dates_selected[date_int + 1]):
                    if (self.df.values[1][k] == uName_selected[l]):
                        self.yaxis_df = pd.json_normalize(self.df.values[3][k])
                        summ += int(float(self.yaxis_df[Measurements_selected[l]].head()[0]))
                        x += 1
                        date_new = str(self.df.values[0][k])
                        date_var_new = int(date_new[d1] + date_new[d2])
                        if (self.averaging_combo.get() == 'per 3 hours'):
                            if (date_var_new - date_var == 3):
                                date_var = date_var_new
                                xaxis.append(date_new)
                                yaxis.append(summ / x)
                                summ = 0
                                x = 0
                                date = date_new
                        elif (date_var_new > date_var):
                            date_var = date_var_new
                            xaxis.append(date_new)
                            yaxis.append(summ / x)
                            summ = 0
                            x = 0
                            date = date_new
                    k += 1
                    if (k == len(self.df.values[0])):
                        break
            else:
                while (self.df.values[0][k] != Dates_selected[date_int + 1]):
                    if (self.df.values[1][k] == uName_selected[l]):
                        xaxis.append(self.df.values[0][k])
                        self.yaxis_df = pd.json_normalize(self.df.values[3][k])
                        yaxis.append(self.yaxis_df[str(Measurements_selected[l])].head()[0])
                    k += 1
                    if (k == len(self.df.values[0])):
                        break
            xes.append(xaxis)
            yes.append(yaxis)
            l += 1
            date_int += 2
        p = 0
        maxx = []
        maxx = xes[0]
        if (len(xes) > 1):
            for r in range(0, len(xes)):
                if (len(xes[r]) > len(maxx)):
                    maxx = xes[r]
        if (self.plotting_combo.get() == "separately"):
            fig, ax1 = plt.subplots()
            ax1.grid()
            if (self.plot_type_combo.get() == 'linear'):
                ax1.plot(maxx, yes[0], c='r')
            elif (self.plot_type_combo.get() == 'dots'):
                ax1.scatter(maxx, yes[0], s=10, c='r')
            elif (self.plot_type_combo.get() == 'bars'):
                ax1.bar(maxx, yes[0], width=0.3, edgecolor='r')
            if (len(xes) >= 2):
                fig, ax2 = plt.subplots()
                ax2.grid()
                if (self.plot_type_combo.get() == 'linear'):
                    ax2.plot(maxx, yes[1], c='g')
                elif (self.plot_type_combo.get() == 'dots'):
                    ax2.scatter(maxx, yes[1], s=10, c='g')
                elif (self.plot_type_combo.get() == 'bars'):
                    ax2.bar(maxx, yes[1], width=0.3, edgecolor='g')
            if (len(xes) == 3):
                fig, ax3 = plt.subplots()
                ax3.grid()
                if (self.plot_type_combo.get() == 'linear'):
                    ax3.plot(maxx, yes[2], c='b')
                elif (self.plot_type_combo.get() == 'dots'):
                    ax3.scatter(maxx, yes[2], s=10, c='b')
                elif (self.plot_type_combo.get() == 'bars'):
                    ax3.bar(maxx, yes[2], width=0.3, edgecolor='b')
        else:
            plt.grid()
            while (p < len(xes)):
                if (self.plot_type_combo.get() == 'linear'):
                    if (p == 0):
                        plt.plot(maxx, yes[p], c='r')
                    elif (p == 1):
                        plt.plot(maxx, yes[p], c='g')
                    elif (p == 2):
                        plt.plot(maxx, yes[p], c='b')
                elif (self.plot_type_combo.get() == 'dots'):
                    if (p == 0):
                        plt.scatter(maxx, yes[p], s=10, c='r')
                    elif (p == 1):
                        plt.scatter(maxx, yes[p], s=10, c='g')
                    elif (p == 2):
                        plt.scatter(maxx, yes[p], s=10, c='b')
                elif (self.plot_type_combo.get() == 'bars'):
                    if (p == 0):
                        plt.bar(maxx, yes[p], width=0.3, edgecolor='r')
                    elif (p == 1):
                        plt.bar(maxx, yes[p], width=0.3, edgecolor='g')
                    elif (p == 2):
                        plt.bar(maxx, yes[p], width=0.3, edgecolor='b')
                p += 1
        plt.legend(Measurements_selected)
        plt.show()

if __name__ == "__main__":
    window = tk.Tk(className='Python Examples - Window Size')
    app = Window()
    window.wm_title("PlotKing1.0")
    window.geometry("900x600")
    window.resizable(False, False)
    window.mainloop()

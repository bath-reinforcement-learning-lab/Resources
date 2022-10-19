import pickle
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

def plot_graphs(folder_dir, runs):
    filenames = os.listdir(folder_dir)  
    file_cat_dict = {}
    for file in filenames:
        drl = file.split("_")[-1]
        if drl in file_cat_dict.keys():
            file_cat_dict[drl].append(file)
        else:
            file_cat_dict[drl] = [file]
    drl_cat_dict = {}
    for drl in file_cat_dict.keys():
        if drl not in drl_cat_dict.keys():
            drl_cat_dict[drl] = {}
        for file in file_cat_dict[drl]:
            tag = file.split("_")[0] # refers to decisions, rewards or length
            if tag not in drl_cat_dict[drl]:
                drl_cat_dict[drl][tag] = []
            drl_cat_dict[drl][tag].append(file)

    # Now we have each seperated.


    for drl in drl_cat_dict.keys():
        print("")
        print(drl)
        print("")
        colours = ["blue", "green", "red", "orange", "purple", "pink", "cyan",
                    "yellow", "brown" ]
        colour_index = 0
        for tag in drl_cat_dict[drl].keys():
            print("")
            print(tag)
            print("")
            tag_list = []
            for file in drl_cat_dict[drl][tag]:
                file_name = os.path.join(folder_dir, file)
                run = file_name.split("_")[-2]
                drl_pickle = open(file_name, "rb")
                tag_list.append(pickle.load(drl_pickle))

            # find shortest list
            shortest_len = 1000000 # arb high
            shortest_list = None
            for list_r in tag_list:
                if len(list_r) < shortest_len:
                    shortest_len = len(list_r)
                    shortest_list = list_r
            print(shortest_len)
            # get the new a
            a = []
            for list_r in tag_list:
                a.append([])

            ranger = len(shortest_list)

            for i in range(ranger):
                for j in range(len(tag_list)):
                    a[j].append(list_r[i])

            a = np.array(a)
            temp_list = np.mean(a, axis=0)
            window_size = 40
            temp_series = pd.Series(temp_list)
            windows = temp_series.rolling(window_size)
            moving_averages = windows.mean()
            moving_stds = windows.std()
            moving_averages_list = moving_averages.tolist()
            moving_stds_list = moving_stds.tolist()
            final_list = moving_averages_list[window_size - 1:]
            std_list = moving_stds_list[window_size - 1:]
            lower_list = []
            upper_list = []
            for i in range(len(final_list)):
                lower_list.append(final_list[i] - std_list[i])
                upper_list.append(final_list[i] + std_list[i])
            x = range(len(final_list))
            y = final_list
            # a, c = np.polyfit(x, y, 1)
            colour = colours[colour_index]
            plt.plot(x, y, label = tag+" mean", color = colour)
            plt.fill_between(x, lower_list, upper_list, color=colour, alpha = 0.3)
            #plt.plot(x, a*x + c, label = tag+ " best_fit", color = colour, linewidth=7.0)
            colour_index += 1
        plt.xlabel("episode number")
        plt.ylabel("Average episodic return")
        plt.legend()
        plt.title(drl)
        plt.show()









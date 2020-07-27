import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import numpy as np
from datetime import datetime

from operator import itemgetter

from scipy.interpolate import make_interp_spline, BSpline


def reward_functions_plot_swarm(file_path):
    records = []

    with open(file_path) as f:
        for line in f:
            data = json.loads(line)
            if data["completed"]:
                records.append({"class": "completed", "acc_reward": data["acc_rewards"]})
            else:
                if data["acc_rewards"] < 0:
                    continue
                records.append({"class": "not completed", "acc_reward": data["acc_rewards"]})

    df = pd.DataFrame(records)

    sns.set(style="whitegrid", color_codes=True)
    ax = sns.swarmplot(x="class", y="acc_reward", data=df, order=["not completed", "completed"])
    plt.ylabel('accumulated rewards')
    plt.xlabel('')
    plt.show()


def bar_chart(PATH):
    sorted_list = [
        (0.29333333333333333, 'double-dueling-prioritized_1'),
        (0.56, 'double-dueling-prioritized_2'),
        (0.6, 'double-dueling-prioritized_3'),
        (0.07333333333333333, 'double-dueling-prioritized_4'),
        (0.44, 'double-dueling-prioritized_5'),
        (0.0, 'double-dueling_1'),
        (0.35333333333333333, 'double-dueling_2'),
        (0.0, 'double-dueling_3'),
        (0.0, 'double-dueling_4'),
        (0.0, 'double-dueling_5'),
        (0.006666666666666667, 'double-prioritized_1'),
        (0.56, 'double-prioritized_2'),
        (0.2866666666666667, 'double-prioritized_3'),
        (0.07333333333333333, 'double-prioritized_4'),
        (0.44, 'double-prioritized_5'),
    ]

    sorted_list.sort(key=itemgetter(0))

    features_sorted = []
    importance_sorted = []

    for i in sorted_list:
        features_sorted += [i[1]]
        importance_sorted += [i[0]]

    plt.title("DQN Variants Performance", fontsize=15)
    plt.xlabel("Completion Rate", fontsize=13)

    plt.barh(range(len(importance_sorted)), importance_sorted, color="green", edgecolor='green')
    plt.yticks(range(len(importance_sorted)), features_sorted)

    plt.show()


def average_plot(PATH):
    # PATH: Set your path to the folder containing the .csv files

    # Fetch all files in path
    fileNames = os.listdir(PATH)

    # Filter file name list for files ending with .csv
    fileNames = [file for file in fileNames if '.csv' in file]

    file_version = 1
    data_frames = []
    legend_names = ['dist4', 'dist0.005', 'ep40']
    legends = 0
    # Loop over all files
    for file in fileNames:
        # Read .csv file and append to list

        data_frames.append(pd.read_csv(PATH + file))
        print("current file: {}".format(file))

        if file_version % 1 == 0:
            df = pd.concat(data_frames, axis=1, keys=['a', 'b', 'c', 'd', 'e'])

            df = df.groupby(level=1, axis=1).mean()
            # filter out 1% of the highest and lowest outliers
            q_low = df["Value"].quantile(0.01)
            q_hi = df["Value"].quantile(0.99)

            df_filtered = df[(df["Value"] < q_hi) & (df["Value"] > q_low)]

            x, y = df_filtered["Step"], df_filtered["Value"].ewm(com=150, adjust=False).mean()

            # Create line for every file
            if legends < 0:  # change this to include highlighting
                plt.plot(x, y, label='{}'.format(legend_names[legends]), linestyle=":")
            else:
                plt.plot(x, y, label='{}'.format(legend_names[legends]))
            plt.legend()

            data_frames = []
            file_version = 0
            legends += 1

        file_version += 1

    # Generate the plot
    plt.ylabel('accumulated rewards')
    plt.xlabel('time steps')
    plt.axhline(y=1500, color='y', linestyle=':')

    figure = plt.gcf()  # get current figure
    figure.set_size_inches(10, 6)

    plt.savefig(PATH + "evaluation_graph.png", dpi=400, format='png')
    plt.show()


def convert_completionRate_to_file(PATH, data_id="completion"):
    records = {}

    # Fetch all files in path
    fileNames = os.listdir(PATH)

    # Filter file name list for files ending with .csv
    fileNames = [file for file in fileNames if '.log' in file]

    # Loop over all files
    for file in fileNames:
        full = file.split('-')
        del full[-1]
        category = '-'.join(full)
        with open(PATH + file) as f:
            for line in f:
                data = json.loads(line)
                if data_id in data:
                    if category in records:
                        records[category].append(data[data_id])
                        continue
                    else:
                        records[category] = [data[data_id]]
                        continue

    f = open("{0}{2}-{1}.csv".format(PATH, datetime.today().strftime('%d.%m'), data_id), "w")

    keys = list(records.keys())
    f.write(", ".join(list(keys)))
    f.write("\n")
    entry_per_category_len = len(records[keys[0]])

    for i in range(entry_per_category_len):
        entry_str = ""
        for j in range(len(records)):
            entry_str += '{0}'.format(records[keys[j]][i])
            if j + 1 != len(records):
                entry_str += ', '
        entry_str += '\n'
        f.write(entry_str)

    f.close()

    print(records)


if __name__ == "__main__":
    # reward_functions_plot_swarm("../data/session_02.06/time-2230.log")
    # average_plot("E:/concept-1/final/")
    # bar_chart("")
    convert_completionRate_to_file("E:/concept-1/final/")

import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

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
    ax = sns.swarmplot(x="class", y="acc_reward", data=df)
    plt.ylabel('accumulated rewards')
    plt.xlabel('')
    plt.show()


def average_plot(PATH):
    # PATH: Set your path to the folder containing the .csv files

    # Fetch all files in path
    fileNames = os.listdir(PATH)

    # Filter file name list for files ending with .csv
    fileNames = [file for file in fileNames if '.csv' in file]

    # Loop over all files
    for file in fileNames:
        # Read .csv file and append to list

        df = pd.read_csv(PATH + file)
        print("current file: {}".format(file))

        # filter out 1% of the highest and lowest outliers
        q_low = df["Value"].quantile(0.01)
        q_hi = df["Value"].quantile(0.99)

        df_filtered = df[(df["Value"] < q_hi) & (df["Value"] > q_low)]

        x, y = df_filtered["Step"], df_filtered["Value"].ewm(com=50, adjust=False).mean()

        # Create line for every file
        plt.plot(x, y)

    # Generate the plot
    plt.ylabel('accumulated rewards')
    plt.xlabel('time steps')
    plt.show()


if __name__ == "__main__":
    # reward_functions_plot_swarm("../data/session_02.06/time-2230.log")
    average_plot("../study/algorithm_test/double_dueling_prioritized/data/")

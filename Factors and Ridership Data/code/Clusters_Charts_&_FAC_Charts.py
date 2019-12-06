# import packages for the file usage
import os.path
from pathlib import Path, PureWindowsPath

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys, os
import os

# declare paths
script_folder = ""
load_data = ""
output_folder = ""
folder_path = ""
file_name = ""


def get_cluster_file(_filename):
    current_dir = Path.cwd()
    # pathname = os.path.abspath(__file__)
    print("Inside Cluster method - Current working directory:", current_dir)
    current_dir = PureWindowsPath(current_dir)
    # current_dir = chdir(pathlib.Path('..'))
    print("Changed Cluster director - Current working directory:", current_dir.parents[0])
    # Change the directory
    current_dir = current_dir.parents[0] / 'Script Outputs' / 'Cluster_wise_summation_files'
    print("Inside Cluster method - Re-assigned working directory:", current_dir)
    os.chdir(str(current_dir))
    # home_dir = pathlib.Path.home()
    # print("Home dir is ",home_dir)
    # script_folder = os.path.abspath(pathname)
    # change_folder = os.path.abspath(os.path.join(script_folder, ".."))
    # print("Folder name: " + os.path.join(script_folder, ".."))
    # os.chdir(change_folder)
    # load_file = os.path.abspath(os.path.join(change_folder, "Estimation_File",_filename))
    # print("File name: " + load_file)
    df = pd.read_csv(_filename)
    return df



def get_UPT_FAC_file(_filename):
    current_dir = Path.cwd()
    # pathname = os.path.abspath(__file__)
    print("Inside UPT_FAC method - Current working directory:", current_dir)
    # print("Doesnt reach here")
    # print("Inside UPT_FAC method:", pathname)
    # script_folder = os.path.abspath(pathname)
    # change_folder = os.path.abspath(os.path.join(script_folder, ".."))
    # print("Folder name: " + change_folder)
    # change_folder = os.path.abspath(os.path.join(change_folder, "Mode Estimation/Est4"))
    # os.chdir(change_folder)
    # print("File name: " + change_folder)
    # return pd.read_csv(_filename)
    pass


def Create_Combined_Graphs(_dfCluster, _dfFAC,_folder_name,_file_name):
    # get unique values
    yrs = _dfCluster['Year'].unique()
    yrs.sort()
    chartname = ""
    clusters = _dfCluster[chartname].unique()
    clusters.sort()
    modes = _dfCluster['Mode'].unique()
    modes.sort()

    # create chart for the cluster file



    # create chart for the UPT_FAC file

    pass




def main():
    # create function to prepare charts
    dfGT11 = get_cluster_file("CLUSTER_GT_NEW_11.csv")
    dfGT11.head()
    # dfGT11
    # df_UPTFAC_GT11 = get_UPT_FAC_file("FAC_totals_GT_CLUSTERS.csv")
    # df_UPTFAC_GT11
    # Create_Cumulative_Graphs()
    # dfGT8 = get_cluster_file("CLUSTER_GT_8_GROUPS.csv")
    # df_UPTFAC_GT8 = get_UPT_FAC_file("FAC_totals_gt_grouped_CLUSTERS.csv")
    #
    # dfAPTA = get_cluster_file("CLUSTER_APTA.csv")
    # df_UPTFAC_APTA = get_UPT_FAC_file("FAC_totals_gt_grouped_CLUSTERS.csv")


if __name__ == "__main__":
    main()

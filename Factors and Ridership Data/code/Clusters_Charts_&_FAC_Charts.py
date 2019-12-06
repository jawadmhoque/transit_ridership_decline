# import packages for the file usage
import os.path
from pathlib import Path, PureWindowsPath
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os

# declare paths
script_folder = ""
load_data = ""
output_folder = ""
folder_path = ""
file_name = ""


def get_cluster_file(_filename):
    # get the abs path of the directory of the code/script
    # Factors and Ridership Data\ code
    current_dir = Path(__file__).parent.absolute()
    # Change the directory
    # \Script Outputs \ Cluster_wise_summation_files
    # print("current directory at get_cluster_file ",current_dir)
    current_dir = current_dir.parents[0] / 'Script Outputs' / 'Cluster_wise_summation_files'
    os.chdir(str(current_dir))
    # print("set directory at get_cluster_file ", current_dir)
    df = pd.read_csv(_filename)
    return df


def get_upt_fac_file(_filename):
    # get the abs path of the directory of the code/script
    # Factors and Ridership Data\ code
    current_dir = Path(__file__).parent.absolute()
    # Change the directory
    # \Model Estimation\Est4
    # print("current directory at get_cluster_file ",current_dir)
    current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est4'
    os.chdir(str(current_dir))
    # print("set directory at get_upt_fac_file ", current_dir)
    df = pd.read_csv(_filename)
    return df


def create_combined_graphs(_dfCluster, _dfFAC, _folder_name, _file_name):
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
    dfgt11 = get_cluster_file("CLUSTER_GT_NEW_11.csv")
    dfgt11.head()

    df_uptfac_gt11 = get_upt_fac_file("FAC_totals_GT_CLUSTERS.csv")
    df_uptfac_gt11.head()

    # Create_Cumulative_Graphs()
    # dfGT8 = get_cluster_file("CLUSTER_GT_8_GROUPS.csv")
    # df_UPTFAC_GT8 = get_UPT_FAC_file("FAC_totals_gt_grouped_CLUSTERS.csv")
    #
    # dfAPTA = get_cluster_file("CLUSTER_APTA.csv")
    # df_UPTFAC_APTA = get_UPT_FAC_file("FAC_totals_gt_grouped_CLUSTERS.csv")


if __name__ == "__main__":
    main()

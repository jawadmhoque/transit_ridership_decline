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
    # \Model Estimation\Est4
    # print("current directory at get_cluster_file ",current_dir)
    current_dir = current_dir.parents[0] / 'Script Outputs' / 'Cluster_wise_summation_files'
    os.chdir(str(current_dir))
    # print("set directory at get_upt_fac_file ", current_dir)
    df = pd.read_csv(_filename)
    return df

def get_upt_fac_file(_filename):
    # get the abs path of the directory of the code/script
    # Factors and Ridership Data\ code
    current_dir = Path(__file__).parent.absolute()
    # Change the directory
    # \Script Outputs \ Cluster_wise_summation_files
    # print("current directory at get_cluster_file ",current_dir)
    current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est4'
    os.chdir(str(current_dir))
    # print("set directory at get_cluster_file ", current_dir)
    df = pd.read_csv(_filename)
    return df



def create_combined_graphs(_dfCluster, _dfFAC, _clustercolumn):
    df_uptfac_cluster = _dfFAC
    dffac = _dfFAC
    clustercolumn = _clustercolumn
    try:
        # get unique values
        yrs = df_uptfac_cluster['Year'].unique()
        yrs.sort()

        clusters = df_uptfac_cluster[clustercolumn].unique()
        clusters.sort()

        df_uptfac_cluster.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)

        modes = df_uptfac_cluster['Mode'].unique()
        modes.sort()

        # create charts for FACs --> this should be starting from (0,X) --> X = 1,2,3...,8
        for cluster in clusters:
            df_fltr = df_uptfac_cluster[df_uptfac_cluster[clustercolumn] == cluster]
            # df_fltr_fac = dffac[dffac[clustercolumn] == cluster]
            # Print the cluster
            col_index = df_fltr.columns.get_loc(clustercolumn)
            cluster_code = str(df_fltr.iloc[0, col_index])
            print('Cluster Code:' + str(cluster_code))
            df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
            df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)

            transparency = 0.1
            transparency = transparency
            # # Print the cluster
            # col_index_fac = df_fltr_fac.columns.get_loc(clustercolumn)
            # cluster_code_fac = str(df_fltr_fac.iloc[0, col_index_fac])
            # print('Cluster Code:' + str(cluster_code_fac))
            # df_fltr_fac['Year'] = pd.to_datetime(df_fltr_fac['Year'].astype(str), format='%Y')
            # df_fltr_mod_fac = df_fltr_fac.set_index(pd.DatetimeIndex(df_fltr_fac['Year']).year)
            x = 1
            fig, ax = plt.subplots(nrows=8, ncols=2, figsize=(18, 9), constrained_layout=True)
            for mode in modes:
                if mode == 0:
                    mode_name = "BUS"
                else:
                    mode_name = "RAIL"
                # get number of sub-plots defined - 4*2 means 4 rows having 2 graphs (each sized 18x9) in each row = 8 graphs
                df_fltr_mode = df_fltr_mod[df_fltr_mod.Mode == mode]
                # Year vs UPT_ADJ_Total_FAC_cumsum --> Graph (0,1)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ_Total_FAC_cumsum',
                                                  label='Hypothezized rdrship if no changes in total FACs',
                                                  ax=ax[0][1], legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Rdrship', ax=ax[0][1],
                                                  legend=True, color='black', linewidth=2)
                # Paint the area
                ax[0][1].fill_between(df_fltr_mode['Year'].values, df_fltr_mode['UPT_ADJ_Total_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[
                                          'UPT_ADJ_Total_FAC_cumsum'].values,
                                      facecolor='red', interpolate=True, alpha=transparency)
                ax[0][1].fill_between(df_fltr_mode['Year'].values, df_fltr_mode['UPT_ADJ_Total_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[
                                          'UPT_ADJ_Total_FAC_cumsum'].values,
                                      facecolor='green', interpolate=True, alpha=transparency)
                ax[0][1].set(xlabel="Years", ylabel='Ridership')
                ax[0][1].legend(loc='best')
                ax[0][1].set_autoscaley_on(False)
                try:
                    ax[0][1].grid(True)
                    ax[0][1].margins(0.20)
                    ax[0][1].set_ylim([0, max(df_fltr_mode[['UPT_ADJ', 'UPT_ADJ_Total_FAC_cumsum']].values.max(1))])
                except ValueError:
                    pass

                # Year vs POP_EMP_log_FAC_cumsum --> Graph (0,2)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ_POP_EMP_log_FAC_cumsum',
                                                  label='Hypothezized rdrship if no changes in population & employment',
                                                  ax=ax[1][1], legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Rdrship', ax=ax[1][1],
                                                  legend=True, color='black', linewidth=2)
                # Paint the area
                ax[1][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[
                                          'UPT_ADJ_POP_EMP_log_FAC_cumsum'].values,
                                      facecolor='red', interpolate=True, alpha=transparency)
                ax[1][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[
                                          'UPT_ADJ_POP_EMP_log_FAC_cumsum'].values,
                                      facecolor='green', interpolate=True, alpha=transparency)
                ax[1][1].set(xlabel="Years", ylabel='Ridership')
                ax[1][1].legend(loc='best')
                ax[1][1].set_autoscaley_on(False)
                try:
                    ax[1][1].grid(True)
                    ax[1][1].margins(0.20)
                    ax[1][1].set_ylim(
                        [0, max(df_fltr_mode[['UPT_ADJ', 'UPT_ADJ_POP_EMP_log_FAC_cumsum']].values.max(1))])
                except ValueError:
                    pass

                # Year vs UPT_ADJ_TSD_POP_PCT_FAC_cumsum --> Graph (0,3)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ_TSD_POP_PCT_FAC_cumsum',
                                                  label='Hypothezized rdrship if no change in TSD Pop', ax=ax[2][1],
                                                  legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Rdrship', legend=True,
                                                  ax=ax[2][1], color='black', linewidth=2)
                # Paint the area
                ax[2][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[
                                          'UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values,
                                      facecolor='red', interpolate=True, alpha=transparency)
                ax[2][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[
                                          'UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values,
                                      facecolor='green', interpolate=True, alpha=transparency)
                ax[2][1].set(xlabel="Years", ylabel='Ridership')
                ax[2][1].legend(loc='best')
                ax[2][1].set_autoscaley_on(False)
                try:
                    ax[2][1].grid(True)
                    ax[2][1].margins(0.20)
                    ax[2][1].set_ylim(
                        [0, max(df_fltr_mode[['UPT_ADJ', 'UPT_ADJ_TSD_POP_PCT_FAC_cumsum']].values.max(1))])
                except ValueError:
                    pass

                # Year vs UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum --> Graph (0,4)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
                                                  label='Hypothezized rdrship if no change in PCT HH NO VEH',
                                                  ax=ax[3][1], legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Rdrship', ax=ax[3][1],
                                                  legend=True,
                                                  color='black', linewidth=2)
                # Paint the area
                ax[3][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[
                                          'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values,
                                      facecolor='red', interpolate=True, alpha=transparency)
                ax[3][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[
                                          'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values,
                                      facecolor='green', interpolate=True, alpha=transparency)
                ax[3][1].set(xlabel="Years", ylabel='Ridership')
                ax[3][1].legend(loc='best')
                ax[3][1].set_autoscaley_on(False)
                try:
                    ax[3][1].grid(True)
                    ax[3][1].margins(0.20)
                    ax[3][1].set_ylim(
                        [0, max(df_fltr_mode[['UPT_ADJ', 'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum']].values.max(1))])
                except ValueError:
                    pass

                # Year vs UPT_ADJ_VRM_ADJ_log_FAC_cumsum --> Graph (0,5)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ_VRM_ADJ_log_FAC_cumsum',
                                                  label='Hypothezized rdrship if no change in VRMs',
                                                  ax=ax[4][1], legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Rdrship', ax=ax[4][1],
                                                  legend=True,
                                                  color='black', linewidth=2)
                # Paint the area
                ax[4][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[
                                          'UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values,
                                      facecolor='red', interpolate=True, alpha=transparency)
                ax[4][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[
                                          'UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values,
                                      facecolor='green', interpolate=True, alpha=transparency)
                ax[4][1].set(xlabel="Years", ylabel='Ridership')
                ax[4][1].legend(loc='best')
                ax[4][1].set_autoscaley_on(False)
                try:
                    ax[4][1].grid(True)
                    ax[4][1].margins(0.20)
                    ax[4][1].set_ylim(
                        [0, max(df_fltr_mode[['UPT_ADJ', 'UPT_ADJ_VRM_ADJ_log_FAC_cumsum']].values.max(1))])
                except ValueError:
                    pass

                # Year vs UPT_ADJ_GasPrice_log_FAC_cumsum --> Graph (0,6)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ_GasPrice_log_FAC_cumsum',
                                                  label='Hypothezized rdrship if no change in Gas Prices',
                                                  ax=ax[5][1], legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Rdrship', ax=ax[5][1],
                                                  legend=True,
                                                  color='black', linewidth=2)
                # Paint the area
                ax[5][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_GasPrice_log_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[
                                          'UPT_ADJ_GasPrice_log_FAC_cumsum'].values,
                                      facecolor='red', interpolate=True, alpha=transparency)
                ax[5][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_GasPrice_log_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[
                                          'UPT_ADJ_GasPrice_log_FAC_cumsum'].values,
                                      facecolor='green', interpolate=True, alpha=transparency)
                ax[5][1].set(xlabel="Years", ylabel='Ridership')
                ax[5][1].legend(loc='best')
                ax[5][1].set_autoscaley_on(False)
                try:
                    ax[5][1].grid(True)
                    ax[5][1].margins(0.20)
                    ax[5][1].set_ylim(
                        [0, max(df_fltr_mode[['UPT_ADJ', 'UPT_ADJ_GasPrice_log_FAC_cumsum']].values.max(1))])
                except ValueError:
                    pass

                # Year vs UPT_ADJ_FARE_per_UPT_log_FAC_cumsum --> Graph (0,7)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ_FARE_per_UPT_log_FAC_cumsum',
                                                  label='Hypothezized rdrship if no change in UPTs',
                                                  ax=ax[6][1], legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Rdrship', ax=ax[6][1],
                                                  legend=True, color='black', linewidth=2)
                # Paint the area
                ax[6][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[
                                          'UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values,
                                      facecolor='red', interpolate=True, alpha=transparency)
                ax[6][1].fill_between(df_fltr_mode['Year'].values,
                                      df_fltr_mode['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[
                                          'UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values,
                                      facecolor='green', interpolate=True, alpha=transparency)
                ax[6][1].set(xlabel="Years", ylabel='Ridership')
                ax[6][1].legend(loc='best')
                ax[6][1].set_autoscaley_on(False)
                try:
                    ax[6][1].grid(True)
                    ax[6][1].margins(0.20)
                    ax[6][1].set_ylim(
                        [0, max(df_fltr_mode[['UPT_ADJ', 'UPT_ADJ_FARE_per_UPT_log_FAC_cumsum']].values.max(1))])
                except ValueError:
                    pass
                # create chart for the cluster file
                # try:
                #     df_fltr_mode_fac = df_fltr_mod_fac[df_fltr_mod_fac.Mode == mode]
                #     # Year vs Total_FAC_Scaled --> Graph (0,0)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_Total_FAC_cumsum',
                #                                           label='Hypthoteical rdrship',
                #                                           ax=ax[0][0], legend=True, color='', linewidth=3)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='Observed Rdrshp', label='UPT_ADJ', ax=ax[0][0],
                #                                           legend=True,
                #                                           color='black', linewidth=3)
                #     ax[0][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_Total_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_Total_FAC_cumsum'].values >= df_fltr_mode_fac[
                #                               'UPT_ADJ'].values,
                #                           facecolor='green', interpolate=True, alpha=0.3)
                #     ax[0][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_Total_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_Total_FAC_cumsum'].values < df_fltr_mode_fac[
                #                               'UPT_ADJ'].values,
                #                           facecolor='red', interpolate=True, alpha=0.3)
                #     ax[0][0].set(xlabel="Years", ylabel='Total_FAC')
                #     ax[0][0].legend(loc='best')
                #
                #     # Year vs Total_FAC_Scaled --> Graph (1,0)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_POP_EMP_log_FAC_cumsum',
                #                                           label='UPT_ADJ - POP_EMP_log_FAC_cumsum', ax=ax[1][0],
                #                                           legend=True)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[1][0],
                #                                           legend=True)
                #     ax[1][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values >=
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
                #     ax[1][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values <
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
                #     ax[1][0].set(xlabel="Years", ylabel='POP_EMP')
                #     ax[1][0].legend(loc='best')
                #
                #     # Year vs Total_FAC_Scaled --> Graph (2,0)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_TSD_POP_PCT_FAC_cumsum',
                #                                           label='UPT_ADJ - TSD_POP_PCT_FAC_cumsum', ax=ax[2][0],
                #                                           legend=True)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[2][0],
                #                                           legend=True)
                #     ax[2][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values >=
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
                #     ax[2][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values <
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
                #     ax[2][0].set(xlabel="Years", ylabel='TSD_POP_PCT')
                #     ax[2][0].legend(loc='best')
                #
                #     # Year vs Total_FAC_Scaled --> Graph (3,0)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
                #                                           label='UPT_ADJ - TSD_POP_PCT_FAC_cumsum', ax=ax[3][0],
                #                                           legend=True)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[3][0],
                #                                           legend=True)
                #     ax[3][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values >=
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
                #     ax[3][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values <
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
                #     ax[3][0].set(xlabel="Years", ylabel='PCT_HH_NO_VEH')
                #     ax[3][0].legend(loc='best')
                #
                #     # Year vs Total_FAC_Scaled --> Graph (4,0)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_VRM_ADJ_log_FAC_cumsum',
                #                                           label='UPT_ADJ - VRM_ADJ_log_FAC_cumsum', ax=ax[4][0],
                #                                           legend=True)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[4][0],
                #                                           legend=True)
                #     ax[4][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values >=
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
                #     ax[4][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values <
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
                #     ax[4][0].set(xlabel="Years", ylabel='VRM_ADJ')
                #     ax[4][0].legend(loc='best')
                #
                #     # Year vs Total_FAC_Scaled --> Graph (5,0)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_GasPrice_log_FAC_cumsum',
                #                                           label='UPT_ADJ - GasPrice_log_FAC_cumsum', ax=ax[5][0],
                #                                           legend=True)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[5][0],
                #                                           legend=True)
                #     ax[5][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_GasPrice_log_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_GasPrice_log_FAC_cumsum'].values >=
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
                #     ax[5][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_GasPrice_log_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_GasPrice_log_FAC_cumsum'].values <
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
                #     ax[5][0].set(xlabel="Years", ylabel='GasPrice')
                #     ax[5][0].legend(loc='best')
                #
                #     # Year vs Total_FAC_Scaled --> Graph (6,0)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_FARE_per_UPT_log_FAC_cumsum',
                #                                           label='UPT_ADJ - FARE_per_UPT_log_FAC_cumsum', ax=ax[6][0],
                #                                           legend=True)
                #     df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[6][0],
                #                                           legend=True)
                #     ax[6][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values >=
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
                #     ax[6][0].fill_between(df_fltr_mode_fac['Year'].values,
                #                           df_fltr_mode_fac['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values,
                #                           df_fltr_mode_fac['UPT_ADJ'].values,
                #                           where=df_fltr_mode_fac['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values <
                #                                 df_fltr_mode_fac[
                #                                     'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
                #     ax[6][0].set(xlabel="Years", ylabel='FARE_per_UPT')
                #     ax[6][0].legend(loc='best')
                # except ValueError:
                #     pass

                # save the plot
            fig.suptitle(('Cluster Code:' + str(clustercolumn) + "-" + str(mode_name)), fontsize=14)
            # fig.tight_layout()
            _figno = x
            # get the abs path of the directory of the code/script
            # Factors and Ridership Data\ code
            current_dir = Path(__file__).parent.absolute()
            # Change the directory
            # \Model Estimation\Est4
            # print("current directory at get_cluster_file ",current_dir)
            current_dir = current_dir.parents[0] / 'Script Outputs' / 'Combined'
            os.chdir(str(current_dir))
            print("Current set directory: ", current_dir)
            fig.savefig(("Fig " + str(_figno) + "-" + clustercolumn + " - " + mode_name + ".png"))
            plt.suptitle(clustercolumn, fontsize=14)
            plt.close(fig)
            x += 1
    finally:
        pass

def main():
    # create function to prepare charts
    dfgt11 = get_cluster_file("CLUSTER_GT_NEW_11.csv")
    dfgt11.head()

    df_uptfac_gt11 = get_upt_fac_file("UPT_FAC_totals_GT_CLUSTERS.csv")
    df_uptfac_gt11.head()

    variablename = 'CLUSTER_GT_NEW_11'

    create_combined_graphs(dfgt11, df_uptfac_gt11, 'CLUSTER_GT_NEW_11')
    print('complete')
    # dfGT8 = get_cluster_file("CLUSTER_GT_8_GROUPS.csv")
    # df_UPTFAC_GT8 = get_UPT_FAC_file("FAC_totals_gt_grouped_CLUSTERS.csv")
    #
    # dfAPTA = get_cluster_file("CLUSTER_APTA.csv")
    # df_UPTFAC_APTA = get_UPT_FAC_file("FAC_totals_gt_grouped_CLUSTERS.csv")


if __name__ == "__main__":
    main()

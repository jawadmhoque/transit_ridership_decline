# import packages for the file usage
import os.path
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os


def prepare_charts(_df_org, _clustername, _filename, _startyear, _endyear):
    df_org = _df_org
    clustercolumn = _clustername
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    modes = df_org['Mode'].unique()
    modes.sort()
    figcounter = 1
    chartcols = ['UPT_ADJ_VRM_ADJ_log_FAC_cumsum', 'UPT_ADJ_FARE_per_UPT_2018_log_FAC_cumsum',
                 'UPT_ADJ_POP_EMP_log_FAC_cumsum', 'UPT_ADJ_GAS_PRICE_2018_log_FAC_cumsum',
                 'UPT_ADJ_TOTAL_MED_INC_INDIV_2018_log_FAC_cumsum',
                 'UPT_ADJ_Tot_NonUSA_POP_pct_FAC_cumsum', 'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
                 'UPT_ADJ_TSD_POP_PCT_FAC_cumsum', 'UPT_ADJ_JTW_HOME_PCT_FAC_cumsum',
                 'UPT_ADJ_RAIL_COMPETITION_FAC_cumsum', 'UPT_ADJ_YEARS_SINCE_TNC_BUS_FAC_cumsum',
                 'UPT_ADJ_YEARS_SINCE_TNC_RAIL_FAC_cumsum', 'UPT_ADJ_BIKE_SHARE_BUS_FAC_cumsum',
                 'UPT_ADJ_scooter_flag_BUS_FAC_cumsum', 'UPT_ADJ_BIKE_SHARE_RAIL_FAC_cumsum']
    subplot_labels = ['VRMs', 'Fares', 'Population & Employment', 'Gas Price (S)', 'Med Income (Individual level)',
                      'Immigrant population', '0 Veh household share', 'TSD population', 'Work from home jobs',
                      'Rail Competition', 'since TNCs services on Bus ',
                      'since TNCs services on Rail', ' of Bike Share on Bus',
                      'E-Scooters on Bus', 'E-Scooters on Rail']
    clusternumber = 1
    for cluster in clusters:
        df_fltr = df_org[df_org[clustercolumn] == cluster]
        # Print the cluster
        col_index = df_fltr.columns.get_loc(clustercolumn)
        cluster_code = str(df_fltr.iloc[0, col_index])
        print('Cluster Code:' + str(cluster_code))
        df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
        df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)
        # Initialize the figure
        plt.style.use('seaborn-darkgrid')
        # # create a color palette
        # palette = plt.get_cmap('Set1')
        # # # multiple line plot
        # # num = 0
        x = 1
        for mode in modes:
            fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(22, 11), constrained_layout=False)
            if mode == 0:
                mode_name = "BUS"
            else:
                mode_name = "RAIL"
            df_fltr_mode = df_fltr_mod[df_fltr_mod.Mode == mode]
            col = 0
            row = 0
            transparency = 0.3
            num = 0
            for chartcol, subplotlable in zip(chartcols, subplot_labels):
                df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
                                                  label='Hypothezized rdrship if no changes in ' + str(subplotlable),
                                                  ax=ax[row][col], legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Rdrship', ax=ax[row][col],
                                                  legend=True, color='black', linewidth=2.4)
                # labelsize
                # ax[row][col].legend(fontsize=2)
                # Paint the area
                ax[row][col].fill_between(df_fltr_mode['Year'].values, df_fltr_mode[chartcol].values,
                                          df_fltr_mode['UPT_ADJ'].values,
                                          where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[chartcol].values,
                                          facecolor='green', interpolate=True, alpha=transparency)
                ax[row][col].fill_between(df_fltr_mode['Year'].values, df_fltr_mode[chartcol].values,
                                          df_fltr_mode['UPT_ADJ'].values,
                                          where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[chartcol].values,
                                          facecolor='red', interpolate=True, alpha=transparency)
                # ax[row][col].set(xlabel="Years", ylabel='Ridership')
                ax[row][col].legend(loc='best', fontsize=6)
                ax[row][col].set_autoscaley_on(False)
                try:
                    ax[row][col].grid(True)
                    ax[row][col].margins(0.20)
                    min_val = min(df_fltr_mode[['UPT_ADJ', chartcol]].values.min(1))
                    max_val = max(df_fltr_mode[['UPT_ADJ', chartcol]].values.max(1))
                    ax[row][col].set_ylim([min_val * 0.5, max_val * 1.25])
                    # ax[row][col].set_ylim([0, (max(df_fltr_mode[['UPT_ADJ', chartcol]].values.max(1))])
                except ValueError:
                    pass
                if row >= 3:
                    row = 0
                    col += 1
                else:
                    row += 1

            for z in fig.get_axes():
                z.label_outer()

            # num += 1
            fig.suptitle(('Cluster Code: ' + str(cluster) + "-" + str(mode_name)), fontsize=12)
            # fig.tight_layout()
            _figno = x
            # get the abs path of the directory of the code/script
            # Factors and Ridership Data\ code
            current_dir = pathlib.Path(__file__).parent.absolute()
            # Change the directory
            # \Script Outputs
            # print("current directory at get_cluster_file ",current_dir)
            # change the directory to where the file would be saved
            current_dir = current_dir.parents[0] / 'Script Outputs'
            os.chdir(str(current_dir))
            print("Current set directory: ", current_dir)
            outputdirectory = "Est6_Outputs"
            p = pathlib.Path(outputdirectory)
            p.mkdir(parents=True, exist_ok=True)
            current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
            os.chdir(str(current_dir))
            # Axis title
            fig.text(0.5, 0.02, 'Year', ha='center', va='center')
            fig.text(0.06, 0.5, 'Ridership', ha='center', va='center', rotation='vertical')
            figname = ("Est6 - " + str(_startyear) + "-" + str(_endyear) + " Cluster " + str(
                cluster) + "-" + mode_name + ".png")
            figcounter += 1

            fig.savefig(figname)
            # fig.savefig(("Fig " + str(clusternumber) + "-" +
            #              str(_figno) + "-" + clustercolumn + " - " + mode_name + ".png"))

            plt.suptitle(clustercolumn, fontsize=10)

            # for z in ax.flat:
            #     z.set(xlabel='Years', ylabel='Ridership')

            plt.close(fig)
            x += 1
            clusternumber += 1
    print("Success")


# def create_upt_fac_total_apta4_cluster(_filename, _clustervalue):
#     # get the abs path of the directory of the code/script
#     # Factors and Ridership Data\ code
#     current_dir = pathlib.Path(__file__).parent.absolute()
#     folder_name = chart_name = _filename.split('.')[0]
#     # Change the directory
#     # \Script Outputs \ Cluster_wise_summation_files
#     # print("current directory at get_cluster_file ",current_dir)
#     current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est6'
#     os.chdir(str(current_dir))
#     # print("set directory at get_cluster_file ", current_dir)
#     df_org = pd.read_csv(_filename)
#     # create cumulative column and update the column
#     # create new columns
#     col_name = ['VRM_ADJ_log_FAC', 'FARE_per_UPT_2018_log_FAC', 'POP_EMP_log_FAC', 'GAS_PRICE_2018_log_FAC',
#                 'TOTAL_MED_INC_INDIV_2018_log_FAC', 'Tot_NonUSA_POP_pct_FAC', 'PCT_HH_NO_VEH_FAC', 'TSD_POP_PCT_FAC',
#                 'JTW_HOME_PCT_FAC', 'RAIL_COMPETITION_FAC', 'YEARS_SINCE_TNC_BUS_FAC', 'YEARS_SINCE_TNC_RAIL_FAC',
#                 'BIKE_SHARE_BUS_FAC', 'scooter_flag_BUS_FAC', 'BIKE_SHARE_RAIL_FAC', 'Total_FAC']
#     cum_col = []
#     col_UPT_ADJ = ['UPT_ADJ']
#
#     for col in col_name:
#         df_org[str(col) + '_cumsum'] = df_org[col]
#         cum_col.append(str(col) + '_cumsum')
#
#     cluster_values = _clustervalue
#
#     # # for each cluster_id get the cumulative addition starting from 2002-->2018
#     # os.chdir(output_folder)
#     for col in cum_col:
#         df_org[col] = df_org.groupby([cluster_values, 'RAIL_FLAG'])[col].cumsum()
#
#     # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
#     for col in cum_col:
#         df_org['UPT_ADJ_' + str(col)] = df_org['UPT_ADJ'] - df_org[col]
#
#         # save the cumulative file as UPT_filename.csv
#     df_org.to_csv("UPT_" + folder_name + '.csv')
#     print("Success")
#
#     startyear = 2002
#     endyear = 2018
#     df_queried = prepare_charts_timeframe(df_org, startyear, endyear)
#     prepare_charts(df_queried, cluster_values, _filename, startyear, endyear)
#
#     startyear = 2012
#     endyear = 2018
#     df_queried = prepare_charts_timeframe(df_org, startyear, endyear)
#     prepare_charts(df_queried, cluster_values, _filename, startyear, endyear)


# def prepare_charts_timeframe(_df, _start_year, _end_year):
#     df = _df
#     startyear = _start_year
#     end_year = _end_year
#     df_fitered = df[(df.Year >= startyear) & (df.Year <= end_year)]
#     # df_queried = df.where(("Year">=str(startyear)) & ("Year"<=str(end_year)))
#     return df_fitered


def filter_dataframe(_df, _startyear, _endyear):
    df = _df
    startyear = _startyear
    end_year = _endyear
    df_fitered = df[(df.Year >= startyear) & (df.Year <= end_year)]
    # df_queried = df.where(("Year">=str(startyear)) & ("Year"<=str(end_year)))
    return df_fitered


def create_upt_fac_total_apta4_cluster_b2002(_filename, _clustervalue, _startyear, _endyear):
    # get the abs path of the directory of the code/script
    # Factors and Ridership Data\ code
    current_dir = pathlib.Path(__file__).parent.absolute()
    folder_name = chart_name = _filename.split('.')[0]
    # Change the directory
    # \Script Outputs \ Cluster_wise_summation_files
    # print("current directory at get_cluster_file ",current_dir)
    current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est6'
    os.chdir(str(current_dir))
    # print("set directory at get_cluster_file ", current_dir)
    df = pd.read_csv(_filename)
    startyear = _startyear
    endyear = _endyear
    df_org = filter_dataframe(df, startyear, endyear)
    # create cumulative column and update the column
    # create new columns
    col_name = ['VRM_ADJ_log_FAC', 'FARE_per_UPT_2018_log_FAC', 'POP_EMP_log_FAC', 'GAS_PRICE_2018_log_FAC',
                'TOTAL_MED_INC_INDIV_2018_log_FAC', 'Tot_NonUSA_POP_pct_FAC', 'PCT_HH_NO_VEH_FAC', 'TSD_POP_PCT_FAC',
                'JTW_HOME_PCT_FAC', 'RAIL_COMPETITION_FAC', 'YEARS_SINCE_TNC_BUS_FAC', 'YEARS_SINCE_TNC_RAIL_FAC',
                'BIKE_SHARE_BUS_FAC', 'scooter_flag_BUS_FAC', 'BIKE_SHARE_RAIL_FAC', 'Total_FAC']
    cum_col = []
    col_UPT_ADJ = ['UPT_ADJ']

    for col in col_name:
        df_org[str(col) + '_cumsum'] = df_org[col]
        cum_col.append(str(col) + '_cumsum')

    cluster_values = _clustervalue

    # # for each cluster_id get the cumulative addition starting from 2002-->2018
    # os.chdir(output_folder)
    for col in cum_col:
        df_org[col] = df_org.groupby([cluster_values, 'RAIL_FLAG'])[col].cumsum()

    # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
    for col in cum_col:
        df_org['UPT_ADJ_' + str(col)] = df_org['UPT_ADJ'] - df_org[col]

        # save the cumulative file as UPT_filename.csv
    df_org.to_csv("UPT_" + folder_name + "_b" + str(startyear) + '.csv')
    print("Success")

    # df_queried = prepare_charts_timeframe(df_org, startyear, endyear)
    prepare_charts(df_org, cluster_values, _filename, startyear, endyear)

    # startyear = 2012
    # endyear = 2018
    # df_queried = prepare_charts_timeframe(df_org, startyear, endyear)
    # prepare_charts(df_queried, cluster_values, _filename, startyear, endyear)


def create_upt_fac_total_apta4_b2012(_filename, _clustervalue, _startyear, _endyear):
    # get the abs path of the directory of the code/script
    # Factors and Ridership Data\ code
    current_dir = pathlib.Path(__file__).parent.absolute()
    folder_name = chart_name = _filename.split('.')[0]
    # Change the directory
    # \Script Outputs \ Cluster_wise_summation_files
    # print("current directory at get_cluster_file ",current_dir)
    current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est6'
    os.chdir(str(current_dir))
    # print("set directory at get_cluster_file ", current_dir)
    df = pd.read_csv(_filename)
    startyear = _startyear
    endyear = _endyear
    df_org = filter_dataframe(df, startyear, endyear)
    # create cumulative column and update the column
    # create new columns
    col_name = ['VRM_ADJ_log_FAC', 'FARE_per_UPT_2018_log_FAC', 'POP_EMP_log_FAC', 'GAS_PRICE_2018_log_FAC',
                'TOTAL_MED_INC_INDIV_2018_log_FAC', 'Tot_NonUSA_POP_pct_FAC', 'PCT_HH_NO_VEH_FAC', 'TSD_POP_PCT_FAC',
                'JTW_HOME_PCT_FAC', 'RAIL_COMPETITION_FAC', 'YEARS_SINCE_TNC_BUS_FAC', 'YEARS_SINCE_TNC_RAIL_FAC',
                'BIKE_SHARE_BUS_FAC', 'scooter_flag_BUS_FAC', 'BIKE_SHARE_RAIL_FAC', 'Total_FAC']
    cum_col = []
    col_UPT_ADJ = ['UPT_ADJ']

    for col in col_name:
        df_org[str(col) + '_cumsum'] = df_org[col]
        cum_col.append(str(col) + '_cumsum')

    cluster_values = _clustervalue

    # # for each cluster_id get the cumulative addition starting from 2002-->2018
    # os.chdir(output_folder)
    for col in cum_col:
        df_org[col] = df_org.groupby([cluster_values, 'RAIL_FLAG'])[col].cumsum()

    # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
    for col in cum_col:
        df_org['UPT_ADJ_' + str(col)] = df_org['UPT_ADJ'] - df_org[col]

        # save the cumulative file as UPT_filename.csv
    df_org.to_csv("UPT_" + folder_name + "_b" + str(startyear) + '.csv')
    print("Success")

    # df_queried = prepare_charts_timeframe(df_org, startyear, endyear)
    prepare_charts(df_org, cluster_values, _filename, startyear, endyear)


def main():
    # Pass on the cluster_file and cluster_column
    # create_upt_fac_total_apta4_cluster("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4")

    create_upt_fac_total_apta4_cluster_b2002("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4", 2002, 2018)
    create_upt_fac_total_apta4_b2012("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4", 2012, 2018)
    # for 2002 - 2018
    # for 2012 - 2018


if __name__ == "__main__":
    main()

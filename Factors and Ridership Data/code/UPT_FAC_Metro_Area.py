# import packages for the file usage
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import os.path
import numpy as np
import os


# def filter_dataframe(_df, _startyear, _endyear):
#     df = _df
#     startyear = _startyear
#     end_year = _endyear
#     df_fitered = df[(df.Year >= startyear) & (df.Year <= end_year)]
#     # df_queried = df.where(("Year">=str(startyear)) & ("Year"<=str(end_year)))
#     return df_fitered
#
#
# def prepare_charts(df_org, metro_area_col, startyear, endyear):
#     clustercolumn = metro_area_col
#     yrs = df_org['Year'].unique()
#     yrs.sort()
#     clusters = df_org[clustercolumn].unique()
#     clusters.sort()
#     df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
#     modes = df_org['Mode'].unique()
#     modes.sort()
#     figcounter = 1
#     clusternumber = 1
#     for cluster in clusters:
#         df_fltr = df_org[df_org[clustercolumn] == cluster]
#         # Print the cluster
#         col_index = df_fltr.columns.get_loc(clustercolumn)
#         cluster_code = str(df_fltr.iloc[0, col_index])
#         print('Cluster Code:' + str(cluster_code))
#         df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
#         df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)
#         # Initialize the figure
#         plt.style.use('seaborn-darkgrid')
#         x = 1
#         for mode in modes:
#             chartcols = ['UPT_ADJ_VRM_ADJ_log_FAC_cumsum',
#                          'UPT_ADJ_FARE_per_UPT_2018_log_FAC_cumsum',
#                          'UPT_ADJ_POP_EMP_log_FAC_cumsum',
#                          'UPT_ADJ_TSD_POP_PCT_FAC_cumsum',
#                          'UPT_ADJ_GAS_PRICE_2018_log_FAC_cumsum',
#                          'UPT_ADJ_TOTAL_MED_INC_INDIV_2018_log_FAC_cumsum',
#                          # 'UPT_ADJ_Tot_NonUSA_POP_pct_FAC_cumsum',
#                          'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
#                          'UPT_ADJ_JTW_HOME_PCT_FAC_cumsum',
#                          'UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum',
#                          'UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum',
#                          'UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum',
#                          'UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum',
#                          'UPT_ADJ_BIKE_SHARE_FAC_cumsum',
#                          'UPT_ADJ_scooter_flag_FAC_cumsum',
#                          'UPT_ADJ_Unknown_FAC_cumsum']
#             subplot_labels = ['Vehicle Revenue Miles',
#                               'Average Fares (2018$)',
#                               'Population + Employment',
#                               '% of Population in Transit Supportive Density',
#                               'Average Gas Price (2018$)',
#                               'Median Per Capita Income (2018$)',
#                               # 'Immigrant population',
#                               '% of Households with 0 Vehicles',
#                               '% Working at Home',
#                               'Years Since Ride-hail Start on Bus for High Inc/NY',
#                               'Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters',
#                               'Years Since Ride-hail Start on Rail for High Inc/NY',
#                               'Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters',
#                               'Bike Share',
#                               'Electric Scooters',
#                               'Unmeasurable variables']
#             fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(23, 16), constrained_layout=False)
#             if ((cluster == 1) or (cluster == 10)) and (mode == 0):
#                 mode_name = "BUS"
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')
#
#                 subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
#                 subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
#                 subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')
#
#             if ((cluster == 1) or (cluster == 10)) and (mode == 1):
#                 mode_name = "RAIL"
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')
#
#                 subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
#                 subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
#                 subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')
#
#             if ((cluster == 2) or (cluster == 3)) and (mode == 0):
#                 mode_name = "BUS"
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')
#
#                 subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
#                 subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')
#                 subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')
#
#             if ((cluster == 2) or (cluster == 3)) and (mode == 1):
#                 mode_name = "RAIL"
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')
#                 chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')
#
#                 subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
#                 subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')
#                 subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')
#
#             df_fltr_mode = df_fltr_mod[df_fltr_mod.Mode == mode]
#             col = 0
#             row = 0
#             transparency = 0.3
#             num = 0
#             for chartcol, subplotlable in zip(chartcols, subplot_labels):
#                 df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
#                                                   label='Hypothesized Ridership if no changes in ' +
#                                                         str(subplotlable[:27]), ax=ax[row][col], legend=True,
#                                                   fontsize=12)
#                 df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Ridership', ax=ax[row][col],
#                                                   legend=True, color='black', linewidth=2.4, fontsize=12)
#                 ax[row][col].set_xlabel(xlabel="Year", fontsize=14)
#                 ax[row][col].tick_params(labelsize=14)
#                 # Paint the area
#                 ax[row][col].fill_between(df_fltr_mode['Year'].values, df_fltr_mode[chartcol].values,
#                                           df_fltr_mode['UPT_ADJ'].values,
#                                           where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[chartcol].values,
#                                           facecolor='green', interpolate=True, alpha=transparency)
#                 ax[row][col].fill_between(df_fltr_mode['Year'].values, df_fltr_mode[chartcol].values,
#                                           df_fltr_mode['UPT_ADJ'].values,
#                                           where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[chartcol].values,
#                                           facecolor='red', interpolate=True, alpha=transparency)
#                 # ax[row][col].set(xlabel="Years", ylabel='Ridership')
#                 ax[row][col].legend(loc='best', fontsize=12)
#                 if "Ride-hail" not in subplotlable:
#                     ax[row][col].set_title(str(subplotlable), fontsize=15)
#                 else:
#                     ax[row][col].set_title(str(subplotlable[:28]), fontsize=15)
#                 ax[row][col].set_autoscaley_on(False)
#                 try:
#                     ax[row][col].grid(True)
#                     ax[row][col].margins(0.20)
#                     min_val = min(df_fltr_mode[['UPT_ADJ', chartcol]].values.min(1))
#                     max_val = max(df_fltr_mode[['UPT_ADJ', chartcol]].values.max(1))
#                     ax[row][col].set_ylim([min_val * 0.5, max_val * 1.25])
#                 except ValueError:
#                     pass
#                 if row >= 3:
#                     row = 0
#                     col += 1
#                 else:
#                     row += 1
#
#             for z in fig.get_axes():
#                 z.label_outer()
#
#             fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
#             _figno = x
#             # get the abs path of the directory of the code/script
#             # Factors and Ridership Data\ code
#             current_dir = pathlib.Path(__file__).parent.absolute()
#             # Change the directory
#             # \Script Outputs
#             # change the directory to where the file would be saved
#             current_dir = current_dir.parents[0] / 'Script Outputs'
#             os.chdir(str(current_dir))
#             print("Current set directory: ", current_dir)
#             outputdirectory = "Est7_Outputs"
#             p = pathlib.Path(outputdirectory)
#             p.mkdir(parents=True, exist_ok=True)
#             current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
#             os.chdir(str(current_dir))
#             # Axis title
#             fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
#             figlabel = "Ridership"
#             # if max(df_fltr['UPT_ADJ']) / 10 ** 9 > 0.0:
#             #     figlabel = 'Ridership (in 100 million)'
#             # else:
#             #     figlabel = 'Ridership (in 10 million)'
#
#             fig.text(0.02, 0.5, figlabel, ha='center', va='baseline', rotation='vertical',
#                      fontsize=18)
#             figname = ("Est7 - " + str(startyear) + "-" + str(endyear) + " Cluster " + str(
#                 cluster) + "-" + mode_name + ".png")
#             figcounter += 1
#             figlabel = ""
#
#             fig.savefig(figname)
#
#             plt.suptitle(clustercolumn, fontsize=18)
#
#             plt.close(fig)
#             x += 1
#             clusternumber += 1
#         print("Success")
#
#
# def create_upt_fac_metro_area(input_csv_file, filter_col, base_year, end_year):
#     # get the abs path of the directory of the code/script
#     # Factors and Ridership Data\ code
#     current_dir = pathlib.Path(__file__).parent.absolute()
#     folder_name = chart_name = input_csv_file.split('.')[0]
#     # Change the directory
#     # \Script Outputs \ Cluster_wise_summation_files
#     current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
#     os.chdir(str(current_dir))
#     df = pd.read_csv(input_csv_file)
#     startyear = base_year
#     endyear = end_year
#     df_org = filter_dataframe(df, startyear, endyear)
#     # create cumulative column and update the column
#     # create new columns
#     col_name = ['VRM_ADJ_log_FAC',
#                 'FARE_per_UPT_2018_log_FAC',
#                 'POP_EMP_log_FAC',
#                 'TSD_POP_PCT_FAC',
#                 'GAS_PRICE_2018_log_FAC',
#                 'TOTAL_MED_INC_INDIV_2018_log_FAC',
#                 # 'Tot_NonUSA_POP_pct_FAC',
#                 'PCT_HH_NO_VEH_FAC',
#                 'JTW_HOME_PCT_FAC',
#                 'YEARS_SINCE_TNC_BUS2_HINY_FAC',
#                 'YEARS_SINCE_TNC_BUS2_MIDLOW_FAC',
#                 'YEARS_SINCE_TNC_RAIL2_HINY_FAC',
#                 'YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC',
#                 'BIKE_SHARE_FAC',
#                 'scooter_flag_FAC',
#                 'Unknown_FAC']
#     cum_col = []
#     col_UPT_ADJ = ['UPT_ADJ']
#
#     cum_col = []
#     col_UPT_ADJ = ['UPT_ADJ']
#     # check for table records, wherever data is missing replace it with "0"
#     for col in col_name:
#         df[col] = np.where(df[col] == '-', 0, df[col])
#         try:
#             df[col] = df[col]
#         except ValueError:
#             pass
#
#     for col in col_name:
#         df_org[str(col) + '_cumsum'] = df_org[col]
#         cum_col.append(str(col) + '_cumsum')
#
#     metro_area_col = filter_col
#
#     # # for each cluster_id get the cumulative addition starting from 2002-->2018
#     # os.chdir(output_folder)
#     for col in cum_col:
#         df_org[col] = df_org.groupby([metro_area_col, 'RAIL_FLAG'])[col].cumsum()
#
#     # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
#     for col in cum_col:
#         df_org['UPT_ADJ_' + str(col)] = df_org['UPT_ADJ'] - df_org[col]
#
#         # save the cumulative file as UPT_filename.csv
#     df_org.to_csv("UPT_" + folder_name + "_b" + str(startyear) + '.csv')
#     print("Successfully created " + "UPT_" + folder_name + "_b" + str(startyear) + '.csv')
#     # df_queried = prepare_charts_timeframe(df_org, startyear, endyear)
#     prepare_charts(df_org, metro_area_col, startyear, endyear)

def read_the_FAC_file(file_name):
    # get the abs path of the directory of the code/script
    # Check file in Path = Factors and Ridership Data\code
    current_dir = pathlib.Path(__file__).parent.absolute()
    folder_name = file_name.split('.')[0]
    # Change the directory
    # \Script Outputs \ Cluster_wise_summation_files
    current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
    os.chdir(str(current_dir))
    try:
        if pathlib.Path(current_dir / file_name).exists():
            df = pd.read_csv(file_name)
            prepare_dataframe(df)
    except FileNotFoundError:
        print("File not found " + str(current_dir))


def get_filtered_columns():
    col_name = ["ID", "Year", "RAIL_FLAG", "CLUSTER_APTA", "UPT_ADJ",
                'VRM_ADJ_log_FAC', 'FARE_per_UPT_2018_log_FAC', 'POP_EMP_log_FAC',
                'TSD_POP_PCT_FAC', 'GAS_PRICE_2018_log_FAC', 'TOTAL_MED_INC_INDIV_2018_log_FAC', 'PCT_HH_NO_VEH_FAC',
                'JTW_HOME_PCT_FAC', 'YEARS_SINCE_TNC_BUS_FAC', 'YEARS_SINCE_TNC_RAIL_FAC',
                'BIKE_SHARE_FAC', 'scooter_flag_FAC', 'Unknown_FAC']
    return col_name


def check_4_nullvalues(df, col_name):
    # check for table records, wherever data is missing replace it with "0"
    for col in col_name:
        df[col] = np.where(df[col] == '-', 0, df[col])
        try:
            df[col] = df[col]
        except ValueError:
            pass
    return df


def get_start_year(df):
    # get the first and last year for the current metro area
    Years = df["Year"].unique()
    # start_year = pd.to_datetime((Years[0]).astype(str), format='%Y')
    start_year = str(Years[0])
    return start_year


def get_end_year(df):
    # get the first and last year for the current metro area
    Years = df["Year"].unique()
    # end_year = pd.to_datetime((Years[-1]).astype(str), format='%Y')
    end_year = str(Years[-1])
    return end_year


def get_cumsum_fields(df, col_name):
    cum_col = []
    for col in col_name:
        if col not in ["ID", "Year", "RAIL_FLAG", "CLUSTER_APTA", "UPT_ADJ"]:
            df[str(col) + '_cumsum'] = df[col]
            cum_col.append(str(col) + '_cumsum')
    # for each cluster_id get the cumulative addition starting from 2002-->2018
    for col in cum_col:
        df[col] = df[col].cumsum()
    # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
    for col in cum_col:
        df['UPT_ADJ_' + str(col)] = df['UPT_ADJ'] - df[col]
    return df


def prepare_dataframe(df):
    # combine Bus and Rail values
    df['YEARS_SINCE_TNC_BUS_FAC'] = df['YEARS_SINCE_TNC_BUS2_HINY_FAC'] + df['YEARS_SINCE_TNC_BUS2_MIDLOW_FAC']
    df['YEARS_SINCE_TNC_RAIL_FAC'] = df['YEARS_SINCE_TNC_RAIL2_HINY_FAC'] + df['YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC']
    col_name = get_filtered_columns()
    df = df.loc[:, col_name]
    # replace the null values with 0
    df = check_4_nullvalues(df, col_name)
    metro_names = df['ID'].unique()
    for metro in metro_names:
        # if metro == "New York-Northern New Jersey-Long Island, NY-NJ-PA Metro Area-Bus":
        file_name = str(metro)
        df_filter = df[df.ID == str(metro)]
        df_filter = get_cumsum_fields(df_filter, col_name)
        df_filter.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
        start_year = get_start_year(df_filter)
        end_year = get_end_year(df_filter)
        df_filter.to_csv(metro+".csv")
        prepare_chart(df_filter, start_year, end_year, file_name)


def prepare_chart(df, start_year, end_year, file_name):
    df['Year'] = pd.to_datetime(df['Year'].astype(str), format='%Y')
    df = df.set_index(pd.DatetimeIndex(df['Year']).year)
    modes = df['Mode'].unique()
    plt.style.use('seaborn-darkgrid')
    for mode in modes:
        chartcols = ['UPT_ADJ_VRM_ADJ_log_FAC_cumsum',
                     'UPT_ADJ_FARE_per_UPT_2018_log_FAC_cumsum',
                     'UPT_ADJ_POP_EMP_log_FAC_cumsum',
                     'UPT_ADJ_TSD_POP_PCT_FAC_cumsum',
                     'UPT_ADJ_GAS_PRICE_2018_log_FAC_cumsum',
                     'UPT_ADJ_TOTAL_MED_INC_INDIV_2018_log_FAC_cumsum',
                     # 'UPT_ADJ_Tot_NonUSA_POP_pct_FAC_cumsum',
                     'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
                     'UPT_ADJ_JTW_HOME_PCT_FAC_cumsum',
                     'UPT_ADJ_YEARS_SINCE_TNC_BUS_FAC_cumsum',
                     'UPT_ADJ_YEARS_SINCE_TNC_RAIL_FAC_cumsum',
                     'UPT_ADJ_BIKE_SHARE_FAC_cumsum',
                     'UPT_ADJ_scooter_flag_FAC_cumsum',
                     'UPT_ADJ_Unknown_FAC_cumsum']
        subplot_labels = ['Vehicle Revenue Miles',
                          'Average Fares (2018$)',
                          'Population + Employment',
                          '% of Population in Transit Supportive Density',
                          'Average Gas Price (2018$)',
                          'Median Per Capita Income (2018$)',
                          # 'Immigrant population',
                          '% of Households with 0 Vehicles',
                          '% Working at Home',
                          'Years Since Ride-hail Start on Bus',
                          'Years Since Ride-hail Start on Rail',
                          'Bike Share',
                          'Electric Scooters',
                          'Unmeasurable variables']
        df_fltr_mode = df[df.Mode == mode]
        col = 0
        row = 0
        transparency = 0.3
        num = 0
        # if df_fltr_mode.loc[0,'UPT_ADJ'] is not != 0:
        fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(22, 19), sharex=True, sharey=True,
                               constrained_layout=False, squeeze=False)
        # fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(22, 19), constrained_layout=False, squeeze=False)
        if mode == 0:
            chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL_FAC_cumsum')
            subplot_labels.remove('Years Since Ride-hail Start on Rail')
        else:
            chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS_FAC_cumsum')
            subplot_labels.remove('Years Since Ride-hail Start on Bus')

        for chartcol, subplotlable in zip(chartcols, subplot_labels):
            df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
                                              label='Hypothesized Ridership if no changes in ' + str(
                                                  subplotlable[:27]),
                                              ax=ax[row][col], legend=True,
                                              fontsize=12, linewidth=2.5)
            df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ',
                                              label='Observed Ridership',
                                              ax=ax[row][col], legend=True,
                                              color='black',
                                              fontsize=12, linewidth=2.5)
            # Paint the area
            ax[row][col].fill_between(df_fltr_mode['Year'].values, df_fltr_mode[chartcol].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[chartcol].values,
                                      facecolor='green', interpolate=True, alpha=transparency)
            ax[row][col].fill_between(df_fltr_mode['Year'].values, df_fltr_mode[chartcol].values,
                                      df_fltr_mode['UPT_ADJ'].values,
                                      where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[chartcol].values,
                                      facecolor='red', interpolate=True, alpha=transparency)
            ax[row][col].set_xlabel(xlabel="Year", fontsize=13)
            ax[row][col].tick_params(labelsize=13)
            ax[row][col].legend(loc='best', fontsize=9)
            ax[row][col].set_title(str(subplotlable), fontsize=13)
            try:
                ax[row][col].grid(True)
                ax[row][col].margins(0.20)
                min_val = min(df_fltr_mode[['UPT_ADJ', chartcol]].values.min(1))
                max_val = max(df_fltr_mode[['UPT_ADJ', chartcol]].values.max(1))
                ax[row][col].set_ylim([min_val * 0.5, max_val * 1.25])
            except ValueError:
                pass
            if row >= 3:
                row = 0
                col += 1
            else:
                row += 1
    # remove the X and Y labels of the innermost graphs
    for z in fig.get_axes():
        z.label_outer()

    fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
    current_dir = pathlib.Path(__file__).parent.absolute()
    # Change the directory to ..\Script Outputs
    current_dir = current_dir.parents[0] / 'Script Outputs'
    os.chdir(str(current_dir))
    # outputdirectory = "Est7_Outputs/Metro_Area"
    outputdirectory = "Est7_Outputs/without_scale"
    p = pathlib.Path(outputdirectory)
    p.mkdir(parents=True, exist_ok=True)
    current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
    os.chdir(str(current_dir))
    # Axis title
    figlabel = ""
    fig.set_size_inches(16.53, 11.69)
    fig.text(0.02, 0.5, figlabel, ha='center', va='baseline', rotation='vertical',
             fontsize=16)
    figname = ("UPT_FAC - " + "b" + str(start_year) + " - " + str(file_name) + ".png")
    fig.savefig(figname)
    plt.suptitle(file_name, fontsize=15)
    plt.close(fig)
    print("Successfully created")


def main():
    # get the UPT_FAC files created according to the base year
    # # # # # # # # #  base year 2002
    # create_upt_fac_metro_area("FAC.csv", "ID", 2002, 2018)
    read_the_FAC_file("FAC.csv")


if __name__ == "__main__":
    main()

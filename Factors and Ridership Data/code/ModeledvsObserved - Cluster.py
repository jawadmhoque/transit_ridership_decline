# import packages for the file usage
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import os.path
import numpy as np
import os
from tqdm import tqdm
import time
import shutil

'''
The purpose of the script is to generate charts for each metro area 
The input file is Model Estimation/EstXX where XX is the Model Estimation version/trial
There are two output file
    1. Excel file 
    2. Charts
Entry point of the script is the main function
Req: Use a template.xlsx saved in the Template folder
'''


def check_nullvalues(df, col_name):
    # check for table records, wherever data is missing replace it with "0"
    df = df.copy()
    for col in col_name:
        df[col] = np.where(df[col] == '-', 0, df[col])
        df[col] = df[col].replace(np.nan, 0)
        try:
            df[col] = df[col]
        except ValueError:
            pass
    return df


def get_startyear(df):
    # get the first and last year for the current metro area
    Years = df["Year"].unique()
    # start_year = pd.to_datetime((Years[0]).astype(str), format='%Y')
    start_year = str(Years[0])
    return start_year


def get_endyear(df):
    # get the first and last year for the current metro area
    Years = df["Year"].unique()
    # end_year = pd.to_datetime((Years[-1]).astype(str), format='%Y')
    end_year = str(Years[-1])
    return end_year


def get_cumsumfields(df, col_name):
    df = df.copy()
    cum_col = []
    for col in col_name:
        if col not in ["Year", "RAIL_FLAG", "CLUSTER_APTA4", "UPT_ADJ"]:
            df[str(col) + '_cumsum'] = df[col]
            cum_col.append(str(col) + '_cumsum')
    # for each cluster_id get the cumulative addition starting from 2002-->2018
    for col in cum_col:
        df[col] = df[col].cumsum()
    # convert the million values to smaller units
    for col in cum_col:
        df[col] = df[col] / 100000000
    df['UPT_ADJ'] = df['UPT_ADJ'] / 100000000
    # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
    # for col in cum_col:
    #     df['UPT_ADJ_' + str(col)] = df['UPT_ADJ'] - df[col]
    return df


def read_FACfile(file_name, file_path):
    # get the absolute path of the directory of the current script
    # Check file in Path = Factors and Ridership Data\code
    current_dir = pathlib.Path(__file__).parent.absolute()
    # change the directory where the file_name is stored
    current_dir = current_dir.parents[0] / file_path
    try:
        if pathlib.Path(current_dir / file_name).exists():
            os.chdir(str(current_dir))
            df = pd.read_csv(file_name)
            df = df.copy().loc[np.where((df.CLUSTER_APTA4 != 10))]
            df = df.reindex()
            # get the unique metro names
            clusters = df['CLUSTER_APTA4'].unique()
            for cluster in clusters:
                df_cluster = df.copy().loc[df.CLUSTER_APTA4 == cluster,:]
                modes = df_cluster['RAIL_FLAG'].unique()
                for mode in modes:
                    df_by_mode = df_cluster.copy().loc[df_cluster.RAIL_FLAG == mode,:]
                    prepare_dataframe(df_by_mode, mode, cluster)
    except FileNotFoundError:
        print("File not found " + str(current_dir))


def get_cluster_title(cluster_code):
    if cluster_code == float(1):
        cluster_title = 'High Op-Ex Group'
    elif cluster_code == float(2):
        cluster_title = 'Mid Op-Ex Group'
    elif cluster_code == float(3):
        cluster_title = 'Low Op-Ex Group'
    else:
        cluster_title = 'New York'
    return cluster_title


def prepare_dataframe(df, mode, cluster):
    col_name = get_filteredcolumns()
    df_cluster = df.copy().loc[:, col_name]

    # replace the null values with 0
    df_cluster = check_nullvalues(df_cluster, col_name)

    # merge fields "BUS" and "RAIL"
    df_cluster["VRM_ADJ_log_FAC"] = df_cluster["VRM_ADJ_BUS_log_FAC"] + df_cluster["VRM_ADJ_RAIL_log_FAC"]

    df_cluster["FARE_per_UPT_cleaned_2018_log_FAC"] = df_cluster["FARE_per_UPT_cleaned_2018_BUS_log_FAC"] + \
                                                      df_cluster["FARE_per_UPT_cleaned_2018_RAIL_log_FAC"]

    df_cluster['YEARS_SINCE_TNC'] = df_cluster["YEARS_SINCE_TNC_BUS_HINY_FAC"] + \
                                    df_cluster["YEARS_SINCE_TNC_BUS_MIDLOW_FAC"] + \
                                    df_cluster["YEARS_SINCE_TNC_RAIL_HINY_FAC"] + \
                                    df_cluster["YEARS_SINCE_TNC_RAIL_MID_FAC"]

    # add them to the col_name list
    col_name.extend(["VRM_ADJ_log_FAC", "FARE_per_UPT_cleaned_2018_log_FAC",
                     "YEARS_SINCE_TNC"])

    # now make the copy for the condensed dataframe
    df_cluster_summary = df_cluster.copy().loc[:, col_name]

    # Drop columns
    # df_cluster.drop(columns=['MAINTENANCE_WMATA_FAC', 'RESTRUCTURE_FAC', 'New_Reporter_FAC'], axis=1, inplace=True)
    #
    # # Delete the non required fields from the col_name
    # col_name.remove("VRM_ADJ_BUS_log_FAC")
    # col_name.remove("VRM_ADJ_RAIL_log_FAC")
    # col_name.remove("FARE_per_UPT_cleaned_2018_BUS_log_FAC")
    # col_name.remove("FARE_per_UPT_cleaned_2018_RAIL_log_FAC")
    # col_name.remove("YEARS_SINCE_TNC_BUS_HINY_FAC")
    # col_name.remove("YEARS_SINCE_TNC_BUS_MIDLOW_FAC")
    # col_name.remove("YEARS_SINCE_TNC_RAIL_HINY_FAC")
    # col_name.remove("YEARS_SINCE_TNC_RAIL_MID_FAC")
    # col_name.remove("MAINTENANCE_WMATA_FAC")
    # col_name.remove("RESTRUCTURE_FAC")
    # col_name.remove("New_Reporter_FAC")
    #
    # # # Create new columns
    # df_cluster_summary['Service'] = df_cluster_summary["VRM_ADJ_log_FAC"] + \
    #                                 df_cluster_summary["MAINTENANCE_WMATA_FAC"] + df_cluster_summary["RESTRUCTURE_FAC"]
    # df_cluster_summary['Land_Use'] = df_cluster_summary["POP_EMP_log_FAC"] + df_cluster_summary["TSD_POP_EMP_PCT_FAC"]
    # df_cluster_summary['Income_and_Household_Characteristics'] = df_cluster_summary[
    #                                                                  "TOTAL_MED_INC_INDIV_2018_log_FAC"] + \
    #                                                              df_cluster_summary["JTW_HOME_PCT_FAC"]
    # df_cluster_summary['New_Competing_Modes'] = df_cluster_summary["YEARS_SINCE_TNC"] + \
    #                                             df_cluster_summary["BIKE_SHARE_FAC"] + \
    #                                             df_cluster_summary["scooter_flag_FAC"]

    # summarised colcharts

    df_cluster_summary = df_cluster_summary.copy().loc[:, col_name]

    # Prepare the charts
    summary_cluster_area(df_cluster_summary, col_name, mode, cluster)


def get_filteredcolumns():
    # returns only those columns whose charts need be created
    col_name = ["Year", "RAIL_FLAG", 'UPT_ADJ',
                # "UPT_ADJ", "CLUSTER_APTA4",
                'VRM_ADJ_BUS_log_FAC', 'VRM_ADJ_RAIL_log_FAC',
                'FARE_per_UPT_cleaned_2018_BUS_log_FAC', 'FARE_per_UPT_cleaned_2018_RAIL_log_FAC',
                'POP_EMP_log_FAC', 'TSD_POP_EMP_PCT_FAC',
                'GAS_PRICE_2018_log_FAC', 'TOTAL_MED_INC_INDIV_2018_log_FAC', 'PCT_HH_NO_VEH_FAC',
                'JTW_HOME_PCT_FAC',
                'YEARS_SINCE_TNC_BUS_HINY_FAC', 'YEARS_SINCE_TNC_BUS_MIDLOW_FAC',
                'YEARS_SINCE_TNC_RAIL_HINY_FAC', 'YEARS_SINCE_TNC_RAIL_MID_FAC',
                'BIKE_SHARE_FAC', 'scooter_flag_FAC', 'Unknown_FAC',
                'MAINTENANCE_WMATA_FAC', 'RESTRUCTURE_FAC', 'New_Reporter_FAC']
    return col_name


def get_filtered_summary_columns():
    # returns only those columns whose charts need be created
    col_name = ["Year", "RAIL_FLAG", 'UPT_ADJ',
                # "CLUSTER_APTA4",
                'Service', 'Land_Use', 'FARE_per_UPT_cleaned_2018_log_FAC',
                'Income_and_Household_Characteristics', 'GAS_PRICE_2018_log_FAC',
                'New_Competing_Modes']
    return col_name


def get_modestring(mode):
    if mode == 0:
        modeName = "Bus"
    else:
        modeName = "Rail"
    return modeName


def summary_cluster_area(df, sum_col_name, mode, cluster):
    start_year = get_startyear(df)
    end_year = get_endyear(df)

    # sum all the interested columns
    df["Total"] = 0
    for col in sum_col_name:
        if col not in ["Year", "RAIL_FLAG", "CLUSTER_APTA4", "UPT_ADJ"]:
            df["Total"] += df[col]

    # only keep total column.
    sum_col_name = ["Year", "RAIL_FLAG", "CLUSTER_APTA4", "UPT_ADJ", 'Total']

    df = get_cumsumfields(df, sum_col_name)
    df.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    # Check file in Path = Factors and Ridership Data\code
    current_dir = pathlib.Path(__file__).parent.absolute()
    # Change the directory - Script Outputs\Est11_Outputs\Metro_Area_CSVs
    get_dir_path = current_dir.parents[0] / 'Script Outputs' / 'Est11_Outputs' / 'Cluster_Area_Summary_CSVs'
    # Check if the above directory path exists or not, if not then create it
    pathlib.Path(get_dir_path).mkdir(parents=True, exist_ok=True)
    os.chdir(str(get_dir_path))
    # export the metro file as CSV
    strModeName = get_modestring(mode)
    df.to_csv(get_cluster_title(cluster) + "-" + "Total - Modeled vs Observed" + "-" + strModeName + ".csv")
    chartcols = ['Total_cumsum']
    subplot_labels = ['Modeled Ridership']
    fsize = (8.3, 5.8)  # A5 page = 5.8 x 8.3 inch
    prepare_chart(df, chartcols, subplot_labels, strModeName, cluster, cols_per_fig=1, rows_per_fig=1,
                  chartsavefoldername='Cluster_Area_Summary', fig_size=fsize)
    # print("Successfully created charts for " + str(metro))
    time.sleep(0.2)


def prepare_chart(df, chartcols, subplot_labels, strModeName, cluster, cols_per_fig, rows_per_fig, chartsavefoldername,
                  fig_size):
    modes = df['Mode'].unique()
    plt.style.use('seaborn-darkgrid')
    strMode = ""
    for mode in modes:
        df_fltr_mode = df[df.Mode == mode]
        col = 0
        row = 0
        transparency = 0.4
        num = 0
        # if df_fltr_mode.loc[0,'UPT_ADJ'] is not != 0:
        if fig_size < (16.53, 11.69):
            subplot_figsize = (17, 12)
        else:
            subplot_figsize = (22, 19)
        fig, ax = plt.subplots(nrows=rows_per_fig, ncols=cols_per_fig, figsize=subplot_figsize, sharex=True,
                               sharey=True,
                               constrained_layout=False, squeeze=False)
        fig.subplots_adjust(bottom=0.15, left=0.2)
        # fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(22, 19), constrained_layout=False, squeeze=False)
        if mode == 0:
            strMode = "Bus"
        else:
            strMode = "Rail"

        # Check the first year and the last year
        start_year = df_fltr_mode['Year'].iloc[0]
        int_start_year = int(start_year)
        if int_start_year > 2006:
            base_year = 2006
            inumber = int_start_year - base_year
            for i in range(1, inumber + 1, 1):
                num = int_start_year - i
                new_row = pd.DataFrame({'Year': num, 'Mode': mode}, index=[0])
                df_fltr_mode = pd.concat([new_row, df_fltr_mode]).reset_index(drop=True)
        df_fltr_mode.loc[:, 'Year'] = pd.to_datetime(df_fltr_mode.loc[:, 'Year'].astype(str), format='%Y')
        df_fltr_mode = df_fltr_mode.set_index(pd.DatetimeIndex(df_fltr_mode['Year']).year)

        for chartcol, subplotlable in zip(chartcols, subplot_labels):
            # split the dataframe into two new dataframe. One where YR<=2012 and YR>=2012
            # This would ensure that we can generate between_fill function only for YR>=2012
            # mask = df_fltr_mode['Year'].dt.year >= int(2006)
            # df_aft_2006 = df_fltr_mode[mask]
            df_aft_2006 = df_fltr_mode.copy()

            strlabel = ""

            if "Median Per Capita Income" in subplotlable:
                strlabel = subplotlable[:33]
            elif "Households with 0 Vehicles" in subplotlable:
                strlabel = subplotlable[:31]
            elif "Income & Household Characteristics" in subplotlable:
                strlabel = subplotlable
            else:
                strlabel = subplotlable[:27]

            df_aft_2006.groupby('Mode').plot(x='Year', y='UPT_ADJ',
                                             label='Observed Ridership',
                                             ax=ax[row][col], legend=True,
                                             color='black',
                                             fontsize=12, linewidth=2.5)

            df_aft_2006.groupby('Mode').plot(x='Year', y='Total_cumsum',
                                             label='Modelled Ridership',
                                             ax=ax[row][col], legend=True,
                                             color='blue',
                                             fontsize=12, linewidth=2.5)

            # Paint the area
            # ax[row][col].fill_between(df_aft_2006['Year'].values, df_aft_2006[chartcol].values,
            #                           df_aft_2006['UPT_ADJ'].values,
            #                           where=df_aft_2006['UPT_ADJ'].values > df_aft_2006[chartcol].values,
            #                           facecolor='green', interpolate=True, alpha=transparency,
            #                           label=('Increases due to changes in ' + str(strlabel)))
            # ax[row][col].fill_between(df_aft_2006['Year'].values, df_aft_2006[chartcol].values,
            #                           df_aft_2006['UPT_ADJ'].values,
            #                           where=df_aft_2006['UPT_ADJ'].values <= df_aft_2006[chartcol].values,
            #                           facecolor='red', interpolate=True, alpha=transparency,
            #                           label=('Decreases due to changes in ' + str(strlabel)))

            ax[row][col].set_xlabel(xlabel="Year", fontsize=10)
            ax[row][col].tick_params(labelsize=9, pad=6)
            ax[row][col].set_ylabel(ylabel="Annual Ridership (100 millions)", fontsize=10)
            ax[row][col].tick_params(labelsize=9, pad=6)
            ax[row][col].legend(loc=3, fontsize=9)
            ax[row][col].set_title(str(subplotlable), fontsize=12, loc='center', fontweight='bold')
            # y = 1.0, pad = -14,
            try:
                ax[row][col].grid(True)
                ax[row][col].margins(0.20)
                max_val = np.nanmax(df_aft_2006[['UPT_ADJ', chartcol]])
                ax[row][col].set_ylim([0, max_val * 1.25])
            except ValueError:
                pass
            if row >= (rows_per_fig - 1):
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
    outputdirectory = "Est11_Outputs/" + chartsavefoldername
    p = pathlib.Path(outputdirectory)
    p.mkdir(parents=True, exist_ok=True)
    current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
    os.chdir(str(current_dir))
    # Axis title
    figlabel = ""
    fig.set_size_inches(fig_size)
    fig.text(0.02, 0.5, figlabel, ha='center', va='baseline', rotation='vertical',
             fontsize=16)
    # (cluster_chart) + "-" + strMode
    figname = (get_cluster_title(cluster) + " - " + "Observed vs Modelled Ridership - " + strModeName + ".png")
    fig.suptitle((get_cluster_title(cluster) + " - " + "Observed vs Modelled Ridership - " + strModeName), fontsize=16, y=0.98,
                 fontweight='bold', )
    make_space_above(ax, topmargin=1)
    # plt.suptitle((str(file_name) + " - " + strMode), fontsize=15)
    fig.savefig(figname)
    plt.close(fig)
    # print("Successfully created")


def make_space_above(axes, topmargin=1):
    """ increase figure size to make topmargin (in inches) space for
        titles, without changing the axes sizes"""
    fig = axes.flatten()[0].figure
    s = fig.subplotpars
    w, h = fig.get_size_inches()

    figh = h - (1 - s.top) * h + topmargin
    fig.subplots_adjust(bottom=s.bottom * h / figh, top=1 - topmargin / figh)
    fig.set_figheight(figh)


def main():
    file_path = 'Model Estimation/Est11'
    file_name = 'FAC_APTA4_CLUSTERS_11-19.csv'
    read_FACfile(file_name, file_path)
    print("completed")


if __name__ == "__main__":
    main()

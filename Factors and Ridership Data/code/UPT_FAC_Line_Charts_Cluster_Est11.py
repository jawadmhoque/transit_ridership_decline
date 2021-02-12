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
        # df[col] = df[col].cumsum()
        # get the cumulative value at this column, ignore first row values
        # df[col] = df[col].cumsum().shift().fillna(0)
        # current csv has inbuilt first row values truncated to zero, so using only cumsum
        # if this is not the case use df[col] = df[col].cumsum().shift().fillna(0)
        df[col] = df[col].cumsum()
    # convert the million values to smaller units
    for col in cum_col:
        df[col] = df[col] / 1000000
    df['UPT_ADJ'] = df['UPT_ADJ'] / 1000000
    # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
    for col in cum_col:
        df['UPT_ADJ_' + str(col)] = df['UPT_ADJ'] - df[col]
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
            # Remove "/" from Louisville otherwise it gives error later
            # df['ID'] = df['ID'].apply(lambda x: x.replace("Louisville/Jefferson County, KY-IN Metro Area-Bus",
            # "Louisville,Jefferson County, KY-IN Metro Area-Bus"))
            prepare_dataframe(df)

    except FileNotFoundError:
        print("File not found " + str(current_dir))

def get_cluster_title(cluster_code):
    if cluster_code==float(1):
        cluster_title = 'High Op-Ex Group'
    elif cluster_code==float(2):
        cluster_title = 'Mid Op-Ex Group'
    elif cluster_code==float(3):
        cluster_title = 'Low Op-Ex Group'
    else:
        cluster_title = 'New York'
    return cluster_title

def prepare_dataframe(df, i=None):
    col_name = get_filteredcolumns()
    df_cluster = df.copy().loc[:, col_name]

    # replace the null values with 0
    df_cluster = check_nullvalues(df_cluster, col_name)

    # merge fields "BUS" and "RAIL"
    df_cluster["VRM_ADJ_log_FAC"] = df_cluster["VRM_ADJ_BUS_log_FAC"] + df_cluster["VRM_ADJ_RAIL_log_FAC"]
    df_cluster["FARE_per_UPT_cleaned_2018_log_FAC"] = df_cluster["FARE_per_UPT_cleaned_2018_BUS_log_FAC"] + \
                                                    df_cluster["FARE_per_UPT_cleaned_2018_RAIL_log_FAC"]
    # df["YEARS_SINCE_TNC_BUS_FAC"] = df["YEARS_SINCE_TNC_BUS_HINY_FAC"] + df["YEARS_SINCE_TNC_BUS_MIDLOW_FAC"]
    # df['YEARS_SINCE_TNC_RAIL_FAC'] = df["YEARS_SINCE_TNC_RAIL_HINY_FAC"] + df["YEARS_SINCE_TNC_RAIL_MID_FAC"]
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
    df_cluster.drop(columns=['MAINTENANCE_WMATA_FAC', 'RESTRUCTURE_FAC', 'New_Reporter_FAC'], axis=1, inplace=True)
    # Delete the non required fields from the col_name
    col_name.remove("VRM_ADJ_BUS_log_FAC")
    col_name.remove("VRM_ADJ_RAIL_log_FAC")
    col_name.remove("FARE_per_UPT_cleaned_2018_BUS_log_FAC")
    col_name.remove("FARE_per_UPT_cleaned_2018_RAIL_log_FAC")
    col_name.remove("YEARS_SINCE_TNC_BUS_HINY_FAC")
    col_name.remove("YEARS_SINCE_TNC_BUS_MIDLOW_FAC")
    col_name.remove("YEARS_SINCE_TNC_RAIL_HINY_FAC")
    col_name.remove("YEARS_SINCE_TNC_RAIL_MID_FAC")
    col_name.remove("MAINTENANCE_WMATA_FAC")
    col_name.remove("RESTRUCTURE_FAC")
    col_name.remove("New_Reporter_FAC")

    # # Create new columns
    df_cluster_summary['Service'] = df_cluster_summary["VRM_ADJ_log_FAC"] + df_cluster_summary["MAINTENANCE_WMATA_FAC"] + \
                                  df_cluster_summary["RESTRUCTURE_FAC"]
    df_cluster_summary['Land_Use'] = df_cluster_summary["POP_EMP_log_FAC"] + df_cluster_summary["TSD_POP_EMP_PCT_FAC"]
    df_cluster_summary['Income_and_Household_Characteristics'] = df_cluster_summary["TOTAL_MED_INC_INDIV_2018_log_FAC"] + \
                                                               df_cluster_summary["JTW_HOME_PCT_FAC"]
    df_cluster_summary['New_Competing_Modes'] = df_cluster_summary["YEARS_SINCE_TNC"] + \
                                              df_cluster_summary["BIKE_SHARE_FAC"] + \
                                              df_cluster_summary["scooter_flag_FAC"]
    # summarised colcharts
    sum_col_name = get_filtered_summary_columns()
    df_cluster_summary = df_cluster_summary.copy().loc[:, sum_col_name]

    # get the unique metro names
    clusters = df_cluster['CLUSTER_APTA4'].unique()
    modes = df_cluster['RAIL_FLAG'].unique()

    # Delete if the script output folder is already existing
    # Check file in Path = Factors and Ridership Data\code
    current_dir = pathlib.Path(__file__).parent.absolute()
    # get_dir_path = current_dir.parents[0] / 'Script Outputs' / 'Est11_Outputs'
    # if get_dir_path.exists() and get_dir_path.is_dir():
    #     Cluster_Path = get_dir_path / 'Cluster_Area'
    #     if Cluster_Path.exists() and Cluster_Path.is_dir():
    #         shutil.rmtree(get_dir_path / 'Cluster_Area')
    #         shutil.rmtree(get_dir_path / 'Cluster_Area_CSVs')
    #         shutil.rmtree(get_dir_path / 'Cluster_Area_Summary_CSVs')
    #         shutil.rmtree(get_dir_path / 'Cluster_Area_Summary')

    i = 0
    # get the unique metro names
    clusters = df_cluster['CLUSTER_APTA4'].unique()

    # Iterate for each unique metropolitan area and prepare charts
    for cluster in tqdm(clusters):
        df_by_cluster = df_cluster[df_cluster.CLUSTER_APTA4==cluster]
        chart_code = df_by_cluster['CLUSTER_APTA4'].iloc[0]
        cluster_chart = get_cluster_title(chart_code)
        modes = df_by_cluster['RAIL_FLAG'].unique()
        for mode in modes:
            df_cluster_mode = df_by_cluster[df_by_cluster.RAIL_FLAG==mode]
            cluster_area(cluster, df_cluster_mode, col_name,mode,cluster_chart)
            time.sleep(0.2)
    # get the unique metro names
    clusters = df_cluster_summary['CLUSTER_APTA4'].unique()
    for cluster in tqdm(clusters):
        df_summ_by_cluster = df_cluster_summary[df_cluster_summary.CLUSTER_APTA4 == cluster]
        chart_code = df_summ_by_cluster['CLUSTER_APTA4'].iloc[0]
        cluster_chart = get_cluster_title(chart_code)
        modes = df_summ_by_cluster['RAIL_FLAG'].unique()
        for mode in modes:
            df_summ_by_cluster_mode = df_summ_by_cluster[df_summ_by_cluster.RAIL_FLAG == mode]
            summary_cluster_area(cluster, df_summ_by_cluster_mode, sum_col_name,mode,cluster_chart)
            time.sleep(0.2)
    # print("Successfully created metro area based FAC Charts")


def get_filteredcolumns():
    # returns only those columns whose charts need be created
    col_name = ["Year", "RAIL_FLAG", "CLUSTER_APTA4", 'UPT_ADJ',
                # "UPT_ADJ",
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
    col_name = ["Year", "RAIL_FLAG", "CLUSTER_APTA4", 'UPT_ADJ',
                'Service', 'Land_Use', 'FARE_per_UPT_cleaned_2018_log_FAC',
                'Income_and_Household_Characteristics', 'GAS_PRICE_2018_log_FAC',
                'New_Competing_Modes']
    return col_name

def get_modestring(mode):
    if mode == 0:
        modeName="Bus"
    else:
        modeName="Rail"
    return modeName


def cluster_area(cluster, df, col_name,mode,cluster_chart):
    file_name = str(cluster)
    df_filter = df.copy()[df.CLUSTER_APTA4 == cluster]
    start_year = get_startyear(df_filter)
    end_year = get_endyear(df_filter)
    # get the first year of the cities record. If the year is before 2012, do some work
    if int(start_year) <= (2012):
        for col in col_name:
            if col not in ["Year", "RAIL_FLAG", "CLUSTER_APTA4", "UPT_ADJ"]:
                df_filter[col] = np.where(df_filter['Year'] <= int(2012), 0, df_filter[col])

    df_filter = get_cumsumfields(df_filter, col_name)
    df_filter.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    # Check file in Path = Factors and Ridership Data\code
    current_dir = pathlib.Path(__file__).parent.absolute()
    # Change the directory - Script Outputs\Est11_Outputs\Metro_Area_CSVs
    get_dir_path = current_dir.parents[0] / 'Script Outputs' / 'Est11_Outputs' / 'Cluster_Area_CSVs'
    # Check if the above directory path exists or not, if not then create it
    pathlib.Path(get_dir_path).mkdir(parents=True, exist_ok=True)
    os.chdir(str(get_dir_path))
    # export the metro file as CSV
    strModeName = get_modestring(mode)
    df_filter.to_csv("Cluster_"+str(cluster) + "-"+strModeName+ ".csv")

    chartcols = ['UPT_ADJ_VRM_ADJ_log_FAC_cumsum',
                 'UPT_ADJ_FARE_per_UPT_cleaned_2018_log_FAC_cumsum',
                 'UPT_ADJ_POP_EMP_log_FAC_cumsum',
                 'UPT_ADJ_TSD_POP_EMP_PCT_FAC_cumsum',
                 'UPT_ADJ_GAS_PRICE_2018_log_FAC_cumsum',
                 'UPT_ADJ_TOTAL_MED_INC_INDIV_2018_log_FAC_cumsum',
                 'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
                 'UPT_ADJ_JTW_HOME_PCT_FAC_cumsum',
                 # 'UPT_ADJ_YEARS_SINCE_TNC_BUS_FAC_cumsum',
                 # 'UPT_ADJ_YEARS_SINCE_TNC_RAIL_FAC_cumsum',
                 'UPT_ADJ_YEARS_SINCE_TNC_cumsum',
                 'UPT_ADJ_BIKE_SHARE_FAC_cumsum',
                 'UPT_ADJ_scooter_flag_FAC_cumsum',
                 # 'UPT_ADJ_MAINTENANCE_WMATA_FAC_cumsum',
                 # 'UPT_ADJ_RESTRUCTURE_FAC_cumsum',
                 # 'UPT_ADJ_New_Reporter_FAC_cumsum',
                 'UPT_ADJ_Unknown_FAC_cumsum']
    subplot_labels = ['Vehicle Revenue Miles',
                      'Average Fares (2018$)',
                      'Population + Employment',
                      'Density',
                      'Average Gas Price (2018$)',
                      'Median Per Capita Income (2018$)',
                      '% of Households with 0 Vehicles',
                      '% Working at Home',
                      # 'Years Since Ride-hail Start on Bus',
                      # 'Years Since Ride-hail Start on Rail',
                      'Years Since Ride-hail Start',
                      'Bike Share',
                      'Electric Scooters',
                      # 'Major Maintenance Event',
                      # 'Network Restructure',
                      # 'New_Reporters',
                      'Unmeasurable variables']
    fsize = (16.53, 11.69)
    prepare_chart(df_filter, file_name, chartcols, subplot_labels, strModeName, cluster_chart, cols_per_fig=3, rows_per_fig=4, chartsavefoldername='Cluster_Area', fig_size=fsize)
    # print("Successfully created charts for " + str(metro))
    time.sleep(0.2)


def summary_cluster_area(cluster, df, sum_col_name,mode,cluster_chart):
    file_name = str(cluster)
    df_filter = df.copy()[df.CLUSTER_APTA4 == cluster]
    start_year = get_startyear(df_filter)
    end_year = get_endyear(df_filter)
    # get the first year of the cities record. If the year is before 2012, do some work
    if int(start_year) <= (2012):
        for col in sum_col_name:
            if col not in ["Year", "RAIL_FLAG", "CLUSTER_APTA4", "UPT_ADJ"]:
                df_filter[col] = np.where(df_filter['Year'] <= int(2012), 0, df_filter[col])

    df_filter = get_cumsumfields(df_filter, sum_col_name)
    df_filter.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)

    # Check file in Path = Factors and Ridership Data\code
    current_dir = pathlib.Path(__file__).parent.absolute()
    # Change the directory - Script Outputs\Est11_Outputs\Metro_Area_CSVs
    get_dir_path = current_dir.parents[0] / 'Script Outputs' / 'Est11_Outputs' / 'Cluster_Area_Summary_CSVs'
    # Check if the above directory path exists or not, if not then create it
    pathlib.Path(get_dir_path).mkdir(parents=True, exist_ok=True)
    os.chdir(str(get_dir_path))
    # export the metro file as CSV
    strModeName = get_modestring(mode)
    df_filter.to_csv("Cluster_" + str(cluster) + "-" + strModeName + ".csv")
    chartcols = ['UPT_ADJ_Service_cumsum',
                 'UPT_ADJ_FARE_per_UPT_cleaned_2018_log_FAC_cumsum',
                 'UPT_ADJ_Land_Use_cumsum',
                 'UPT_ADJ_Income_and_Household_Characteristics_cumsum',
                 'UPT_ADJ_GAS_PRICE_2018_log_FAC_cumsum',
                 'UPT_ADJ_New_Competing_Modes_cumsum']
    subplot_labels = ['Service',
                      'Average Fares',
                      'Land Use',
                      'Income & Household Characteristics',
                      'Gas Price',
                      'New Competing Modes']
    fsize = (11.69, 16.53)
    prepare_chart(df_filter, file_name, chartcols, subplot_labels, strModeName,cluster_chart,cols_per_fig=2, rows_per_fig=3,
                  chartsavefoldername='Cluster_Area_Summary', fig_size=fsize)
    # print("Successfully created charts for " + str(metro))
    time.sleep(0.2)


def prepare_chart(df, file_name, chartcols, subplot_labels,strModeName,cluster_chart,cols_per_fig, rows_per_fig, chartsavefoldername,
                  fig_size):
    df.loc[:, 'Year'] = pd.to_datetime(df.loc[:, 'Year'].astype(str), format='%Y')
    df = df.set_index(pd.DatetimeIndex(df['Year']).year)
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

        for chartcol, subplotlable in zip(chartcols, subplot_labels):
            # Check the first year and the last year
            start_year = df_fltr_mode['Year'].iloc[0]
            int_year = start_year.year
            if int_year >2006:
                no_of_rows = int_year - 2006
                # df_fltr_modestart_year = str(Years[0]).reindex(df_fltr_mode.index.tolist() + list(range(0, no_of_rows)))

                # introduce blanks rows for year 2006 until start_year

            # split the dataframe into two new dataframe. One where YR<=2012 and YR>=2012
            # This would ensure that we can generate between_fill function only for YR>=2012
            mask = df_fltr_mode['Year'].dt.year >= int(2006)
            # df_b4_2012 = df_fltr_mode[~mask]
            df_aft_2006 = df_fltr_mode[mask]

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

            # Paint the area
            ax[row][col].fill_between(df_aft_2006['Year'].values, df_aft_2006[chartcol].values,
                                      df_aft_2006['UPT_ADJ'].values,
                                      where=df_aft_2006['UPT_ADJ'].values > df_aft_2006[chartcol].values,
                                      facecolor='green', interpolate=True, alpha=transparency,
                                      label=('Increases due to changes in ' + str(strlabel)))
            ax[row][col].fill_between(df_aft_2006['Year'].values, df_aft_2006[chartcol].values,
                                      df_aft_2006['UPT_ADJ'].values,
                                      where=df_aft_2006['UPT_ADJ'].values <= df_aft_2006[chartcol].values,
                                      facecolor='red', interpolate=True, alpha=transparency,
                                      label=('Decreases due to changes in ' + str(strlabel)))
            ax[row][col].set_xlabel(xlabel="Year", fontsize=10)
            ax[row][col].tick_params(labelsize=9, pad=6)
            ax[row][col].set_ylabel(ylabel="Annual Ridership (millions)", fontsize=10)
            ax[row][col].tick_params(labelsize=9, pad=6)
            ax[row][col].legend(loc=3, fontsize=9)
            ax[row][col].set_title(str(subplotlable), fontsize=12, loc='center', fontweight='bold')
            # y = 1.0, pad = -14,
            try:
                ax[row][col].grid(True)
                ax[row][col].margins(0.20)
                # max_val = max(df_aft_2006[['UPT_ADJ', chartcol]].values.max(1))
                # ax[row][col].set_ylim([0, max_val * 1.25])
                # min_val = np.nanmin(df_aft_2006[['UPT_ADJ', chartcol]])
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
    figname = ("UPT_FAC - " + str(file_name) +"-"+strModeName +".png")
    fig.suptitle((cluster_chart) + "-" + strMode, fontsize=16, y=0.98, fontweight='bold', )
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

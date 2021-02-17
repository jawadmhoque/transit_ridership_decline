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
            # get the unique metro names
            # clusters = df['CLUSTER_APTA4'].unique()
            modes = df['RAIL_FLAG'].unique()
            for mode in modes:
                df_by_mode = df.copy().loc[np.where((df.RAIL_FLAG == mode) & (df.CLUSTER_APTA4 != 10))]
                df_by_mode.drop(columns=['CLUSTER_APTA4', 'CLUSTER_APTA'], axis=1, inplace=True)
                df_by_mode_sum = df_by_mode.copy().groupby('Year').agg('sum').reset_index()
                df_by_mode_sum['RAIL_FLAG'] = mode
                prepare_dataframe(df_by_mode_sum, mode)

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


def prepare_dataframe(df, mode):
    col_name = get_filteredcolumns()
    df_cluster = df.copy().loc[:, col_name]

    # replace the null values with 0
    df_cluster = check_nullvalues(df_cluster, col_name)

    # Prepare the charts
    summary_cluster_area(df_cluster, col_name, mode)


def get_filteredcolumns():
    # col_name = ["Year", "RAIL_FLAG", 'UPT_ADJ',
    #             # "UPT_ADJ", "CLUSTER_APTA4", 'Unknown_FAC',
    #             'VRM_ADJ_BUS_log_FAC', 'VRM_ADJ_RAIL_log_FAC',
    #             'FARE_per_UPT_cleaned_2018_BUS_log_FAC', 'FARE_per_UPT_cleaned_2018_RAIL_log_FAC',
    #             'POP_EMP_log_FAC', 'TSD_POP_EMP_PCT_FAC',
    #             'GAS_PRICE_2018_log_FAC', 'TOTAL_MED_INC_INDIV_2018_log_FAC', 'PCT_HH_NO_VEH_FAC',
    #             'JTW_HOME_PCT_FAC',
    #             'YEARS_SINCE_TNC_BUS_HINY_FAC', 'YEARS_SINCE_TNC_BUS_MIDLOW_FAC',
    #             'YEARS_SINCE_TNC_RAIL_HINY_FAC', 'YEARS_SINCE_TNC_RAIL_MID_FAC',
    #             'BIKE_SHARE_FAC', 'scooter_flag_FAC',  'Known_FAC',
    #             'MAINTENANCE_WMATA_FAC', 'RESTRUCTURE_FAC', 'New_Reporter_FAC']

    # returns only those columns whose charts need be created
    col_name = ["Year", "RAIL_FLAG", 'UPT_ADJ', 'Known_FAC', 'New_Reporter_FAC']
    return col_name


def get_modestring(mode):
    if mode == 0:
        modeName = "Bus"
    else:
        modeName = "Rail"
    return modeName


def get_pivot(df, base_year,sum_col_name):
    df = df.reset_index(drop=True).copy()
    col = "Pivot_4m_" + base_year
    df[col] = 0

    # get the index of the row corresponding to the base_year
    itr = df.index[df['Year'] == int(base_year)].to_list()
    # Set the value of the Pivot_base_year column at "itr" index-th row equal to UPT_Adj
    df.at[itr[0], col] = df["UPT_ADJ"].iloc[itr[0]]

    start_year = get_startyear(df)

    end =(int(df.index[df['Year'] == int(start_year)].to_list()[0])) - 1

    for i in range(itr[0] - 1, (int(df.index[df['Year'] == int(start_year)].to_list()[0])) - 1,-1):
        df.at[i, col] = df[col].iloc[(i+1)] - df["Known_FAC"].iloc[(i+1)] - df["New_Reporter_FAC"].iloc[(i+1)]

    end_year = get_endyear(df)

    for i in range(itr[0] + 1, (int(df.index[df['Year'] == int(end_year)].to_list()[0])+1)):
        df.at[i, col] = df[col].iloc[i - 1] + df["Known_FAC"].iloc[i] + df["New_Reporter_FAC"].iloc[i]

    # sum_col_name.append("Total")
    sum_col_name.append(col)

    # convert the readings into 100 millions
    for col in sum_col_name:
        if col not in ["Year", "RAIL_FLAG", "CLUSTER_APTA4"]:
            df[col] = df[col] / 100000000

    return df


def summary_cluster_area(df, sum_col_name, mode):
    # sum all the interested columns
    df["Total"] = 0
    for col in sum_col_name:
        if col not in ["Year", "RAIL_FLAG", "CLUSTER_APTA4", "UPT_ADJ"]:
            df["Total"] += df[col]

    sum_col_name.append("Total")

    df = get_pivot(df, '2012',sum_col_name)

    df.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    # Check file in Path = Factors and Ridership Data\code
    current_dir = pathlib.Path(__file__).parent.absolute()
    # Change the directory - Script Outputs\Est11_Outputs\Metro_Area_CSVs
    get_dir_path = current_dir.parents[0] / 'Script Outputs' / 'Est11_Outputs' / 'Total_CSVs'
    # Check if the above directory path exists or not, if not then create it
    pathlib.Path(get_dir_path).mkdir(parents=True, exist_ok=True)
    os.chdir(str(get_dir_path))
    # export the metro file as CSV
    strModeName = get_modestring(mode)
    df.to_csv("Total - Modeled vs Observed" + "-" + strModeName + ".csv")
    chartcols = ['Pivot_4m_2012']
    subplot_labels = ['Modeled Ridership']
    fsize = (8.3, 5.8)  # A5 page = 5.8 x 8.3 inch
    prepare_chart(df, chartcols, subplot_labels, strModeName, cols_per_fig=1, rows_per_fig=1,
                  chartsavefoldername='Total_Charts', fig_size=fsize)
    # print("Successfully created charts for " + str(metro))
    time.sleep(0.2)


def prepare_chart(df, chartcols, subplot_labels, strModeName, cols_per_fig, rows_per_fig, chartsavefoldername,
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

            df_aft_2006.groupby('Mode').plot(x='Year', y='Pivot_4m_2012',
                                             label='Modeled Ridership',
                                             ax=ax[row][col], legend=True,
                                             color='blue',
                                             fontsize=12, linewidth=2.5)

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
    figname = ("Observed vs Modelled Ridership across all clusters - " + strModeName + ".png")
    fig.suptitle(("Observed vs Modelled Ridership across all clusters - " + strModeName), fontsize=16, y=0.98,
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

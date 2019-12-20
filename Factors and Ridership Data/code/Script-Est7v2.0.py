# import packages for the file usage
import os.path
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from matplotlib import cycler


def filter_dataframe(_df, _startyear, _endyear):
    df = _df
    startyear = _startyear
    end_year = _endyear
    df_fitered = df[(df.Year >= startyear) & (df.Year <= end_year)]
    # df_queried = df.where(("Year">=str(startyear)) & ("Year"<=str(end_year)))
    return df_fitered


# make the charts
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
            chartcols = ['UPT_ADJ_VRM_ADJ_log_FAC_cumsum',
                         'UPT_ADJ_FARE_per_UPT_2018_log_FAC_cumsum',
                         'UPT_ADJ_POP_EMP_log_FAC_cumsum',
                         'UPT_ADJ_TSD_POP_PCT_FAC_cumsum',
                         'UPT_ADJ_GAS_PRICE_2018_log_FAC_cumsum',
                         'UPT_ADJ_TOTAL_MED_INC_INDIV_2018_log_FAC_cumsum',
                         # 'UPT_ADJ_Tot_NonUSA_POP_pct_FAC_cumsum',
                         'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
                         'UPT_ADJ_JTW_HOME_PCT_FAC_cumsum',
                         'UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum',
                         'UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum',
                         'UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum',
                         'UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum',
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
                              'Years Since Ride-hail Start on Bus for High Inc/NY',
                              'Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters',
                              'Years Since Ride-hail Start on Rail for High Inc/NY',
                              'Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters',
                              'Bike Share',
                              'Electric Scooters',
                              'Unmeasurable variables']
            fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(22, 15), constrained_layout=False)

            if ((cluster == 1) or (cluster == 10)) and (mode == 0):
                mode_name = "BUS"
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')

                subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')

            if ((cluster == 1) or (cluster == 10)) and (mode == 1):
                mode_name = "RAIL"
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')

                subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')

            if ((cluster == 2) or (cluster == 3)) and (mode == 0):
                mode_name = "BUS"
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')

                subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')
                subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')

            if ((cluster == 2) or (cluster == 3)) and (mode == 1):
                mode_name = "RAIL"
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')

                subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')
                subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')

            df_fltr_mode = df_fltr_mod[df_fltr_mod.Mode == mode]
            col = 0
            row = 0
            transparency = 0.3
            num = 0
            for chartcol, subplotlable in zip(chartcols, subplot_labels):
                df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
                                                  label='Hypothezized Ridership if no changes in ' + str(
                                                      subplotlable[:27]), ax=ax[row][col], legend=True)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Ridership', ax=ax[row][col],
                                                  legend=True, color='black', linewidth=2.4)
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
                ax[row][col].legend(loc='best', fontsize=10)
                if "Ride-hail" not in subplotlable:
                    ax[row][col].set_title(str(subplotlable))
                else:
                    ax[row][col].set_title(str(subplotlable[:28]))
                ax[row][col].set_autoscaley_on(False)
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

            for z in fig.get_axes():
                z.label_outer()

            fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
            _figno = x
            # get the abs path of the directory of the code/script
            # Factors and Ridership Data\ code
            current_dir = pathlib.Path(__file__).parent.absolute()
            # Change the directory
            # \Script Outputs
            # change the directory to where the file would be saved
            current_dir = current_dir.parents[0] / 'Script Outputs'
            os.chdir(str(current_dir))
            print("Current set directory: ", current_dir)
            outputdirectory = "Est7_Outputs"
            p = pathlib.Path(outputdirectory)
            p.mkdir(parents=True, exist_ok=True)
            current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
            os.chdir(str(current_dir))
            # Axis title
            # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
            figlabel = ""
            # if max(df_fltr['UPT_ADJ']) / 10 ** 9 > 0.0:
            #     figlabel = 'Ridership (in 100 million)'
            # else:
            #     figlabel = 'Ridership (in 10 million)'

            fig.text(0.02, 0.5, figlabel, ha='center', va='baseline', rotation='vertical',
                     fontsize=16)
            figname = ("Est7 - " + str(_startyear) + "-" + str(_endyear) + " Cluster " + str(
                cluster) + "-" + mode_name + ".png")
            figcounter += 1
            figlabel = ""

            fig.savefig(figname)

            plt.suptitle(clustercolumn, fontsize=10)

            plt.close(fig)
            x += 1
            clusternumber += 1
        print("Success")


def create_upt_fac_cluster_file(_filename, _clustervalue, _startyear, _endyear):
    # get the abs path of the directory of the code/script
    # Factors and Ridership Data\ code
    current_dir = pathlib.Path(__file__).parent.absolute()
    folder_name = chart_name = _filename.split('.')[0]
    # Change the directory
    # \Script Outputs \ Cluster_wise_summation_files
    current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
    os.chdir(str(current_dir))
    df = pd.read_csv(_filename)
    startyear = _startyear
    endyear = _endyear
    df_org = filter_dataframe(df, startyear, endyear)
    # create cumulative column and update the column
    # create new columns
    col_name = ['VRM_ADJ_log_FAC',
                'FARE_per_UPT_2018_log_FAC',
                'POP_EMP_log_FAC',
                'TSD_POP_PCT_FAC',
                'GAS_PRICE_2018_log_FAC',
                'TOTAL_MED_INC_INDIV_2018_log_FAC',
                # 'Tot_NonUSA_POP_pct_FAC',
                'PCT_HH_NO_VEH_FAC',
                'JTW_HOME_PCT_FAC',
                'YEARS_SINCE_TNC_BUS2_HINY_FAC',
                'YEARS_SINCE_TNC_BUS2_MIDLOW_FAC',
                'YEARS_SINCE_TNC_RAIL2_HINY_FAC',
                'YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC',
                'BIKE_SHARE_FAC',
                'scooter_flag_FAC',
                'Unknown_FAC']
    cum_col = []
    col_UPT_ADJ = ['UPT_ADJ']

    for col in col_name:
        df[col] = np.where(df[col] == '-', 0, df[col])
        try:
            df[col] = df[col]
        except ValueError:
            pass

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
    print("Successfully created " + "UPT_" + folder_name + "_b" + str(startyear) + '.csv')
    # df_queried = prepare_charts_timeframe(df_org, startyear, endyear)
    prepare_charts(df_org, cluster_values, _filename, startyear, endyear)


def get_cluster_chart_raw(_df, _filename, _chart_name, _clusterfile):
    df_org = _df
    filename = _filename
    chart_name = _chart_name
    clustercolumn = _clusterfile
    # get unique values
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    modes = df_org['Mode'].unique()
    modes.sort()
    mode_name = ""
    figcounter = 1
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
        fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(22, 15), constrained_layout=False)
        for mode in modes:
            chartcols = ['VRM_ADJ',
                         'FARE_per_UPT_2018',
                         'POP_EMP',
                         'TSD_POP_PCT',
                         'GAS_PRICE_2018',
                         'TOTAL_MED_INC_INDIV_2018',
                         # 'UPT_ADJ_Tot_NonUSA_POP_pct_FAC_cumsum',
                         'PCT_HH_NO_VEH',
                         'JTW_HOME_PCT',
                         'YEARS_SINCE_TNC_BUS2_HINY',
                         'YEARS_SINCE_TNC_BUS2_MIDLOW',
                         'YEARS_SINCE_TNC_RAIL2_HINY',
                         'YEARS_SINCE_TNC_RAIL2_MIDLOW',
                         'BIKE_SHARE',
                         'scooter_flag',
                         'UPT_ADJ']
            subplot_labels = ['Vehicle Revenue Miles',
                              'Average Fares (2018$)',
                              'Population + Employment',
                              '% of Population in Transit Supportive Density',
                              'Average Gas Price (2018$)',
                              'Median Per Capita Income (2018$)',
                              # 'Immigrant population',
                              '% of Households with 0 Vehicles',
                              '% Working at home',
                              'Years Since Ride-hail Start Bus HINY',
                              'Years Since Ride-hail Start Bus MIDLOW',
                              'Years Since Ride-hail Start Rail HINY',
                              'Years Since Ride-hail Start Rail MIDLOW',
                              'Bike Share',
                              'Electric Scooters',
                              'Ridership']

            # plt.xlabel('xlabel', fontsize=16)
            # plt.ylabel('ylabel', fontsize=16)

            remove_list = ['POP_EMP','GAS_PRICE_2018', 'TSD_POP_PCT', 'TOTAL_MED_INC_INDIV_2018', 'PCT_HH_NO_VEH',
                           'JTW_HOME_PCT', 'BIKE_SHARE', 'scooter_flag']

            if ((cluster == 1) or (cluster == 10)) and (mode == 0):
                mode_name = "BUS"
                chartcols.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                remove_list.append('YEARS_SINCE_TNC_BUS2_HINY')

                subplot_labels.remove('Years Since Ride-hail Start Bus MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Rail MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Rail HINY')

            if ((cluster == 1) or (cluster == 10)) and (mode == 1):
                mode_name = "RAIL"
                chartcols.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_BUS2_HINY')

                subplot_labels.remove('Years Since Ride-hail Start Bus HINY')
                subplot_labels.remove('Years Since Ride-hail Start Bus MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Rail MIDLOW')

            if ((cluster == 2) or (cluster == 3)) and (mode == 0):
                mode_name = "BUS"
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                chartcols.remove('YEARS_SINCE_TNC_BUS2_HINY')
                remove_list.append('YEARS_SINCE_TNC_BUS2_MIDLOW')

                subplot_labels.remove('Years Since Ride-hail Start Rail MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Bus HINY')
                subplot_labels.remove('Years Since Ride-hail Start Rail HINY')

            if ((cluster == 2) or (cluster == 3)) and (mode == 1):
                mode_name = "RAIL"
                chartcols.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                chartcols.remove('YEARS_SINCE_TNC_BUS2_HINY')

                subplot_labels.remove('Years Since Ride-hail Start Bus MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Bus HINY')
                subplot_labels.remove('Years Since Ride-hail Start Rail HINY')

            df_fltr_mode = df_fltr_mod[df_fltr_mod.Mode == mode]
            col = 0
            row = 0
            num = 0

            # if ((cluster == 2) or (cluster == 3) or (cluster == 10)) and (mode == 0):

            for chartcol, subplotlable in zip(chartcols, subplot_labels):
                if mode == 0 and (chartcol in remove_list):
                    pass
                else:
                    if mode == 1 and (chartcol in remove_list):
                        if chartcol == 'TOTAL_MED_INC_INDIV_2018':
                            labeltext = (str(subplotlable[0:32]))
                        else:
                            labeltext = (str(subplotlable[0:27]))
                    else:
                        labeltext = (str(subplotlable[0:27]) + ' - ' + mode_name)

                    df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
                                                      label=(labeltext),
                                                      ax=ax[row][col], legend=True)
                    ax[row][col].legend(loc='best', fontsize=10)
                    if "Ride-hail" not in subplotlable:
                        ax[row][col].set_title(str(subplotlable))
                    else:
                        ax[row][col].set_title(str(subplotlable[:28]))
                    ax[row][col].set_autoscaley_on(True)
                    try:
                        ax[row][col].grid(True)
                        ax[row][col].margins(0.20)
                        # ax[row][col].set_ylim(0, (df_fltr_mode[chartcols].max()) * 1.25)
                    except ValueError:
                        pass
                if row >= 3:
                    row = 0
                    col += 1
                else:
                    row += 1

        fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
        _figno = x
        # get the abs path of the directory of the code/script
        # Factors and Ridership Data\ code
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Change the directory
        # \Script Outputs
        # change the directory to where the file would be saved
        current_dir = current_dir.parents[0] / 'Script Outputs'
        os.chdir(str(current_dir))
        print("Current set directory: ", current_dir)
        outputdirectory = "Est7_Outputs"
        p = pathlib.Path(outputdirectory)
        p.mkdir(parents=True, exist_ok=True)
        current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
        os.chdir(str(current_dir))
        # Axis title
        # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
        figlabel = ""
        # if max(df_fltr['UPT_ADJ']) / 10 ** 9 > 0.0:
        #     figlabel = 'Ridership (in 100 million)'
        # else:
        #     figlabel = 'Ridership (in 10 million)'

        fig.text(0.02, 0.5, figlabel, ha='center', va='baseline', rotation='vertical',
                 fontsize=16)
        figname = ("Est7 - (absolute)" + " Cluster " + str(cluster) + ".png")
        figcounter += 1
        figlabel = ""

        fig.savefig(figname)

        plt.suptitle(clustercolumn, fontsize=10)

        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)


def get_cluster_file_raw(_filename, _clusterfile):
    filename = _filename
    clusterfile = _clusterfile
    try:
        chart_name = filename.split('.')[0]
        # get the absolute path of the script and then check if the csv file exists or not
        current_dir = pathlib.Path(__file__).parent.absolute()
        current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
        os.chdir(str(current_dir))
        try:
            if (current_dir / filename).is_file():
                df = pd.read_csv(filename)
                get_cluster_chart_raw(df, filename, chart_name, clusterfile)
        except FileNotFoundError:
            print("File could not be found. Please check the file is placed in the folder path - Factors and Ridership "
                  "Data\Model Estimation\Est7")
    except FileNotFoundError:
        print("System error, in cluster_level_chart_function")


def get_clusterwise_UPTs(_df, _filename, _chart_name, _clusterfile):
    try:
        df_org = _df
        filename = _filename
        chart_name = _chart_name
        clustercolumn = _clusterfile
        # get unique values
        yrs = df_org['Year'].unique()
        yrs.sort()
        clusters = df_org[clustercolumn].unique()
        clusters.sort()
        df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
        modes = df_org['Mode'].unique()
        modes.sort()
        mode_name = ""
        figcounter = 1
        clusternumber = 1
        x = 1
        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(22,15), constrained_layout=False)
        # plt.style.use('seaborn-darkgrid')
        custom_cycler = (cycler(color=['r', 'g', 'b', 'y']))
        plt.rc('lines', linewidth=2.4)
        plt.rc('axes', prop_cycle=custom_cycler)
        # mpl.style.use('seaborn')
        col = 0
        row = 0
        for cluster in clusters:
            df_fltr = df_org[df_org[clustercolumn] == cluster]
            # Print the cluster
            col_index = df_fltr.columns.get_loc(clustercolumn)
            cluster_code = str(df_fltr.iloc[0, col_index])
            print('Cluster Code:' + str(cluster_code))
            df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
            df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)
            # Initialize the figure
            chartcols = ['UPT_ADJ']
            subplot_labels = ['Ridership']
            for mode in modes:
                if (cluster == 3) and (mode == 1):
                    pass
                else:
                    df_fltr_mode = df_fltr_mod[df_fltr_mod.Mode == mode]
                    if mode == 0:
                        mode_name = "BUS"
                    else:
                        mode_name = "RAIL"

                    for chartcol, subplotlable in zip(chartcols, subplot_labels):
                        df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
                                                          label=(str(subplotlable) + ' - ' + mode_name),
                                                          ax=ax[row][col], legend=True)
                        ax[row][col].set_prop_cycle(custom_cycler)
                        ax[row][col].legend(loc='best', fontsize=10)
                        ax[row][col].set_title(str(subplotlable))
                        ax[row][col].set_autoscaley_on(True)
                        try:
                            ax[row][col].grid(True)
                            ax[row][col].margins(0.20)
                        except ValueError:
                            pass
            if row >= 1:
                row = 0
                col += 1
            else:
                row += 1

        # for z in fig.get_axes():
        #     z.label_outer()

        fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
        _figno = x
        # get the abs path of the directory of the code/script
        # Factors and Ridership Data\ code
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Change the directory
        # \Script Outputs
        # change the directory to where the file would be saved
        current_dir = current_dir.parents[0] / 'Script Outputs'
        os.chdir(str(current_dir))
        print("Current set directory: ", current_dir)
        outputdirectory = "Est7_Outputs"
        p = pathlib.Path(outputdirectory)
        p.mkdir(parents=True, exist_ok=True)
        current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
        os.chdir(str(current_dir))
        # Axis title
        # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
        figlabel = ""

        fig.text(0.02, 0.5, 'Ridership', ha='center', va='baseline', rotation='vertical',
                 fontsize=16)
        figname = ("Est7 - (absolute)" + " Clusterwise Ridership Trends" + ".png")
        figcounter += 1
        figlabel = ""

        fig.savefig(figname)

        plt.suptitle("Clusterwise Ridership Trends", fontsize=10)
        plt.style.use('seaborn')
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0, hspace=0)
        plt.tight_layout()
        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)


    except SystemError:
        print("Functional error, in get_clusterwise_UPTs_function")


def get_clusterwise_only_UPTs(_filename, _clusterfile):
    filename = _filename
    clusterfile = _clusterfile
    try:
        chart_name = filename.split('.')[0]
        # get the absolute path of the script and then check if the csv file exists or not
        current_dir = pathlib.Path(__file__).parent.absolute()
        current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
        os.chdir(str(current_dir))
        try:
            if (current_dir / filename).is_file():
                df = pd.read_csv(filename)
                get_clusterwise_UPTs(df, filename, chart_name, clusterfile)
        except FileNotFoundError:
            print("File could not be found. Please check the file is placed in the folder path - Factors and Ridership "
                  "Data\Model Estimation\Est7")
    except FileNotFoundError:
        print("System error, in cluster_level_chart_function")


def pct_change(df):
    df['UPT_PCT_CHNGE'] = 100 * (1 - df.iloc[0].UPT_ADJ / df.UPT_ADJ)
    return df


def get_pct_change_clusterwise(_df, _chart_name, _clusterfile, _filename):
    df_org = _df
    chart_name = _chart_name
    clustercolumn = _clusterfile
    # get unique values
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    modes = df_org['Mode'].unique()
    modes.sort()
    df_org = df_org.groupby([chart_name, 'Mode']).apply(pct_change)
    get_clusterwise_UPTs(df_org, _filename, chart_name, clustercolumn)


def get_clusterwise_UPTs(_df, _filename, _chart_name, _clusterfile):
    try:
        df_org = _df
        filename = _filename
        chart_name = _chart_name
        clustercolumn = _clusterfile
        clusters = df_org[clustercolumn].unique()
        clusters.sort()
        df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
        modes = df_org['Mode'].unique()
        modes.sort()

        figcounter = 1
        clusternumber = 1
        x = 1
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 25), constrained_layout=False, squeeze=False)
        col = 0
        row = 0
        # plt.style.use('seaborn-darkgrid')
        # custom_cycler = (cycler(color=['r', 'g', 'b', 'y']))
        plt.rc('lines', linewidth=2.4)
        # plt.rc('axes', prop_cycle=custom_cycler)
        for mode in modes:
            df_fltr_mode = df_org[df_org.Mode == mode]
            mode_name = ""
            if mode == 0:
                mode_name = "BUS"
            else:
                mode_name = "RAIL"
            for cluster in clusters:
                if (mode == 1) and (cluster == 3):
                    pass
                else:
                    df_fltr = df_fltr_mode[df_fltr_mode[clustercolumn] == cluster]
                    col_index = df_fltr.columns.get_loc(clustercolumn)
                    cluster_code = str(df_fltr.iloc[0, col_index])
                    df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
                    # df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)
                    chartcols = ['UPT_PCT_CHNGE']
                    if cluster == 1:
                        subplot_labels = ['High Op-Ex Group']
                    elif cluster == 2:
                        subplot_labels = ['Mid Op-Ex Group']
                    elif cluster == 3:
                        subplot_labels = ['Low Op-Ex Group']
                    else:
                        subplot_labels = ['New York']

                    for chartcol, subplotlable in zip(chartcols, subplot_labels):
                        df_fltr.groupby('CLUSTER_APTA4').plot(x='Year', y=str(chartcol),
                                                              label=(str(subplotlable)), ax=ax[row][col], legend=True)
                        # ax[row][col].set_prop_cycle(custom_cycler)
                        ax[row][col].legend(loc='best', fontsize=14)
                        ax[row][col].set_title(str(mode_name),fontsize=16)
                        ax[row][col].set_autoscaley_on(True)
                        # for tick in ax.xaxis.get_majorticklabels():  # example for xaxis
                        #     tick.set_fontsize(14)
                        # ax[row][col].xlabel(fontsize=12)
                        # ax[row][col].ylabel(fontsize=12)
                        try:
                            ax[row][col].grid(True)
                            ax[row][col].margins(0.20)
                        except ValueError:
                            pass
            if row >= 1:
                row = 0
                col += 1
            else:
                row += 1


        fig.tight_layout(rect=[0.03, 0.0, 1, 1])
        _figno = x
        # get the abs path of the directory of the code/script
        # Factors and Ridership Data\ code
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Change the directory
        # \Script Outputs
        # change the directory to where the file would be saved
        current_dir = current_dir.parents[0] / 'Script Outputs'
        os.chdir(str(current_dir))
        print("Current set directory: ", current_dir)
        outputdirectory = "Est7_Outputs"
        p = pathlib.Path(outputdirectory)
        p.mkdir(parents=True, exist_ok=True)
        current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
        os.chdir(str(current_dir))
        # Axis title
        # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
        figlabel = ""

        fig.text(0.02, 0.5, 'Percent Change in Ridership from 2002', ha='center', va='baseline', rotation='vertical',
                 fontsize=16)
        figname = ("Est7 - Percent Change in Ridership from 2002" + ".png")
        figcounter += 1
        figlabel = ""

        fig.savefig(figname)

        plt.suptitle("Percent Change in Ridership from 2002", fontsize=10)
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0, hspace=0)
        plt.tight_layout()
        plt.style.use('seaborn')
        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)
    except SystemError:
        print("Functional error, in get_clusterwise_UPTs_function")


def create_clusterwise_pct(_filename, _clusterfile):
    filename = _filename
    chart_name = clusterfile = _clusterfile
    try:
        # get the absolute path of the script and then check if the csv file exists or not
        current_dir = pathlib.Path(__file__).parent.absolute()
        current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
        os.chdir(str(current_dir))
        try:
            if (current_dir / filename).is_file():
                df = pd.read_csv(filename)
                get_pct_change_clusterwise(df, chart_name, clusterfile, filename)
        except FileNotFoundError:
            print("File could not be found. Please check the file is placed in the folder path - Factors and Ridership "
                  "Data\Model Estimation\Est7")
    except FileNotFoundError:
        print("System error, in cluster_level_chart_function")


def main():
    # get the UPT_FAC files created according to the base year
    # base year 2002
    create_upt_fac_cluster_file("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4", 2002, 2018)
    # # # # # # # base year 2012
    create_upt_fac_cluster_file("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4", 2012, 2018)
    # # # # # # get absolute charts
    get_cluster_file_raw("UPT_FAC_totals_APTA4_CLUSTERS_b2002.csv", "CLUSTER_APTA4")
    # # #  # get pct change in core cluster
    create_clusterwise_pct("UPT_FAC_totals_APTA4_CLUSTERS_b2002.csv", "CLUSTER_APTA4")


if __name__ == "__main__":
    main()

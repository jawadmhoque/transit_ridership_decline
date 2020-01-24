# import packages for the file usage
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import os.path
import numpy as np
import os


def TCRP_Summary_Charts(df, clustercolumn, chartcols, plot_labels):
    df_org = df
    df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    # get unique values
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    modes = df_org['Mode'].unique()
    modes.sort()
    mode_name = ""
    figcounter = 1
    clusternumber = 1
    x = 1
    plt.style.use('seaborn-darkgrid')
    for mode in modes:
        df_mode = df_org[df_org['Mode'] == mode]
        df_mode['Year'] = pd.to_datetime(df_mode['Year'].astype(str), format='%Y')
        df_fltr_mod = df_mode.set_index(pd.DatetimeIndex(df_mode['Year']).year)
        col = 0
        row = 0
        for cluster in clusters:
            clustercharts = chartcols.copy()
            if mode == 0:
                mode_name = "BUS"
                clustercharts.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                clustercharts.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
            else:
                mode_name = "RAIL"
                clustercharts.remove('YEARS_SINCE_TNC_BUS2_HINY')
                clustercharts.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
            df_cluster = df_fltr_mod[df_fltr_mod[clustercolumn] == cluster]
            if cluster == float(1):
                cluster_title = 'High Op-Ex Group'
                if mode == 1:
                    clustercharts.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
                    strTNCField = 'YEARS_SINCE_TNC_RAIL2_HINY'
                else:
                    clustercharts.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
                    strTNCField = 'YEARS_SINCE_TNC_BUS2_HINY'
                # dcolor = "black"
            elif cluster == float(2):
                if mode == 1:
                    clustercharts.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                    strTNCField = 'YEARS_SINCE_TNC_RAIL2_MIDLOW'
                else:
                    clustercharts.remove('YEARS_SINCE_TNC_BUS2_HINY')
                    strTNCField = 'YEARS_SINCE_TNC_BUS2_MIDLOW'
                cluster_title = 'Mid Op-Ex Group'
            elif cluster == float(3):
                if mode == 1:
                    clustercharts.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                    strTNCField = 'YEARS_SINCE_TNC_RAIL2_MIDLOW'
                else:
                    clustercharts.remove('YEARS_SINCE_TNC_BUS2_HINY')
                    strTNCField = 'YEARS_SINCE_TNC_BUS2_MIDLOW'
                cluster_title = 'Low Op-Ex Group'
            else:
                cluster_title = 'New York'
                if mode == 1:
                    clustercharts.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
                    strTNCField = 'YEARS_SINCE_TNC_RAIL2_HINY'
                else:
                    clustercharts.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
                    strTNCField = 'YEARS_SINCE_TNC_BUS2_HINY'
            col = 0
            row = 0
            num = 0
            fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(20, 18), constrained_layout=False, squeeze=False)
            combinechartscol = []
            combinedchartslabel = []
            df_cluster['Vehicle_Revenue_Miles'] = df_cluster['UPT_ADJ_VRM_ADJ_log_FAC_cumsum']
            combinechartscol.append('Vehicle_Revenue_Miles')
            combinedchartslabel.append('Vehicle Revenue Miles')

            df_cluster['Land_Use'] = df_cluster['UPT_ADJ'] - df_cluster['POP_EMP_log_FAC_cumsum'] - df_cluster['TSD_POP_PCT_FAC_cumsum']
            combinechartscol.append('Land_Use')
            combinedchartslabel.append('Land Use Changes')

            df_cluster['Inc_HH_Char'] = df_cluster['UPT_ADJ'] - \
                                        df_cluster['TOTAL_MED_INC_INDIV_2018_log_FAC_cumsum'] - \
                                        df_cluster['PCT_HH_NO_VEH_FAC_cumsum'] - \
                                        df_cluster['JTW_HOME_PCT_FAC_cumsum']
            combinechartscol.append('Inc_HH_Char')
            combinedchartslabel.append('Income & Household Characteristics')

            combinechartscol.append('UPT_ADJ_FARE_per_UPT_2018_log_FAC_cumsum')
            combinedchartslabel.append('Average Fare (2018$)')

            combinechartscol.append('UPT_ADJ_GAS_PRICE_2018_log_FAC_cumsum')
            combinedchartslabel.append('Average Gas Price (2018$)')

            strTNCField = strTNCField+"_FAC_cumsum"

            df_cluster['New_Competing_Modes'] =  df_cluster['UPT_ADJ'] - \
                                                 df_cluster[strTNCField] + \
                                                df_cluster['BIKE_SHARE_FAC_cumsum'] + \
                                                df_cluster['scooter_flag_FAC_cumsum']
            combinechartscol.append('New_Competing_Modes')
            combinedchartslabel.append('New Competing Modes')

            transparency = 0.3
            num = 0
            for combinechartcol, combinedchartlabel in zip(combinechartscol, combinedchartslabel):
                df_cluster.groupby('Mode').plot(x='Year',
                                                y=str(combinechartcol),
                                                label='Hypothesized Ridership if no changes in ' + str(combinedchartlabel),
                                                ax=ax[row][col], legend=True,
                                                fontsize=13, linewidth=2.5)
                df_cluster.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Ridership', ax=ax[row][col],
                                                  legend=True, color='black', linewidth=2.5, fontsize=13)
                # Paint the area
                ax[row][col].fill_between(df_cluster['Year'].values, df_cluster[combinechartcol].values,
                                          df_cluster['UPT_ADJ'].values,
                                          where=df_cluster['UPT_ADJ'].values > df_cluster[combinechartcol].values,
                                          facecolor='green', interpolate=True, alpha=transparency)
                ax[row][col].fill_between(df_cluster['Year'].values, df_cluster[combinechartcol].values,
                                          df_cluster['UPT_ADJ'].values,
                                          where=df_cluster['UPT_ADJ'].values <= df_cluster[combinechartcol].values,
                                          facecolor='red', interpolate=True, alpha=transparency)

                ax[row][col].set_xlabel(xlabel="Year", fontsize=15.5)
                ax[row][col].tick_params(labelsize=15.5)
                ax[row][col].legend(loc='best')
                ax[row][col].set_title(str(combinedchartlabel), fontsize=15.5)
                try:
                    ax[row][col].grid(True)
                    ax[row][col].margins(0.20)
                    min_val = min(df_cluster[['UPT_ADJ', combinechartcol]].values.min(1))
                    max_val = max(df_cluster[['UPT_ADJ', combinechartcol]].values.max(1))
                    ax[row][col].set_ylim([min_val * 0.5, max_val * 1.25])
                except ValueError:
                    pass
                if row >= 1:
                    row = 0
                    col += 1
                else:
                    row += 1

            """ 
            This is for each mode,cluster_type charts (12 fields) 
            """
            # for chartcol, subplotlable in zip(clustercharts, plot_labels):
            #     df_cluster.groupby('Mode').plot(x='Year', y=str(chartcol),
            #                                     ax=ax[row][col], legend=True,
            #                                     fontsize=13, linewidth=2.5)
            #     ax[row][col].set_xlabel(xlabel="Year", fontsize=15.5)
            #     ax[row][col].tick_params(labelsize=15.5)
            #     ax[row][col].legend(loc='best')
            #     ax[row][col].set_title(str(subplotlable), fontsize=15.5)
            #     try:
            #         ax[row][col].grid(True)
            #         ax[row][col].margins(0.20)
            #     except ValueError:
            #         pass
            #     if row >= 3:
            #         row = 0
            #         col += 1
            #     else:
            #         row += 1

            for z in fig.get_axes():
                z.label_outer()
            fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
            _figno = x
            current_dir = pathlib.Path(__file__).parent.absolute()
            # Change the directory to ..\Script Outputs
            current_dir = current_dir.parents[0] / 'Script Outputs'
            os.chdir(str(current_dir))
            outputdirectory = "Est7_Outputs"
            p = pathlib.Path(outputdirectory)
            p.mkdir(parents=True, exist_ok=True)
            current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
            os.chdir(str(current_dir))
            # Axis title
            figlabel = ""
            fig.set_size_inches(16.53, 11.69)
            fig.text(0.02, 0.5, figlabel, ha='center', va='baseline', rotation='vertical',
                     fontsize=16)
            figname = ("TCRP Summary Graphs - " + mode_name + " - " + str(cluster_title) + ".png")
            figcounter += 1
            fig.savefig(figname)
            plt.suptitle(clustercolumn, fontsize=18)
            plt.close(fig)
            x += 1
            clusternumber += 1
            print("Successfully created " + figname)


def find_file(filename, clustercolumn):
    # get the abs path of the directory of the code/script
    current_dir = pathlib.Path(__file__).parent.absolute()
    folder_name = chart_name = filename.split('.')[0]
    current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
    os.chdir(str(current_dir))
    df = pd.read_csv(filename)
    chartcols = ['VRM_ADJ', 'FARE_per_UPT_2018',
                 'POP_EMP', 'TSD_POP_PCT',
                 'GAS_PRICE_2018', 'TOTAL_MED_INC_INDIV_2018',
                 'PCT_HH_NO_VEH', 'JTW_HOME_PCT',
                 'YEARS_SINCE_TNC_BUS2_HINY', 'YEARS_SINCE_TNC_BUS2_MIDLOW',
                 'YEARS_SINCE_TNC_RAIL2_HINY', 'YEARS_SINCE_TNC_RAIL2_MIDLOW',
                 'BIKE_SHARE', 'scooter_flag']
    plot_labels = ['Vehicle Revenue Miles', 'Average Fare (2018$)',
                   'Population + Employment', '% of Population in Transit Supportive Density',
                   'Average Gas Price (2018$)', 'Median Per Capita Income (2018$)',
                   '% of Households with 0 Vehicles', '% Working at Home',
                   'Years Since Ride-hail Start', 'Bike Share', 'Electric Scooters']
    TCRP_Summary_Charts(df, clustercolumn, chartcols, plot_labels)


def main():
    """
    # Lets create summary charts
    include a set of FAC charts corresponding to the all six categories as defined for APTA Clusters
    """
    find_file("UPT_FAC_totals_APTA4_CLUSTERS_b2002.csv", "CLUSTER_APTA4")


if __name__ == "__main__":
    main()

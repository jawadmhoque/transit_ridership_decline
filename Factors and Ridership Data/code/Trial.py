# import packages for the file usage
import os.path
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os
from matplotlib import cycler


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
        modes = df_org['Mode'].unique()
        modes.sort()

        figcounter = 1
        clusternumber = 1
        x = 1
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(25, 25), constrained_layout=False, squeeze=False)
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
                        df_fltr.groupby('CLUSTER_APTA4').plot(x='Year', y=str(chartcol),ax=ax[row][col], legend=True)
                        # ax[row][col].set_prop_cycle(custom_cycler)
                        ax[row][col].legend(loc='best', fontsize=10)
                        ax[row][col].set_title(str(mode_name))
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

        fig.text(0.02, 0.5, 'Percent Change in Ridership from 2002', ha='center', va='baseline', rotation='vertical',
                 fontsize=16)
        figname = ("Est7 - Percent Change in Ridership from 2002" + ".png")
        figcounter += 1
        figlabel = ""

        fig.savefig(figname)

        plt.suptitle("Percent Change in Ridership from 2002", fontsize=10)
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
    # Pass on the cluster_file and cluster_column
    # create_upt_fac_total_apta4_cluster("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4")
    create_clusterwise_pct("UPT_FAC_totals_APTA4_CLUSTERS_b2002.csv", "CLUSTER_APTA4")


if __name__ == "__main__":
    main()

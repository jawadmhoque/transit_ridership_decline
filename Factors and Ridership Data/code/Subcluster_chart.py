# import packages for the file usage
import os.path
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os


def pct_change(df):
    df['UPT_PCT_CHNGE'] = 100 * (1 - df.iloc[0].UPT_ADJ / df.UPT_ADJ)
    return df


def get_subclusterwise_charts(_df, _chart_name, _clusterfile, _filename, _subcluster,pct_change_value):
    df_org = _df
    chart_name = _chart_name
    clustercolumn = _clusterfile
    subcluster_field = _subcluster
    # get unique values
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    filter_value = pct_change_value
    if "2002" in filter_value:
        b = 'b2002'
    if "2012" in filter_value:
        b = 'b2012'
    modes = df_org['Mode'].unique()
    modes.sort()
    # df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)

    # df_org = df_org.groupby([chart_name, 'Mode']).apply(pct_change)

    figcounter = 1
    clusternumber = 1
    x = 1

    plt.style.use('seaborn-darkgrid')
    plt.rc('lines', linewidth=2.4)
    for mode in modes:
        df_mode = df_org[df_org['Mode'] == mode]
        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(22, 22), constrained_layout=False, squeeze=False)
        plt.rc('lines', linewidth=2.4)
        col = 0
        row = 0
        if mode == "Bus":
            mode_name = "BUS"
        else:
            mode_name = "RAIL"
        for cluster in clusters:
            df_cluster = df_mode[df_mode[clustercolumn] == cluster]
            if cluster == 1:
                sub_cluster_title = 'High Op-Ex Group'
            elif cluster == 2:
                sub_cluster_title = 'Mid Op-Ex Group'
            elif cluster == 3:
                sub_cluster_title = 'Low Op-Ex Group'
            else:
                sub_cluster_title = 'New York'

            subclusters = df_cluster[subcluster_field].unique()
            subclusters.sort()
            for subcluster in subclusters:
                if subcluster == 1:
                    sub_cluster_label = 'More Favorable External Factors, Stronger Competitiveness'
                elif subcluster == 2:
                    sub_cluster_label = 'More Favorable External Factors, Weaker Competitiveness'
                elif subcluster == 3:
                    sub_cluster_label = 'Less Favorable External Factors, Stronger Competitiveness'
                elif subcluster == 0:
                    sub_cluster_label = 'New York'
                else:
                    sub_cluster_label = 'Less Favorable External Factors, Weaker Competitiveness'
                df_subcluster = df_cluster[df_cluster[subcluster_field] == subcluster]
                df_subcluster['Year'] = pd.to_datetime(df_subcluster['Year'].astype(str), format='%Y')
                df_subcluster.groupby('APTA4_SUBCLUSTER').plot(x='Year', y=pct_change_value, label=sub_cluster_label,
                                                       ax=ax[row][col], legend=True)
                ax[row][col].legend(loc='best', fontsize=10)
                ax[row][col].set_title(str(sub_cluster_title))
                ax[row][col].set_autoscaley_on(True)
                ax[row][col].grid(True)
                ax[row][col].margins(0.20)
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
        figname = ("Est7 - Cluster & subcluster wise - Percent Change in Ridership from " + str(b) + " " + mode_name + ".png")
        figcounter += 1
        figlabel = ""

        fig.savefig(figname)

        plt.suptitle("Percent Change in Ridership from 2002", fontsize=10)
        plt.style.use('seaborn')
        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)


def create_clusterwise_pct(_filename, _clusterfile, _subcluster):
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
                pc_change_value = 'PCT_CHANGE_2002'
                get_subclusterwise_charts(df, chart_name, clusterfile, filename, _subcluster,pc_change_value)
                pc_change_value = 'PCT_CHANGE_2012'
                get_subclusterwise_charts(df, chart_name, clusterfile, filename, _subcluster, pc_change_value)
        except FileNotFoundError:
            print("File could not be found. Please check the file is placed in the folder path - Factors and Ridership "
                  "Data\Model Estimation\Est7")
    except FileNotFoundError:
        print("System error, in cluster_level_chart_function")


def main():
    # Pass on the cluster_file and cluster_column
    # create_upt_fac_total_apta4_cluster("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4")
    create_clusterwise_pct("ridership_cluster.csv", "CLUSTER_APTA4", "APTA4_SUBCLUSTER")


if __name__ == "__main__":
    main()

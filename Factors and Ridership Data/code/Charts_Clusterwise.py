import os.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def

# this is where the code starts
def main():
    script_folder = r'D:\UoK\OneDrive - University of Kentucky\github\Transit_ridership\transit_ridership_decline' \
                    r'\Factors and Ridership Data\code '
    load_data = r'D:\UoK\OneDrive - University of Kentucky\github\Transit_ridership\transit_ridership_decline\Factors ' \
                r'and Ridership Data\Model Estimation\Est4 '
    output_folder = r'D:\UoK\OneDrive - University of Kentucky\github\Transit_ridership\transit_ridership_decline' \
                    r'\Factors and Ridership Data\Script Outputs '
    folder_path = ''
    file_name = ''

    # create cumulative column and update the column
    os.chdir(load_data)
    df_org = pd.read_csv('FAC_totals_GT_CLUSTERS.csv')
    # list(df.columns)
    # create new columsn
    col_name = ['VRM_ADJ_log_FAC', 'FARE_per_UPT_log_FAC', 'POP_EMP_log_FAC', 'GasPrice_log_FAC', 'PCT_HH_NO_VEH_FAC',
                'TSD_POP_PCT_FAC', 'Total_FAC']
    cum_col = []
    col_UPT_ADJ = ['UPT_ADJ']

    for col in col_name:
        df_org[str(col) + '_cumsum'] = df_org[col]
        cum_col.append(str(col) + '_cumsum')

    # # for each cluster_id get the cumulative addition starting from 2002-->2018
    # os.chdir(output_folder)
    for col in cum_col:
        df_org[col] = df_org.groupby(['CLUSTER_GT_NEW_11', 'RAIL_FLAG'])[col].cumsum()

    # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
    for col in cum_col:
        df_org['UPT_ADJ_' + str(col)] = df_org['UPT_ADJ'] - df_org[col]

    # Create_Cumulative_Graphs(dataframe, cluster_values, folder_name, chart_name)
    Create_Cumulative_Graphs(df_org, 'CLUSTER_GT_NEW_11', 'UPT_VAR_CLUSTER_GT', 'UPT_VAR_CLUSTER_GT')
    # prepare_charts(df_org,clusters_col,chartinitials,file_name)


if __name__ == "__main__":
    main()
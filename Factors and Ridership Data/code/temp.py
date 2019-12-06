for cluster in clusters:
    df_fltr_fac = dffac[dffac[clustercolumn] == cluster]
    # Print the cluster
    col_index = df_fltr_fac.columns.get_loc(clustercolumn)
    cluster_code = str(df_fltr_fac.iloc[0, col_index])
    print('Cluster Code:' + str(cluster_code))
    df_fltr_fac['Year'] = pd.to_datetime(df_fltr_fac['Year'].astype(str), format='%Y')
    df_fltr_mod_fac = df_fltr_fac.set_index(pd.DatetimeIndex(df_fltr_fac['Year']).year)

    for mode in modes:
        if mode == 0:
            mode_name = "RAIL"
        else:
            mode_name = "BUS"

        # get number of sub-plots defined - 4*2 means 4 rows having 2 graphs (each sized 18x9) in each row = 8 graphs
        fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(18, 9), constrained_layout=True)
        x = 1
        df_fltr_mode_fac = df_fltr_mod_fac[df_fltr_mod_fac.Mode == mode]

        # Year vs Total_FAC_Scaled --> Graph (0,0)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_Total_FAC_cumsum', label='Hypthoteical rdrship',
                                              ax=ax[0][0], legend=True, color='', linewidth=3)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='Observed Rdrshp', label='UPT_ADJ', ax=ax[0][0], legend=True,
                                              color='black', linewidth=3)
        ax[0][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_Total_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_Total_FAC_cumsum'].values >= df_fltr_mode_fac['UPT_ADJ'].values,
                              facecolor='green', interpolate=True, alpha=0.3)
        ax[0][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_Total_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_Total_FAC_cumsum'].values < df_fltr_mode_fac['UPT_ADJ'].values,
                              facecolor='red', interpolate=True, alpha=0.3)
        ax[0][0].set(xlabel="Years", ylabel='Total_FAC')
        ax[0][0].legend(loc='best')

        # Year vs Total_FAC_Scaled --> Graph (1,0)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_POP_EMP_log_FAC_cumsum',
                                              label='UPT_ADJ - POP_EMP_log_FAC_cumsum', ax=ax[1][0], legend=True)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[1][0], legend=True)
        ax[1][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values >= df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
        ax[1][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_POP_EMP_log_FAC_cumsum'].values < df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
        ax[1][0].set(xlabel="Years", ylabel='POP_EMP')
        ax[1][0].legend(loc='best')

        # Year vs Total_FAC_Scaled --> Graph (2,0)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_TSD_POP_PCT_FAC_cumsum',
                                              label='UPT_ADJ - TSD_POP_PCT_FAC_cumsum', ax=ax[2][0], legend=True)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[2][0], legend=True)
        ax[2][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values >= df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
        ax[2][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values < df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
        ax[2][0].set(xlabel="Years", ylabel='TSD_POP_PCT')
        ax[2][0].legend(loc='best')

        # Year vs Total_FAC_Scaled --> Graph (3,0)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
                                              label='UPT_ADJ - TSD_POP_PCT_FAC_cumsum', ax=ax[3][0], legend=True)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[3][0], legend=True)
        ax[3][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values >= df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
        ax[3][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_TSD_POP_PCT_FAC_cumsum'].values < df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
        ax[3][0].set(xlabel="Years", ylabel='PCT_HH_NO_VEH')
        ax[3][0].legend(loc='best')

        # Year vs Total_FAC_Scaled --> Graph (4,0)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_VRM_ADJ_log_FAC_cumsum',
                                              label='UPT_ADJ - VRM_ADJ_log_FAC_cumsum', ax=ax[4][0], legend=True)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[4][0], legend=True)
        ax[4][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values >= df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
        ax[4][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_VRM_ADJ_log_FAC_cumsum'].values < df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
        ax[4][0].set(xlabel="Years", ylabel='VRM_ADJ')
        ax[4][0].legend(loc='best')

        # Year vs Total_FAC_Scaled --> Graph (5,0)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_GasPrice_log_FAC_cumsum',
                                              label='UPT_ADJ - GasPrice_log_FAC_cumsum', ax=ax[5][0], legend=True)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[5][0], legend=True)
        ax[5][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_GasPrice_log_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_GasPrice_log_FAC_cumsum'].values >= df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
        ax[5][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_GasPrice_log_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_GasPrice_log_FAC_cumsum'].values < df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
        ax[5][0].set(xlabel="Years", ylabel='GasPrice')
        ax[5][0].legend(loc='best')

        # Year vs Total_FAC_Scaled --> Graph (6,0)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ_FARE_per_UPT_log_FAC_cumsum',
                                              label='UPT_ADJ - FARE_per_UPT_log_FAC_cumsum', ax=ax[6][0], legend=True)
        df_fltr_mode_fac.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[6][0], legend=True)
        ax[6][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values >= df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='green', interpolate=True, alpha=0.3)
        ax[6][0].fill_between(df_fltr_mode_fac['Year'].values, df_fltr_mode_fac['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values,
                              df_fltr_mode_fac['UPT_ADJ'].values,
                              where=df_fltr_mode_fac['UPT_ADJ_FARE_per_UPT_log_FAC_cumsum'].values < df_fltr_mode_fac[
                                  'UPT_ADJ'].values, facecolor='red', interpolate=True, alpha=0.3)
        ax[6][0].set(xlabel="Years", ylabel='FARE_per_UPT')
        ax[6][0].legend(loc='best')

        #             # Year vs Total_FAC_Scaled --> Graph (3,1)
        #             df_fltr_mode.groupby('Mode').plot(x='Year', y='TSD_POP_PCT_FAC_cumsum', label='UPT_ADJ - TSD_POP_PCT_FAC_cumsum', ax=ax[3][1], legend=True, marker='',color='skyblue',linewidth=2)
        #             df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='UPT_ADJ', ax=ax[3][1], legend=True, marker='',color='olive',linewidth=2)
        #             ax[3][1].set(xlabel="Years", ylabel='TSD_POP_PCT')
        #             ax[3][1].legend(loc='best')
        fig.suptitle(('Cluster Code:' + str(cluster_code) + "-" + str(mode)), fontsize=14)
        fig.tight_layout()
        _figno = x
        # code to let these file save in the specific folder
        os.chdir(output_folder)
        # add folder name
        #         save_folder = output_folder +'\\' + folder_path
        os.path.join(output_folder, folder_path)

        if not os.path.exists(os.path.join(output_folder, folder_path)):
            os.mkdir(folder_path)
            print(folder_path + " for " + mode_name + " : sucessfully created")
        else:
            print(folder_path + " for " + mode_name + " : already exists")

        mod = output_folder + "\\" + str(folder_path)
        os.chdir(mod)
        fig.savefig(("Fig " + str(_figno) + "-" + cluster_code + " - " + mode_name + ".png"))
        plt.suptitle(cluster_code, fontsize=14)
        plt.close(fig)
        x += 1
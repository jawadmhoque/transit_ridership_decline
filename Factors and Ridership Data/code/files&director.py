import os
# filename = os.getcwd()
# absolute_path = os.path.abspath(".")
# dir paths
script_folder = r'D:\UoK\OneDrive - University of Kentucky\github\Transit_ridership\transit_ridership_decline\Factors and Ridership Data\code'
load_data = r'D:\UoK\OneDrive - University of Kentucky\github\Transit_ridership\transit_ridership_decline\Factors and Ridership Data\Model Estimation\Est4'
output_folder = r'D:\UoK\OneDrive - University of Kentucky\github\Transit_ridership\transit_ridership_decline\Factors and Ridership Data\Script Outputs'
folder_path = ''
file_name = 'FAC_Charts_temp'
# change directory
os.chdir(output_folder)
# print("Current working directory:", os.getcwd())
# print("Current working directory: ", os.getcwd())
print ("Current working directory using abs path: ", os.path.abspath(output_folder))
mod = output_folder + "\\" + "Folder_GT_Jot_Charts" 
print ("Mod working directory using abs path: ", os.path.abspath(mod))

# check if the folder exists or not
if not os.path.exists(mod):
    os.makedirs(file_name)
    print ("Sucess")
else:
    print ("Already exists")
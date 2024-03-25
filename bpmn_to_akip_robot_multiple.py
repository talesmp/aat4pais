import os
import glob
import bpmn_to_akip_robot_single as b2ar

# [General] Finding Files with Extension
def find_files_with_extension(directory, extension):
    return glob.glob(f"{directory}/*.{extension}")

current_directory = os.getcwd().replace('\\', '/')

assessment_process_models_path = current_directory+'/AssessmentProcessModels/'

for apmp in os.listdir(assessment_process_models_path):
  if apmp != 'uncovered-process-models':
    process_folder_name = apmp
    process_folder_path = assessment_process_models_path+apmp+'/'
    bpmn_path = find_files_with_extension(process_folder_path, 'bpmn')[0].replace('\\', '/')
    executed_kw_json_path = process_folder_path+'executedKeywords-'+process_folder_name+'.json'
    b2ar.process_folder_function(apmp, current_directory)
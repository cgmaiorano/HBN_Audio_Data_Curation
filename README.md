# HBN_Audio_Data_Curation
This repository takes in a folder name for the data_run from the Audio QA Pipeline as well as corresponding audio files. Based on the timestamps output into a label file in the QA pipeline, this pipeline segments the larger audio clip for instructions, responses, and stories.

# Install Dependencies
pip install -r requirements.txt 

# Quickstart
python main.py --data_run_folder_name folder_name

# Example
python main.py --data_run_folder_name data_run_20240430_100435

import os
from tqdm import tqdm
from curation_utilities import (
    parse_arguments,
    setup_directories,
    trim
)

def main():
    """This is the main function responsible for audio segment trimming and curation."""
    args = parse_arguments()
    data_run_folder_name = args.data_run_folder_name
    sessions_path = args.sessions
    labels_path = args.labels
    
    audio_segments, sessions, data_run_path, labels = setup_directories("data", data_run_folder_name, sessions_path, labels_path)
    sessions_list = [f for f in os.listdir(sessions) if f.endswith(".wav")]
    
    if not os.path.exists(data_run_path):
        print('data run does not exist.')
    
    for filename in tqdm(sessions_list):
        audio_file_path = os.path.join(sessions, filename)
        label_file_path = os.path.join(labels, f"{filename[:-3]}txt")
        trim(label_file_path, audio_file_path, audio_segments)

if __name__ == "__main__":
    main()

        
        


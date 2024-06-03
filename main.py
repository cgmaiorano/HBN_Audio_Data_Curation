import os
from tqdm import tqdm
from curation_utilities import (
    parse_arguments,
    setup_directories,
    trim,
    log_error,
)

def main():
    """This is the main function responsible for audio segment trimming and curation."""
    args = parse_arguments()
    data_run_path = args.data_run
    sessions_path = args.sessions
    
    error_log_path = os.path.join(data_run_path, "error_log.txt")

    audio_segments, sessions, data_run_path, labels = setup_directories("data", data_run_path, sessions_path)
    sessions_list = [f for f in os.listdir(sessions) if f.endswith(".wav")]
    
    if not os.path.exists(data_run_path):
        print('data run does not exist.')
    
    for filename in tqdm(sessions_list):
        audio_file_path = os.path.join(sessions, filename)
        label_file_path = os.path.join(labels, f"{filename[:-3]}txt")
        try:
            trim(label_file_path, audio_file_path, audio_segments)
        except FileNotFoundError as e:
            log_error(str(e), error_log_path)  # Log the error to error_log.txt

if __name__ == "__main__":
    main()

        
        


import torchaudio
import torch
import os
import json
import sys
import argparse
from pydub import AudioSegment

project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_dir)

def parse_arguments():
    """Parse command line arguments including hyperparameters with defaults from Config."""
    parser = argparse.ArgumentParser(description="Experiment script for session processing.")
    parser.add_argument("--data_run_folder_name", type=str, help="Path to the video folder")
    return parser.parse_args()

def setup_directories(base_dir, data_run):
    """Set up directories for the current run, creating unique folders based on the timestamp."""
    data_run_folder = os.path.join(base_dir, data_run)
    audio_segments = os.path.join(data_run_folder, "audio_segments")
    sessions = os.path.join("data", "sessions")
    labels = os.path.join(data_run_folder, "audacity")
    
    os.makedirs(data_run_folder, exist_ok=True)
    os.makedirs(audio_segments, exist_ok=True)
    os.makedirs(sessions, exist_ok=True)
    os.makedirs(labels, exist_ok=True)

    return(audio_segments, sessions, data_run_folder, labels)

def speech_language_instructions(participant_speech_language_tasks_instructions, audio, audio_label_path):
    first_story = False
    second_story = False
    with open(audio_label_path) as file:
        for line in file:
            line = line.split("\t")
            if line[2].startswith("story_0"):
                first_story = True
            elif line[2].startswith("story_1"):
                second_story = True
            else:
                if float(line[0]) < 0:
                    segment = audio[float(0*1000):float(line[1])*1000]
                else:
                    # segment based on start and end time epr line for instructions
                    segment = audio[float(line[0])*1000:float(line[1])*1000]
                output_file_path = os.path.join(participant_speech_language_tasks_instructions, f"{line[2][:-1]}_instruction.wav")
                segment.export(out_f = output_file_path, format='wav')
    return first_story, second_story

def speech_language_responses_and_stories(participant_speech_language_tasks_responses, participant_reading_language_instruction_and_response, audio, audio_label_path, first_story, second_story):
    with open(audio_label_path) as file:
        previous_task_count = None
        previous_task_name = None
        previous_end_time = None
        for line in file:
            line = line.split("\t")
            start_time = line[0]
            end_time = line[1]
            if line[2].startswith("story_0"):
                if first_story is True and second_story is True:
                    story_0_start = previous_end_time
                elif first_story is True and second_story is False:
                    segment = audio[float(previous_end_time)*1000:]
                    output_file_path = os.path.join(participant_reading_language_instruction_and_response, "peggy_babcock.wav")
                    segment.export(output_file_path, format='wav')
            elif line[2].startswith("story_1"):
                if first_story is True and second_story is True:
                    segment1 = audio[float(story_0_start)*1000:float(start_time)*1000]
                    output_file_path = os.path.join(participant_reading_language_instruction_and_response, "peggy_babcock.wav")
                    segment1.export(output_file_path, format='wav')

                    segment2 = audio[float(start_time)*1000:]
                    output_file_path = os.path.join(participant_reading_language_instruction_and_response, "phonetic_kingdom.wav")
                    segment2.export(output_file_path, format='wav')
            else:
                current_task_count = int(line[2][:2])
                # pass over first loop
                if current_task_count == 0:
                    pass
                # check that the current task count is the correct following task according to protocol order, segment the audio and save to files
                elif current_task_count == previous_task_count + 1:
                    segment = audio[float(previous_end_time)*1000:float(start_time)*1000]
                    output_file_path = os.path.join(participant_speech_language_tasks_responses, previous_task_name + "_response.wav")
                    segment.export(output_file_path, format='wav')
            previous_task_count = current_task_count
            previous_end_time = end_time
            previous_task_name = line[2][:-1]


def trim(label_file_path, corresponding_audio_filepath, audio_segments_path):
     # load the audio file
    audio = AudioSegment.from_file(corresponding_audio_filepath)
    # extract participant ID from path and crate new folder within output_file_path to save all segments per participant
    participant_ID = os.path.basename(label_file_path)[:7]
    output_participant_dir = os.path.join(audio_segments_path, f"{participant_ID}")
    speech_language_tasks = os.path.join(output_participant_dir, "speech_language_tasks")
    reading_language_tasks = os.path.join(output_participant_dir, "reading_language_tasks")
    speech_language_tasks_instructions = os.path.join(speech_language_tasks, "speech_language_instructions")
    speech_language_tasks_responses = os.path.join(speech_language_tasks, "speech_language_responses")
    reading_language_instruction_and_response = os.path.join(reading_language_tasks, "instructions_and_responses")

    os.makedirs(output_participant_dir, exist_ok=True)
    os.makedirs(speech_language_tasks, exist_ok=True)
    os.makedirs(reading_language_tasks, exist_ok=True)
    os.makedirs(speech_language_tasks_instructions, exist_ok=True)
    os.makedirs(speech_language_tasks_responses, exist_ok=True)
    os.makedirs(reading_language_instruction_and_response, exist_ok=True)

    print("Trimming Speech Language Task Instructions")
    first_story, second_story = speech_language_instructions(speech_language_tasks_instructions, audio, label_file_path)

    print("Trimming Responses and Stories")
    speech_language_responses_and_stories(speech_language_tasks_responses, reading_language_instruction_and_response, audio, label_file_path, first_story, second_story)

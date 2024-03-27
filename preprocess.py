import argparse
import cv2
import os
import glob
import json
import shutil

def skip_frames(video_path, skip_interval, output_path):
    if skip_interval>0:
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 1, (width, height))
        skip_interval = frame_count//48
        # print(skip_interval)
        frame_index = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_index % (skip_interval + 1) == 0:
                out.write(frame)
            frame_index += 1

        cap.release()
        out.release()
    else:
        shutil.copy(src=video_path, dst=output_path)

def process_videos(input_dir, output_dir, skip_interval):
    video_files = glob.glob(input_dir + '/**/*.mp4', recursive=True)
    video_files_mov = glob.glob(input_dir + '/**/*.mov', recursive=True)
    for video_file in [*video_files, *video_files_mov]:
        output_path = output_dir + '/' + video_file.split('/')[-1]
        skip_frames(video_file, skip_interval, output_path)

def process_structured_data(json_file_path, input_dir, output_dir, skip_interval):
    print("Data preprocessing STARTED!")
    # Read the JSON file
    print("json_file_path: ", json_file_path)
    with open(json_file_path) as json_file:
        data = json.load(json_file)
    if not os.path.exists(output_dir):
        print('making directory')
        os.makedirs(output_dir)

    # Iterate over the videoData and text arrays in both the train and test sections
    num_text_prompts = 0
    num_videos = 0
    for section in ['train', 'test']:
        if (section in data):
            for i, data_point in enumerate(data[section]):
                text, video_data = data_point[0], data_point[1]
                file_name = video_data.split('/')[-1]
                # Check if the file has the .mp4 format
                if video_data.endswith('.mp4'):# or video_data.endswith('.mov'):
                    # Create the text file name
                    text_file_name = file_name.removesuffix(('.mp4' if (video_data.endswith('.mp4')) else '.mov'))
                    text_file_name = text_file_name + '.txt'
                    # Create the full path for the text file
                    text_file_path = os.path.join(output_dir, text_file_name)
                    video_file_path, video_file_path_out = os.path.join(input_dir, section, video_data), os.path.join(output_dir, file_name)
                    skip_frames(video_file_path, int(skip_interval), output_path=video_file_path_out)
                    num_videos += 1
                    # Create the text file
                    with open(text_file_path, 'w') as text_file:
                        # Write the corresponding text from the text array as the content of the text file
                        text_file.write(text)
                        num_text_prompts += 1

        # for text, video_data in zip(data[section]['text'], data[section]['videoData']):
        #     # Extract the file name
        #     file_name = video_data.split('/')[-1]
        #     # Check if the file has the .mp4 format
        #     if video_data.endswith('.mp4') or video_data.endswith('.mov'):
        #         text_file_name = file_name.removesuffix(('.mp4' if (video_data.endswith('.mp4')) else '.mov'))
        #         # Create the text file name
        #         text_file_name = text_file_name + '.txt'
        #         # Create the full path for the text file
        #         text_file_path = os.path.join(output_dir, text_file_name)
        #         video_file_path, video_file_path_out = os.path.join(input_dir, section, video_data), os.path.join(output_dir, file_name)
        #         skip_frames(video_file_path, skip_interval, output_path=video_file_path_out)
        #         num_videos += 1
        #         # Create the text file
        #         with open(text_file_path, 'w') as text_file:
        #             # Write the corresponding text from the text array as the content of the text file
        #             text_file.write(text)
        #             num_text_prompts += 1
    print(f"Data preprocessing DONE: {num_text_prompts} text prompts -> {num_videos} videos")

# #input dir is folder of images and json is the json for anntoations corresponding to the images in appimate data folder
# input_dir = '/content/drive/MyDrive/Colab Notebooks/datasets/Appimate'
# json_file_path = '/content/drive/MyDrive/Colab Notebooks/datasets/Appimate/dataset.json'
# output_dir = '/content/drive/MyDrive/Colab Notebooks/datasets/Appimate/T2V/train_all_mp4'
# skip_interval = n  # skip every n frames

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True, help="Directory to input data")
    parser.add_argument("--json_file_path", type=str, required=True, help="Path to Data Structure JSON file")
    parser.add_argument("--skip_interval", type=str, default=1, help="Skip afyer n frames")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to output data")
    args = parser.parse_args()

    process_structured_data(args.json_file_path, args.input_dir, args.output_dir, args.skip_interval)
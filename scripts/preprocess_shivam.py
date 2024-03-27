from utils.count_frames import process_videos
from utils.skip_frames import generate_text_files

#input dir is folder of images and json is the json for anntoations corresponding to the images in appimate data folder
input_dir = '/content/drive/MyDrive/Colab Notebooks/datasets/Appimate'
json_file_path = '/content/drive/MyDrive/Colab Notebooks/datasets/Appimate/dataset.json'
output_dir = '/content/drive/MyDrive/Colab Notebooks/datasets/Appimate/T2V/train_all_mp4'
n = 1
skip_interval = n  # skip every n frames

process_videos(input_dir, output_dir, skip_interval)
generate_text_files(output_dir, json_file_path)
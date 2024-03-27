import shutil
import os

# Source folder path
source_folder = '/home/gauravlochab/meetha_visual/Text-To-Video-Finetuning'

# Destination folder path
destination_folder = '/home/gauravlochab/AutoVisual'

# List of folders to exclude
exclude_folders = ['/home/gauravlochab/meetha_visual/Text-To-Video-Finetuning/skipped_all_meetha', '/home/gauravlochab/meetha_visual/Text-To-Video-Finetuning/outputs', 
                   '/home/gauravlochab/meetha_visual/Text-To-Video-Finetuning/text-to-video-ms-1.7b','/home/gauravlochab/meetha_visual/Text-To-Video-Finetuning/Video-BLIP2-Preprocessor',
                   '/home/gauravlochab/meetha_visual/Text-To-Video-Finetuning/__pycache__','/home/gauravlochab/meetha_visual/Text-To-Video-Finetuning/models']

# Function to check if a file/folder should be excluded
def should_exclude(file_path):
    for folder in exclude_folders:
        if file_path.startswith(folder):
            return True
    return False

# Iterate over each file/folder in the source folder
for root, dirs, files in os.walk(source_folder):
    # Exclude folders that match the exclude_folders list
    dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
    
    for file_name in files:
        file_path = os.path.join(root, file_name)
        
        # Check if the file should be excluded
        if not should_exclude(file_path):
            # Construct the destination path
            destination_path = os.path.join(destination_folder, os.path.relpath(file_path, source_folder))
            
            # Create the destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy the file to the destination folder
            shutil.copy(file_path, destination_path)


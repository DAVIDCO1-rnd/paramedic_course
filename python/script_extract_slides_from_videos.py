import os
import shutil
import subprocess


def extract_slides_from_videos(video_folder, scene_threshold=0.4):
    # List all files in the folder
    for filename in os.listdir(video_folder):
        filepath = os.path.join(video_folder, filename)

        # Skip non-video files
        if not os.path.isfile(filepath) or not filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
            continue

        # Create subfolder for each video (without extension)
        name_without_ext = os.path.splitext(filename)[0]
        output_folder = os.path.join(video_folder, name_without_ext)

        # Delete folder if it already exists
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

        # Create new (clean) output folder
        os.makedirs(output_folder, exist_ok=True)

        # Build ffmpeg command
        output_pattern = os.path.join(output_folder, "slide_%05d.jpg")
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", filepath,
            "-vf", f"select='gt(scene,{scene_threshold})'",
            "-vsync", "vfr",
            "-q:v", "2",
            output_pattern
        ]

        print(f"Processing: {filename}")
        try:
            subprocess.run(ffmpeg_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {filename}: {e}")


def main():
    folder_name = "slides"
    current_folder_full_path = os.getcwd()
    parent_folder_full_path = os.path.dirname(current_folder_full_path)
    folder_full_path = os.path.join(parent_folder_full_path, folder_name)

    extract_slides_from_videos(folder_full_path, scene_threshold=0.01)

main()

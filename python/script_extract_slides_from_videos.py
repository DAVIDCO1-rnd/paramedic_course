import os
import shutil
import subprocess


def extract_slides_from_videos(video_folder, scene_threshold=0.4):
    videos_list = os.listdir(video_folder)
    sorted_videos_list = sorted(videos_list)
    for filename in sorted_videos_list:
        filepath = os.path.join(video_folder, filename)

        if not os.path.isfile(filepath) or not filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', 'webm')):
            continue

        name_without_ext = os.path.splitext(filename)[0]
        output_folder = os.path.join(video_folder, name_without_ext)

        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder, exist_ok=True)

        # Step 1: Extract slides with FFmpeg
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
            continue

        # Step 2: Rename images to include total count
        slide_files = sorted([f for f in os.listdir(output_folder) if f.lower().endswith('.jpg')])
        total_slides = len(slide_files)

        for index, old_name in enumerate(slide_files, start=1):
            new_name = f"{index:05d}_out_of_{total_slides:05d}.jpg"
            os.rename(
                os.path.join(output_folder, old_name),
                os.path.join(output_folder, new_name)
            )


def main():
    folder_name = "slides"
    current_folder_full_path = os.getcwd()
    parent_folder_full_path = os.path.dirname(current_folder_full_path)
    folder_full_path = os.path.join(parent_folder_full_path, folder_name)

    extract_slides_from_videos(folder_full_path, scene_threshold=0.005)


main()

import os
import subprocess
import whisper
import yt_dlp
import torch

def generate_hebrew_subtitles(video_path, srt_path):
    """
    Transcribes Hebrew subtitles from a local video using Whisper.
    Uses 'large' model for improved accuracy. Falls back to CPU if needed.
    """
    print("🎙️ Loading Whisper 'large' model for improved accuracy...")

    try:
        # Try loading the large model on GPU if available
        if torch.cuda.is_available():
            device = "cuda"
            try:
                model = whisper.load_model("large", device=device)
            except RuntimeError as e:
                print("⚠️ CUDA out of memory. Falling back to CPU...")
                model = whisper.load_model("large", device="cpu")
        else:
            model = whisper.load_model("large", device="cpu")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return

    print(f"🔊 Transcribing audio from: {video_path}")
    try:
        result = model.transcribe(
            video_path,
            language='he',
            task='transcribe',
            initial_prompt="החייאה, עיסויי חזה, נתיב אוויר, דום לב, החייאת תינוקות, הנשמה, בדיקת דופק"
        )
    except Exception as e:
        print(f"❌ Failed during transcription: {e}")
        return

    print(f"📝 Writing subtitles to: {srt_path}")
    try:
        writer = whisper.utils.get_writer("srt", os.path.dirname(srt_path))
        writer(result, os.path.splitext(os.path.basename(srt_path))[0])
        print("✅ Subtitles saved successfully.")
    except Exception as e:
        print(f"❌ Failed to write subtitles: {e}")



def embed_subtitles_with_ffmpeg(video_path, subtitle_path, output_path):
    """
    Uses ffmpeg to burn subtitles into the video.
    """
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return
    if not os.path.exists(subtitle_path):
        print(f"❌ Subtitle file not found: {subtitle_path}")
        return

    print("🎞️ Embedding subtitles into the video...")
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={subtitle_path}:force_style='FontName=Arial,Fontsize=24'",
        '-c:a', 'copy',
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Finished! Subtitled video saved as: {output_path}")

def download_with_ytdlp(url, output_folder_full_path):
    ydl_opts = {
        'outtmpl': os.path.join(output_folder_full_path, '%(title)s.%(ext)s')
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    output_folder_name = "CPR"
    current_folder = os.getcwd()
    output_folder_full_path = os.path.join(current_folder, output_folder_name)
    input_filename = "cpr7.mkv"

    video_path = os.path.join(output_folder_full_path, input_filename)
    subtitle_path = os.path.join(output_folder_full_path, "hebrew_subs.srt")
    output_path = os.path.join(output_folder_full_path, "cpr7_with_subtitles.mkv")

    # youtube_url = "https://www.youtube.com/watch?v=8UCqC-OBcQ8"
    # output_folder_name = "CPR"
    # current_folder = os.getcwd()
    # output_folder_full_path = os.path.join(current_folder, output_folder_name)
    # os.makedirs(output_folder_full_path, exist_ok=True)
    # download_with_ytdlp(youtube_url, output_folder_full_path)

    generate_hebrew_subtitles(video_path, subtitle_path)
    embed_subtitles_with_ffmpeg(video_path, subtitle_path, output_path)

if __name__ == "__main__":
    main()

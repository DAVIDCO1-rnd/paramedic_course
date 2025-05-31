import os
import subprocess
import whisper
import yt_dlp

def generate_hebrew_subtitles(video_path, srt_path, use_cpu_if_needed=True):
    """
    Transcribes Hebrew subtitles from a local video using Whisper.
    Automatically falls back to CPU or smaller model if needed.
    """
    print("🎙️ Loading Whisper model...")

    # Choose a smaller model to fit most GPUs (or run on CPU)
    try:
        if use_cpu_if_needed:
            model = whisper.load_model("base", device="cpu")
        else:
            model = whisper.load_model("base")
    except RuntimeError as e:
        print("⚠️ Error loading model on GPU. Falling back to CPU...")
        model = whisper.load_model("base", device="cpu")

    print(f"🔊 Transcribing audio from: {video_path}")
    result = model.transcribe(video_path, language='he', task='transcribe')

    print(f"📝 Writing subtitles to: {srt_path}")
    whisper.utils.WriteSRT(result["segments"], srt_path)

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
    input_filename = "cpr_part1.mp4"

    video_path = os.path.join(output_folder_full_path, input_filename)
    subtitle_path = os.path.join(output_folder_full_path, "hebrew_subs.srt")
    output_path = os.path.join(output_folder_full_path, "cpr_part1_with_subs.mp4")

    # youtube_url = "https://www.youtube.com/watch?v=znjUfbXBptw"
    # output_folder_name = "CPR"
    # current_folder = os.getcwd()
    # output_folder_full_path = os.path.join(current_folder, output_folder_name)
    # os.makedirs(output_folder_full_path, exist_ok=True)
    # download_with_ytdlp(youtube_url, output_folder_full_path)

    generate_hebrew_subtitles(video_path, subtitle_path)
    embed_subtitles_with_ffmpeg(video_path, subtitle_path, output_path)

if __name__ == "__main__":
    main()

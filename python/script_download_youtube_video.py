import os
import subprocess
import whisper
import yt_dlp
import torch
import sys


def generate_hebrew_subtitles(video_path, srt_path):
    print("🎙️ Loading Whisper 'large' model for improved accuracy...")

    try:
        if torch.cuda.is_available():
            device = "cuda"
            try:
                model = whisper.load_model("large", device=device)
            except RuntimeError:
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
    outtmpl = os.path.join(output_folder_full_path, '%(title)s.%(ext)s')
    created = []

    def hook(d):
        if d.get('status') == 'finished' and d.get('filename'):
            created.append(d['filename'])

    # ---------------------------
    # IMPORTANT FIX: Cross-platform option
    # ---------------------------
    ydl_opts = {
        'outtmpl': outtmpl,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['he', 'he.*', 'iw'],
        'subtitlesformat': 'srt/best',
        'postprocessors': [
            {'key': 'FFmpegSubtitlesConvertor', 'format': 'srt'}
        ],
        'progress_hooks': [hook],
    }

    # Windows-only SSL workaround (harmless on Ubuntu because it doesn't run there)
    if sys.platform == "win32":
        ydl_opts['nocheckcertificate'] = True

    # --- Download video ---
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(info)

    video_name = os.path.basename(video_path)

    # --- Detect Hebrew subtitle file ---
    base_no_ext = os.path.splitext(video_path)[0]
    subtitle_name = None
    for lang in ('he', 'iw', 'he-IL'):
        cand = f"{base_no_ext}.{lang}.srt"
        if os.path.isfile(cand):
            subtitle_name = os.path.basename(cand)
            break

    # Fallback: any SRT file created
    if not subtitle_name:
        for f in created:
            if f.lower().endswith('.srt') and os.path.isfile(f):
                subtitle_name = os.path.basename(f)
                break

    return video_name, subtitle_name


def main():
    output_folder_name = "CPR9"
    current_folder = os.getcwd()
    output_folder_full_path = os.path.join(current_folder, output_folder_name)

    youtube_url = "https://www.youtube.com/watch?v=EFKjpgBbuKU"
    os.makedirs(output_folder_full_path, exist_ok=True)

    video_name_with_extension, subtitles_filename = download_with_ytdlp(
        youtube_url, output_folder_full_path
    )

    video_name, video_extension = os.path.splitext(video_name_with_extension)
    video_name_with_subtitles = video_name + "_with_subtitles"
    video_name_with_subtitles_with_extension = video_name_with_subtitles + video_extension

    video_full_path = os.path.join(output_folder_full_path, video_name_with_extension)
    subtitles_full_path = os.path.join(output_folder_full_path, subtitles_filename)
    video_with_subtitles_full_path = os.path.join(
        output_folder_full_path, video_name_with_subtitles_with_extension
    )

    embed_subtitles_with_ffmpeg(
        video_full_path,
        subtitles_full_path,
        video_with_subtitles_full_path
    )


if __name__ == "__main__":
    main()

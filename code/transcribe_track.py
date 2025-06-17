import os
import shutil
import pathlib
import sys

try:
    import imageio_ffmpeg as ioff
except ImportError:
    print("Installing imageio-ffmpeg…", file=sys.stderr)
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "imageio-ffmpeg"])
    import imageio_ffmpeg as ioff

# Ensure ffmpeg binary in project dir and PATH
project_dir = pathlib.Path(__file__).resolve().parent
ffmpeg_src = pathlib.Path(ioff.get_ffmpeg_exe())
ffmpeg_dst = project_dir / "ffmpeg"
if not ffmpeg_dst.exists():
    shutil.copy(ffmpeg_src, ffmpeg_dst)
    ffmpeg_dst.chmod(0o755)

os.environ["PATH"] = f"{project_dir}:{os.environ.get('PATH', '')}"

try:
    import whisper
except ImportError:
    print("Installing openai-whisper…", file=sys.stderr)
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "openai-whisper"])
    import whisper

model = whisper.load_model("base")
print("🔊 Transcribing downloaded_track.mp3…", file=sys.stderr)
result = model.transcribe(str(project_dir / "downloaded_track.mp3"), fp16=False)
print("\n===== TRANSCRIPTION =====\n")
print(result["text"])
print("\n=========================") 
import math
import os
import shutil
import subprocess
from pathlib import Path

import soundfile as sf


def split_wav_to_segments(input_wav: Path, output_dir: Path, segment_seconds: int = 5):
    """Split input wav into N files of `segment_seconds` length (last may be shorter)."""
    signal, sr = sf.read(str(input_wav))
    seg_samples = segment_seconds * sr
    num_segments = math.ceil(len(signal) / seg_samples)
    output_dir.mkdir(parents=True, exist_ok=True)
    for i in range(num_segments):
        start = i * seg_samples
        end = min((i + 1) * seg_samples, len(signal))
        segment = signal[start:end]
        out_path = output_dir / f"rap_5sec_{i:03d}.wav"
        sf.write(str(out_path), segment, sr)
    return num_segments


def separate_vocals_in_dir(segments_dir: Path, vocals_dir: Path):
    """Run Demucs 2-stem separation (vocals) on every wav in `segments_dir`."""
    vocals_dir.mkdir(parents=True, exist_ok=True)
    for wav in sorted(segments_dir.glob("*.wav")):
        print(f"→ separating {wav.name} …")
        # Demucs will create structure <vocals_dir>/<model>/<track_name>/vocals.wav
        subprocess.run([
            "python",
            "-m",
            "demucs.separate",
            "--two-stems=vocals",
            "--name",
            "htdemucs_ft",
            "-o",
            str(vocals_dir),
            str(wav),
        ], check=True)
        # Move resulting vocals file up one level and clean folders
        model_dir = vocals_dir / "htdemucs_ft"
        track_dir = model_dir / wav.stem
        vocals_file = track_dir / "vocals.wav"
        if vocals_file.exists():
            final_path = vocals_dir / f"vocals_{wav.stem}.wav"
            shutil.move(str(vocals_file), str(final_path))
        # Remove intermediate folders
        shutil.rmtree(model_dir, ignore_errors=True)


def main():
    home = Path.home()
    input_wav = home / "Downloads" / "Хочу еще!.wav"
    if not input_wav.exists():
        raise FileNotFoundError(f"Не найден файл {input_wav}. Поместите исходный WAV в папку Downloads.")

    segments_dir = home / "Desktop" / "Хочу_5sec_segments"
    vocals_dir = home / "Desktop" / "Хочу_5sec_vocals"

    print("🔄 Режу WAV на 5-секундные сегменты…")
    num = split_wav_to_segments(input_wav, segments_dir)
    print(f"✅ Сегментация завершена: {num} фрагментов → {segments_dir}")

    print("🎤 Отделяю вокал Demucs (это может занять время)…")
    separate_vocals_in_dir(segments_dir, vocals_dir)
    print(f"✅ Готово! Чистые вокальные дорожки: {vocals_dir}")


if __name__ == "__main__":
    main() 
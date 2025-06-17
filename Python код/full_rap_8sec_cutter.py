#!/usr/bin/env python3
"""
Full RAP 8-Second Cutter
Режет полный трек на кусочки по 8 секунд.
Дополнительно удаляет старые 5-секундные сегменты, чтобы не мешались.
"""

from pathlib import Path
from pydub import AudioSegment
import shutil

SEG_LEN_SEC = 8  # длительность сегмента

# ----- пути -----
project_root = Path(__file__).resolve().parent.parent  # папка «хочу еще»
audio_src = project_root / "Аудио треки" / "Я в потоке, нет я в топе ,.wav"
exp_dir = Path.home() / "Desktop" / "эксперименты с музыкой"


def cleanup_old_segments(folder: Path):
    """Удаляет файлы rap_5sec_* из папки экспериментов и вокальных субпапок"""
    removed = 0
    for wav in folder.glob("rap_5sec_*.wav"):
        wav.unlink(missing_ok=True)
        removed += 1
    # чистим вокалы 5-сек.
    vocals_dir = folder / "professional_vocals"
    for mp3 in vocals_dir.glob("vocals_rap_5sec_*.mp3"):
        mp3.unlink(missing_ok=True)
        removed += 1
    if removed:
        print(f"🗑️ Удалены старые 5-секундные файлы: {removed}")


def cut_track_to_segments(src: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"🎤 Загружаю исходный трек: {src}")
    audio = AudioSegment.from_wav(str(src))
    seg_ms = SEG_LEN_SEC * 1000
    total_segments = len(audio) // seg_ms + (1 if len(audio) % seg_ms else 0)
    print(f"🔪 Режу на {total_segments} сегментов по {SEG_LEN_SEC}с…")

    for i in range(total_segments):
        start_ms = i * seg_ms
        end_ms = min((i + 1) * seg_ms, len(audio))
        seg = audio[start_ms:end_ms]
        start_s = start_ms // 1000
        end_s = end_ms // 1000
        fname = f"rap_8sec_{i+1:03d}_{start_s}s-{end_s}s.wav"
        seg.export(out_dir / fname, format="wav")
        if (i + 1) % 10 == 0 or i + 1 == total_segments:
            print(f"✅ {i+1}/{total_segments} ({(i+1)/total_segments*100:.1f}%) записано")
    print(f"🎉 Готово! Файлы в {out_dir}")


def main():
    if not audio_src.exists():
        print(f"❌ Не найден исходный трек: {audio_src}")
        return

    exp_dir.mkdir(parents=True, exist_ok=True)
    cleanup_old_segments(exp_dir)
    cut_track_to_segments(audio_src, exp_dir)


if __name__ == "__main__":
    main() 
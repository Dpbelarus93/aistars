#!/usr/bin/env python3
"""Quick split WAV into 5-sec segments using pydub"""
from pydub import AudioSegment
from pathlib import Path
import sys

if len(sys.argv)<3:
    print("Usage: split_audio_segments.py <input_wav> <output_dir>")
    sys.exit(1)

input_path=Path(sys.argv[1])
output_dir=Path(sys.argv[2])
output_dir.mkdir(parents=True,exist_ok=True)

audio=AudioSegment.from_file(input_path)
segment_ms=5*1000
for i in range(0,len(audio),segment_ms):
    segment=audio[i:i+segment_ms]
    out_file=output_dir/f"segment_{i//1000:04d}.wav"
    segment.export(out_file,format="wav")
print("Done",output_dir) 
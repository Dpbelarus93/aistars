#!/usr/bin/env python3
"""
🚀 Video Upscaler для Higgsfield видео
Апскейл видео с помощью Real-ESRGAN
"""

import os
import cv2
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

def extract_frames(video_path, output_dir):
    """Извлекает кадры из видео"""
    print(f"📼 Извлекаем кадры из {video_path}")
    
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_num = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_path = output_dir / f"frame_{frame_num:06d}.png"
        cv2.imwrite(str(frame_path), frame)
        frame_num += 1
        
        if frame_num % 10 == 0:
            print(f"  📸 Извлечено {frame_num}/{frame_count} кадров")
    
    cap.release()
    print(f"✅ Извлечено {frame_num} кадров, FPS: {fps}")
    return fps, frame_num

def upscale_frames(input_dir, output_dir, scale=4):
    """Апскейлит кадры с помощью Real-ESRGAN"""
    print(f"🚀 Апскейлим кадры (x{scale})...")
    
    realesrgan_path = Path("Real-ESRGAN")
    
    # Скачиваем модель если её нет
    model_path = realesrgan_path / "weights" / "RealESRGAN_x4plus.pth"
    if not model_path.exists():
        print("📥 Скачиваем модель RealESRGAN...")
        model_path.parent.mkdir(exist_ok=True)
        subprocess.run([
            "wget", 
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
            "-O", str(model_path)
        ])
    
    # Апскейлим каждый кадр
    input_frames = list(input_dir.glob("*.png"))
    total_frames = len(input_frames)
    
    for i, frame_path in enumerate(sorted(input_frames)):
        output_frame = output_dir / frame_path.name
        
        # Команда для Real-ESRGAN
        cmd = [
            sys.executable, 
            str(realesrgan_path / "inference_realesrgan.py"),
            "-n", "RealESRGAN_x4plus",
            "-i", str(frame_path),
            "-o", str(output_frame),
            "--outscale", str(scale)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if (i + 1) % 5 == 0:
                print(f"  🔧 Обработано {i + 1}/{total_frames} кадров")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка при обработке {frame_path}: {e}")
    
    print(f"✅ Апскейлено {total_frames} кадров")

def create_video(frames_dir, output_path, fps):
    """Создаёт видео из апскейленных кадров"""
    print(f"🎬 Создаём видео {output_path}")
    
    frames = sorted(frames_dir.glob("*.png"))
    if not frames:
        print("❌ Не найдены апскейленные кадры!")
        return
    
    # Читаем первый кадр для получения размеров
    first_frame = cv2.imread(str(frames[0]))
    height, width = first_frame.shape[:2]
    
    # Создаём видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    for i, frame_path in enumerate(frames):
        frame = cv2.imread(str(frame_path))
        out.write(frame)
        
        if (i + 1) % 10 == 0:
            print(f"  🎞️ Записано {i + 1}/{len(frames)} кадров")
    
    out.release()
    print(f"✅ Видео сохранено: {output_path}")

def upscale_video(input_video, output_video=None, scale=4):
    """Главная функция апскейла видео"""
    input_path = Path(input_video)
    
    if output_video is None:
        output_video = input_path.parent / f"{input_path.stem}_upscaled_x{scale}.mp4"
    else:
        output_video = Path(output_video)
    
    print(f"🎬 Апскейл видео: {input_path} -> {output_video}")
    
    # Создаём временные директории
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        frames_dir = temp_path / "frames"
        upscaled_dir = temp_path / "upscaled"
        
        frames_dir.mkdir()
        upscaled_dir.mkdir()
        
        try:
            # Извлекаем кадры
            fps, frame_count = extract_frames(input_path, frames_dir)
            
            # Апскейлим
            upscale_frames(frames_dir, upscaled_dir, scale)
            
            # Создаём финальное видео
            create_video(upscaled_dir, output_video, fps)
            
            print(f"🎉 Готово! Апскейленное видео: {output_video}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python video_upscaler.py input_video.mp4 [output_video.mp4] [scale]")
        print("Пример: python video_upscaler.py higgsfield_video.mp4 upscaled_4k.mp4 4")
        sys.exit(1)
    
    input_video = sys.argv[1]
    output_video = sys.argv[2] if len(sys.argv) > 2 else None
    scale = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    
    upscale_video(input_video, output_video, scale) 
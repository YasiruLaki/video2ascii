import argparse
import cv2
import os
import time
import yt_dlp

def get_args():
    parser = argparse.ArgumentParser(description="Convert videos into ASCII art")
  
    parser.add_argument(
        "--src", 
        type=str, 
        required=True, 
        help="Path to a local video file or a YouTube URL"
    )
    
    parser.add_argument(
        "--width", 
        type=int, 
        default=120, 
        help="Width of the ASCII output in characters (default: 120)"
    )
    
    parser.add_argument(
        "--fps", 
        type=int, 
        default=30, 
        help="Playback speed in frames per second (default: 30)"
    )
    
    return parser.parse_args()

def get_video_source(src):
    if src.startswith("http"):
        if yt_dlp is None:
            raise RuntimeError(
                "yt-dlp is required to download YouTube videos. Install with: pip install yt-dlp"
            )

        print("Downloading YouTube video with yt-dlp...")
        ydl_opts = {
            'format': 'mp4/best',
            'outtmpl': 'temp_video.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(src, download=True)
                # prepare_filename gives the final filename used by yt-dlp
                filename = ydl.prepare_filename(info)
                return filename
        except Exception as e:
            # Fall back to returning the original source so the caller can decide
            print(f"yt-dlp download failed: {e}")
            raise
    else:
        return src
    

ASCII_CHARS = "@%#*+=-:. "

def pixel_to_char(pixel_value):
    index = int(pixel_value / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]

def frame_to_ascii(frame, width):
    height, orig_width = frame.shape[:2]
    aspect_ratio = height / orig_width
    new_height = int(aspect_ratio * width * 0.55)  # adjust for character aspect ratio
    
    resized = cv2.resize(frame, (width, new_height))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    ascii_frame = ""
    for row in gray:
        line = "".join(pixel_to_char(pixel) for pixel in row)
        ascii_frame += line + "\n"
    return ascii_frame


def play_ascii_video(src, width, fps):
    video = cv2.VideoCapture(src)
    delay = 1 / fps
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        ascii_frame = frame_to_ascii(frame, width)
        os.system("cls" if os.name == "nt" else "clear")
        print(ascii_frame)
        time.sleep(delay)
    
    video.release()
    
    
if __name__ == "__main__":
    args = get_args()
    video_path = get_video_source(args.src)
    play_ascii_video(video_path, args.width, args.fps)

    

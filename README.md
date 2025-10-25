# video_2_asciii

Simple terminal ASCII video player.

Features:
- Plays local videos or webcam streams in ASCII art.
- Optional color output using curses (best-effort, depends on terminal).
- Optional support for downloading YouTube videos with `yt-dlp`.

Usage:

```bash
python playAscii.py --src ./video.mp4 --width 120 --fps 24
```

To enable color output use `--color` (may be slower). To show the original video window use `--show`.

If you want YouTube support, install `yt-dlp`:

```bash
# on macOS with Homebrew
brew install yt-dlp
```# video2ascii

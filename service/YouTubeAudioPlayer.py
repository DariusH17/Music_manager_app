import subprocess
import threading
from typing import List, Optional, Tuple

import numpy as np
import sounddevice as sd
from yt_dlp import YoutubeDL
import imageio_ffmpeg as ffmpeg


class YouTubeAudioPlayer:
    """
    Can enqueue queries/URLs, play in a background thread,
    and skip the current track on demand.
    """

    def __init__(self, sample_rate: int = 44_100, channels: int = 2):
        self.sample_rate = sample_rate
        self.channels = channels
        self._ffmpeg_exe = ffmpeg.get_ffmpeg_exe()

        self._queue: List[str] = []
        self._lock = threading.Lock()
        self._skip_event = threading.Event()
        self._play_thread: Optional[threading.Thread] = None

    def enqueue(self, query: str) -> None:
        with self._lock:
            self._queue.append(query)

    def skip(self) -> None:
        """Signal the player to stop the current track immediately."""
        self._skip_event.set()
        sd.stop()  # abort any ongoing playback

    def play(self) -> None:
        """Start the playback thread (no-op if already running)."""
        if self._play_thread and self._play_thread.is_alive():
            return
        self._play_thread = threading.Thread(
            target=self._playback_loop, daemon=True
        )
        self._play_thread.start()

    def _playback_loop(self):
        while True:
            with self._lock:
                if not self._queue:
                    break
                query = self._queue.pop(0)

            # clear skip flag for this track
            self._skip_event.clear()

            url, title, duration = self._get_audio_info(query)
            print(f"▶️  Now playing: {title!r} ({duration:.1f}s)")

            pcm = self._decode_full_audio(url, duration)

            # start playback
            sd.play(pcm, samplerate=self.sample_rate)

            # block until end or until sd.stop() is called by skip()
            sd.wait()

            if self._skip_event.is_set():
                print("⏭  Skipped!")
            else:
                print("✅  Finished track.")

        print("🏁  Playlist complete.")

    def _get_audio_info(self, query: str) -> Tuple[str, str, float]:
        opts = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "default_search": "ytsearch",
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(query, download=False)
        entry = info["entries"][0] if "entries" in info else info
        return (
            entry["url"],
            entry.get("title", query),
            float(entry.get("duration", 0.0)),
        )

    def _decode_full_audio(self, url: str, duration: float) -> np.ndarray:
        cmd = [
            self._ffmpeg_exe,
            "-hide_banner", "-loglevel", "error",
            "-i", url,
            "-t", str(int(duration)),
            "-vn",
            "-f", "f32le",
            "-ar", str(self.sample_rate),
            "-ac", str(self.channels),
            "pipe:1",
        ]
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        raw = proc.stdout.read()
        proc.wait()
        arr = np.frombuffer(raw, dtype=np.float32)
        return arr.reshape(-1, self.channels)
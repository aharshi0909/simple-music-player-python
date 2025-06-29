import os
import tempfile
import yt_dlp
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class MusicPlayer:
    def __init__(self, data_manager, user_id):
        self.data_manager = data_manager
        self.user_id = user_id
        self.current_track = None
        self.sound = None
        self.is_playing = False

    def _download_audio(self, video_id):
        path = os.path.join(tempfile.gettempdir(), f"{video_id}.mp3")
        if os.path.exists(path):
            return path

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        return path

    def load_track(self, track, autoplay=False):
        if self.sound:
            self.sound.stop()
            self.sound.unload()

        self.current_track = track
        audio_path = self._download_audio(track["video_id"])
        self.sound = SoundLoader.load(audio_path)

        if self.sound:
            self.sound.bind(on_stop=self._on_stop)
            if autoplay:
                self.play()

    def play(self):
        if self.sound:
            self.sound.play()
            self.is_playing = True
            self.data_manager.add_to_listening_history(self.user_id, self.current_track)

    def pause(self):
        if self.sound:
            self.sound.stop()
            self.is_playing = False

    def toggle_playback(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def _on_stop(self, *args):
        self.is_playing = False

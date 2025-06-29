from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from data_manager import DataManager
from music_player import MusicPlayer
from youtube_api import search_youtube, get_recommendations
from kivy.uix.button import Button

Window.size = (400, 700)

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = "user_1"
        self.dm = DataManager()
        self.player = MusicPlayer(self.dm, self.user_id)

    def play_video(self, video_id, title):
        self.player.load_track({"video_id": video_id, "title": title}, autoplay=True)
        self.ids.now_playing.text = f"🎵 Playing: {title}"

    def toggle_playback(self):
        self.player.toggle_playback()

    def search_video(self):
        query = self.ids.search_input.text.strip()
        if not query:
            self.ids.now_playing.text = "Enter search text"
            return
        results = search_youtube(query)
        self.display_results(results)

    def recommend(self):
        history = self.dm.get_user_listening_history(self.user_id)
        if not history:
            self.ids.now_playing.text = "No history to recommend from"
            return
        last_vid = history[0].get("video_id")
        results = get_recommendations(last_vid)
        self.display_results(results)

    def display_results(self, results):
        self.ids.results_layout.clear_widgets()
        for item in results:
            btn = Button(
                text=item["title"],
                size_hint_y=None,
                height=40,
                on_release=lambda x, i=item: self.play_video(i["video_id"], i["title"])
            )
            self.ids.results_layout.add_widget(btn)

KV = """
<MainLayout>:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    TextInput:
        id: search_input
        hint_text: "Search or enter YouTube video ID"
        size_hint_y: None
        height: 40

    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 10

        Button:
            text: "Search"
            on_release: root.search_video()

        Button:
            text: "Recommend"
            on_release: root.recommend()

    ScrollView:
        size_hint: (1, 0.5)
        GridLayout:
            id: results_layout
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
            padding: 5

    Button:
        text: "Pause / Resume"
        size_hint_y: None
        height: 50
        on_release: root.toggle_playback()

    Label:
        id: now_playing
        text: "Now playing..."
        size_hint_y: None
        height: 40
"""

class YTMusicApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    YTMusicApp().run()
